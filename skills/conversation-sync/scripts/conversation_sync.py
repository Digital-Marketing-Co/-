#!/usr/bin/env python3
"""Deterministic ConversationSync snapshot staging and encrypted GitHub delivery."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, HTTPRedirectHandler, build_opener

IDLE_US = 6_000_000_000
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
SCHEMA = """
CREATE TABLE IF NOT EXISTS project (
  id TEXT PRIMARY KEY, body BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS revision (
  id TEXT PRIMARY KEY, conversation TEXT NOT NULL, observed INTEGER,
  due INTEGER, active INTEGER NOT NULL, body BLOB NOT NULL, current INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS due_revision ON revision(current, active, due);
CREATE TABLE IF NOT EXISTS project_conflict (
  id TEXT NOT NULL, checksum TEXT NOT NULL, body BLOB NOT NULL, PRIMARY KEY(id, checksum)
);
CREATE TABLE IF NOT EXISTS destination (
  channel TEXT PRIMARY KEY, identity TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS delivery (
  revision TEXT NOT NULL, destination TEXT NOT NULL, bundle BLOB NOT NULL,
  receipt TEXT, PRIMARY KEY(revision, destination)
);
"""


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def instant(value):
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError("timestamps must include a timezone")
    delta = parsed - EPOCH
    return (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds


def require_id(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("a stable nonempty source or destination ID is required")
    return value


def project_key(provider, scope, project_id):
    return digest(canonical([provider, scope, require_id(project_id)]))


def normalize(envelope, now):
    provider = require_id(envelope["provider"])
    scope = require_id(envelope["scope"])
    projects = {}
    for project in envelope.get("projects", []):
        key = project_key(provider, scope, project["id"])
        status = project["instruction_status"]
        if status not in {"present", "confirmed_empty", "omitted", "denied", "unsupported"}:
            raise ValueError("invalid project instruction status")
        if status == "present" and not isinstance(project.get("instructions"), str):
            raise ValueError("present project instructions require original text")
        content = canonical(project)
        if key in projects and projects[key] != content:
            raise ValueError("conflicting project records")
        projects[key] = content

    rows = {}
    for record in envelope["conversations"]:
        identity = digest(canonical([provider, scope, require_id(record["id"])]))
        activity = record.get("last_activity_at")
        observed = instant(activity) if activity is not None else None
        if observed is not None and observed > now:
            raise ValueError("future source timestamp must be reconciled")
        if not isinstance(record["messages"], list):
            raise ValueError("messages must be an ordered array")
        active = record.get("in_progress", False)
        if not isinstance(active, bool):
            raise ValueError("in_progress must be Boolean")
        memberships = sorted({project_key(provider, scope, value)
                              for value in record.get("project_ids", [])})
        original = dict(record)
        original["project_ids"] = sorted(set(record.get("project_ids", [])))
        body = canonical({"schema": 1, "source": provider, "scope": scope,
                          "conversation": identity, "record": original,
                          "project_keys": memberships})
        revision = digest(body)
        if identity in rows and rows[identity][0] != revision:
            raise ValueError("combine duplicate discoveries into one record per conversation")
        rows[identity] = (revision, identity, observed,
                          None if observed is None else observed + IDLE_US, active, body)
    return projects, rows.values()


def chatgpt_export(records, scope):
    """Read one supported export shape without inferring live state or project membership."""
    if not isinstance(records, list):
        raise ValueError("expected a ChatGPT conversation JSON array")
    conversations = []
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("mapping"), dict):
            raise ValueError("unsupported ChatGPT conversation record")
        mapping = record["mapping"]
        node_id = record.get("current_node")
        messages = []
        visited = set()
        while node_id is not None:
            if not isinstance(node_id, str) or node_id in visited or node_id not in mapping:
                raise ValueError("invalid ChatGPT conversation branch")
            visited.add(node_id)
            node = mapping[node_id]
            if not isinstance(node, dict):
                raise ValueError("invalid ChatGPT conversation node")
            if isinstance(node.get("message"), dict):
                messages.append(node["message"])
            node_id = node.get("parent")
        timestamps = []
        for node in mapping.values():
            if not isinstance(node, dict):
                raise ValueError("invalid ChatGPT conversation node")
            message = node.get("message")
            if not isinstance(message, dict):
                continue
            for field in ("create_time", "update_time"):
                value = message.get(field)
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    continue
                try:
                    timestamp = Decimal(str(value))
                    if timestamp.is_finite() and timestamp >= 0:
                        timestamps.append(timestamp)
                except InvalidOperation:
                    continue
        activity = None
        if timestamps:
            try:
                activity = datetime.fromtimestamp(float(max(timestamps)), timezone.utc).isoformat()
            except (OverflowError, OSError, ValueError):
                raise ValueError("invalid ChatGPT message timestamp") from None
        conversations.append({
            "id": require_id(record.get("conversation_id") or record.get("id")),
            "last_activity_at": activity,
            "activity_evidence": "snapshot_message_timestamps" if activity else "unavailable",
            "messages": list(reversed(messages)),
            "project_ids": [],
            "project_discovery": "unsupported_in_this_export_adapter",
            "source_record": record,
        })
    return {"provider": "chatgpt-export", "scope": require_id(scope), "conversations": conversations}


def ledger(path):
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    os.close(fd)
    if Path(path).stat().st_mode & 0o077:
        raise ValueError("state database permissions must be 0600")
    db = sqlite3.connect(path, timeout=30)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def ingest(db, projects, rows):
    result = {"inserted": 0, "unchanged": 0, "conflict": 0, "project_conflict": 0}
    with db:
        db.execute("BEGIN IMMEDIATE")
        for key, body in projects.items():
            prior = db.execute("SELECT body FROM project WHERE id=?", (key,)).fetchone()
            if prior and prior["body"] != body:
                db.execute("INSERT OR IGNORE INTO project_conflict VALUES (?,?,?)",
                           (key, digest(body), body))
                result["project_conflict"] += 1
            else:
                db.execute("INSERT OR IGNORE INTO project VALUES (?,?)", (key, body))
        for row in rows:
            revision, identity, observed, *_ = row
            if db.execute("SELECT 1 FROM revision WHERE id=?", (revision,)).fetchone():
                result["unchanged"] += 1
                continue
            current = db.execute(
                "SELECT observed FROM revision WHERE conversation=? AND current=1",
                (identity,)).fetchone()
            newer = not current or (
                current["observed"] is not None and observed is not None
                and observed > current["observed"])
            if newer:
                db.execute("UPDATE revision SET current=0 WHERE conversation=?", (identity,))
            db.execute("INSERT INTO revision VALUES (?,?,?,?,?,?,?)", (*row, int(newer)))
            result["inserted" if newer else "conflict"] += 1
    return result


def eligible(db, revision, now):
    row = db.execute("SELECT * FROM revision WHERE id=?", (revision,)).fetchone()
    if not row or not row["current"] or row["active"] or row["due"] is None or row["due"] > now:
        raise ValueError("revision is not eligible against the supplied snapshot")
    return row


def private_file(path, content):
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
        stream.write(content)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        return None


class GitHub:
    def __init__(self, repository, repository_id, branch, token):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("invalid GitHub owner/repository")
        self.root = "/repos/" + repository
        self.repository = repository
        self.repository_id = repository_id
        self.branch = require_id(branch)
        self.opener = build_opener(NoRedirect())
        self.headers = {"Authorization": "Bearer " + token,
                        "Accept": "application/vnd.github+json"}

    def request(self, path, payload=None):
        request = Request("https://api.github.com" + path,
                          data=None if payload is None else canonical(payload),
                          headers={**self.headers, "Content-Type": "application/json"},
                          method="GET" if payload is None else "PUT")
        with self.opener.open(request, timeout=25) as response:
            return json.load(response)

    def verify_destination(self):
        actual = self.request(self.root)
        if (actual["id"] != self.repository_id or actual["visibility"] != "private"
                or actual["full_name"].casefold() != self.repository.casefold()):
            raise ValueError("configured GitHub repository identity or privacy did not verify")
        return self.request(self.root + "/branches/" + quote(self.branch, safe=""))["commit"]["sha"]

    def read(self, path, ref=None):
        try:
            data = self.request(self.root + "/contents/" + path + "?" +
                                urlencode({"ref": ref or self.branch}))
        except HTTPError as error:
            if error.code == 404:
                return None
            raise
        return base64.b64decode(data["content"])

    def create(self, path, bundle):
        return self.request(self.root + "/contents/" + path, {
            "message": "Archive ConversationSync revision",
            "branch": self.branch, "content": base64.b64encode(bundle).decode()})


def bind_destination(db, channel, identity):
    configured = db.execute("SELECT identity FROM destination WHERE channel=?",
                            (channel,)).fetchone()
    if configured and configured["identity"] != identity:
        raise ValueError("destination changed; preserve the existing queue and review the configuration")
    db.execute("INSERT OR IGNORE INTO destination VALUES (?,?)", (channel, identity))


def push(db, revision, now, github, key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    destination = canonical([github.repository_id, github.branch]).decode()
    github.verify_destination()
    with db:
        db.execute("BEGIN IMMEDIATE")
        row = eligible(db, revision, now)
        bind_destination(db, "github", destination)
        stored = db.execute("SELECT * FROM delivery WHERE revision=? AND destination=?",
                            (revision, destination)).fetchone()
        if stored:
            bundle = stored["bundle"]
        else:
            nonce = secrets.token_bytes(12)
            aad = canonical([github.repository_id, github.branch, revision])
            bundle = b"CS1" + nonce + AESGCM(key).encrypt(nonce, row["body"], aad)
            if len(bundle) > 900_000:
                raise ValueError("bundle exceeds this adapter's verified read-back size limit")
            db.execute("INSERT INTO delivery VALUES (?,?,?,NULL)", (revision, destination, bundle))
    path = "conversation-sync/" + revision + ".enc"
    existing = github.read(path)
    if existing is None:
        eligible(db, revision, now)
        github.verify_destination()
        try:
            github.create(path, bundle)
        except (HTTPError, OSError, TimeoutError):
            if github.read(path) != bundle:
                raise
    commit = github.verify_destination()
    if github.read(path, commit) != bundle:
        raise ValueError("remote read-back did not match the staged encrypted bytes")
    receipt = {"status": "repo_pushed_verified", "repository_id": github.repository_id,
               "branch": github.branch, "path": path, "ciphertext_sha256": digest(bundle),
               "verified_branch_head": commit, "verified_at": datetime.now(timezone.utc).isoformat()}
    with db:
        db.execute("UPDATE delivery SET receipt=? WHERE revision=? AND destination=?",
                   (json.dumps(receipt), revision, destination))
    return receipt


def stage_chatgpt(db, revision, now, workspace, output):
    require_id(workspace)
    with db:
        db.execute("BEGIN IMMEDIATE")
        row = eligible(db, revision, now)
        bind_destination(db, "chatgpt", workspace)
        body = json.loads(row["body"])
        projects = []
        for key in body["project_keys"]:
            project = db.execute("SELECT body FROM project WHERE id=?", (key,)).fetchone()
            conflict = db.execute("SELECT 1 FROM project_conflict WHERE id=?", (key,)).fetchone()
            status = "conflict" if conflict else "manual_review" if project else "unavailable"
            projects.append({"project_key": key, "installation_status": status,
                             "record": json.loads(project["body"]) if project else None})
        package = canonical({"status": "upload_required", "snapshot_only": True,
                             "receiving_workspace": workspace, "revision": revision,
                             "conversation": body, "projects": projects})
        try:
            private_file(output, package)
        except FileExistsError:
            if output.is_symlink() or output.stat().st_mode & 0o077 or output.read_bytes() != package:
                raise ValueError("existing output does not match the private staged package") from None
    return {"status": "upload_required", "revision": revision, "project_count": len(projects)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    load = commands.add_parser("ingest")
    load.add_argument("export", type=Path)
    load.add_argument("--dry-run", action="store_true")
    load.add_argument("--chatgpt-export-scope", help="operator-confirmed account or workspace for ChatGPT conversation JSON")
    commands.add_parser("status")
    for verb in ("stage-chatgpt", "push-github"):
        sub = commands.add_parser(verb)
        sub.add_argument("revision")
        sub.add_argument("--authorize-snapshot", action="store_true", required=True)
        if verb == "stage-chatgpt":
            sub.add_argument("--workspace", required=True)
            sub.add_argument("--output", type=Path, required=True)
        else:
            sub.add_argument("--repository", required=True)
            sub.add_argument("--repository-id", required=True, type=int)
            sub.add_argument("--branch", required=True)
    args = parser.parse_args()
    now = instant(datetime.now(timezone.utc).isoformat())
    if args.command == "ingest":
        source = json.loads(args.export.read_bytes())
        if args.chatgpt_export_scope is not None:
            source = chatgpt_export(source, args.chatgpt_export_scope)
        projects, rows = normalize(source, now)
        result = {"projects": len(projects), "conversations": len(rows), "snapshot_only": True}
        if not args.dry_run:
            result.update(ingest(ledger(args.db), projects, rows))
    else:
        db = ledger(args.db)
        if args.command == "status":
            result = {"snapshot_only": True, "revisions": [dict(row) for row in db.execute(
                "SELECT id,conversation,due,active,current FROM revision ORDER BY due,id")],
                      "receipts": [json.loads(row[0]) for row in db.execute(
                          "SELECT receipt FROM delivery WHERE receipt IS NOT NULL")]}
        elif args.command == "stage-chatgpt":
            result = stage_chatgpt(db, args.revision, now, args.workspace, args.output)
        else:
            github = GitHub(args.repository, args.repository_id, args.branch,
                            os.environ["CONVERSATION_SYNC_GITHUB_TOKEN"])
            key = base64.b64decode(os.environ["CONVERSATION_SYNC_KEY"], validate=True)
            if len(key) != 32:
                raise ValueError("provide a base64-encoded 32-byte encryption key")
            result = push(db, args.revision, now, github, key)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, sqlite3.Error) as error:
        raise SystemExit(f"ConversationSync: {error}") from None
