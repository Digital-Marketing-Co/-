#!/usr/bin/env python3
"""Plan or apply account-wide skill synchronization using full Git history."""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ACCOUNT = "Digital-Marketing-Co"
CANONICAL = "-"
SKILL = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\Z")
STAMP = re.compile(r"Skill-Sync-Stamp: (\S+) ([0-9a-f]{40}) ([0-9]+)\Z")
SENSITIVE = re.compile(
    r"(?im)-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|"
    r"AKIA[A-Z0-9]{16})\b"
)
SHARED = "skills/references"


@dataclass(frozen=True)
class Repo:
    name: str
    url: str
    branch: str
    private: bool


@dataclass(frozen=True)
class Revision:
    repo: Repo
    tree: str
    updated: int
    commit: str


def command(*args, cwd=None, env=None, input_text=None):
    child_env = dict(os.environ if env is None else env, GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(
        args, cwd=cwd, env=child_env, input=input_text, text=True, capture_output=True
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{args[0]} {args[1]} failed: {detail}")
    return result.stdout.strip()


def git(work, *args, **kwargs):
    return command(
        "git", "-c", "credential.https://github.com.helper=",
        "-c", "credential.https://github.com.helper=!gh auth git-credential",
        *args, cwd=work, **kwargs,
    )


def discover():
    rows = json.loads(command(
        "gh", "repo", "list", ACCOUNT, "--limit", "10000", "--json",
        "name,url,isPrivate,isArchived,defaultBranchRef",
    ))
    repos = []
    excluded = []
    for row in rows:
        branch = row["defaultBranchRef"]
        if row["isArchived"] or not branch:
            excluded.append({
                "repo": row["name"],
                "reason": "archived" if row["isArchived"] else "no default branch",
            })
            continue
        repos.append(Repo(row["name"], row["url"] + ".git", branch["name"], row["isPrivate"]))
    if not any(repo.name == CANONICAL for repo in repos):
        raise RuntimeError("Canonical repository missing from account inventory")
    return sorted(repos, key=lambda repo: (repo.name != CANONICAL, repo.name.casefold())), excluded


def remote_head(work, repo):
    ref = f"refs/heads/{repo.branch}"
    result = git(work, "ls-remote", "--refs", repo.url, ref)
    if not result:
        raise RuntimeError(f"{repo.name}: default branch {repo.branch} is missing")
    return result.split()[0]


def inventory(work, repo, head):
    revisions = {}
    for line in git(work, "ls-tree", "-d", head, "skills/").splitlines():
        metadata, path = line.split("\t", 1)
        name = path.removeprefix("skills/")
        tree = metadata.split()[2]
        if path != SHARED:
            marker = git(work, "ls-tree", tree, "SKILL.md")
            if not marker:
                continue
            if not SKILL.fullmatch(name) or not marker.startswith(("100644 blob ", "100755 blob ")):
                raise RuntimeError(f"{repo.name}: invalid skill directory or marker {path}")
        log = git(work, "log", "-1", "--format=%H%n%ct%n%B", head, "--", path).splitlines()
        if len(log) < 2:
            raise RuntimeError(f"{repo.name}: missing update history for {path}")
        commit, updated = log[0], int(log[1])
        for message_line in log[2:]:
            stamp = STAMP.fullmatch(message_line)
            if stamp and stamp[1] == path and stamp[2] == tree:
                updated = int(stamp[3])
        revisions[path] = Revision(repo, tree, updated, commit)
    return revisions


def make_plans(repos, inventories):
    candidates = defaultdict(list)
    for repo in repos:
        for path, revision in inventories[repo].items():
            candidates[path].append(revision)
    plans, conflicts, withheld = {}, [], []
    for repo in repos:
        changes = {}
        for path, versions in sorted(candidates.items()):
            ranked = sorted(
                versions,
                key=lambda v: (-v.updated, v.repo.name != CANONICAL, v.repo.name.casefold()),
            )
            eligible = [v for v in ranked if repo.private or not v.repo.private]
            if not repo.private and (not eligible or eligible[0].tree != ranked[0].tree):
                withheld.append({"repo": repo.name, "path": path, "reason": "newest tree is private"})
            if not eligible:
                continue
            winner = eligible[0]
            previous = inventories[repo].get(path)
            if previous and previous.tree == winner.tree:
                continue
            changes[path] = winner
            conflicts.append({
                "repo": repo.name, "path": path, "source": winner.repo.name,
                "source_commit": winner.commit, "updated_epoch": winner.updated,
                "previous_tree": previous.tree if previous else None, "tree": winner.tree,
                "timestamp_tie": any(
                    v.updated == winner.updated and v.tree != winner.tree for v in eligible
                ),
            })
        plans[repo] = changes
    return plans, conflicts, withheld


def verify_transfer(work, changes):
    for path, revision in changes.items():
        for entry in git(work, "ls-tree", "-rz", revision.tree).split("\0"):
            if not entry:
                continue
            metadata, name = entry.split("\t", 1)
            mode, _, blob = metadata.split()
            if (
                mode not in {"100644", "100755"}
                or any(
                    part.lower() in {".git", ".env", ".npmrc", ".netrc", "credentials.json"}
                    or part.lower().startswith(".env.")
                    or part.lower().endswith((".key", ".p12", ".pfx"))
                    for part in name.split("/")
                )
            ):
                raise RuntimeError(f"Unsafe Git entry or credential-like file: {path}/{name}")
            data = subprocess.check_output(["git", "cat-file", "blob", blob], cwd=work)
            if SENSITIVE.search(data.decode("utf-8", errors="replace")):
                raise RuntimeError(f"Possible credential detected: {path}/{name}")


def prepare(work, repo, head, changes, validator):
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        env = dict(os.environ, GIT_INDEX_FILE=str(temp / "index"), GIT_WORK_TREE=str(temp))
        git(work, "read-tree", head, env=env)
        for path, revision in changes.items():
            existing = git(work, "ls-tree", head, path)
            if existing and " tree " not in existing.split("\t", 1)[0]:
                raise RuntimeError(f"{repo.name}: non-directory obstructs {path}")
            members = git(work, "ls-files", "-z", "--", path, env=env)
            if members:
                # ls-files is NUL-terminated and git update-index reads exact tracked paths.
                git(work, "update-index", "--force-remove", "-z", "--stdin", env=env, input_text=members)
            git(work, "read-tree", f"--prefix={path}/", revision.tree, env=env)
        tree = git(work, "write-tree", env=env)
        for path, revision in changes.items():
            if git(work, "rev-parse", f"{tree}:{path}") != revision.tree:
                raise RuntimeError(f"{repo.name}: staged tree mismatch for {path}")
        skill_tree = git(work, "rev-parse", f"{tree}:skills")
        check = temp / "check"
        check.mkdir()
        # Use a skills-only tree for validation. Do not run scripts from consumers.
        validation_env = dict(env, GIT_INDEX_FILE=str(temp / "validation-index"))
        git(work, "read-tree", "--empty", env=validation_env)
        git(work, "read-tree", "--prefix=skills/", skill_tree, env=validation_env)
        git(work, "checkout-index", "-a", f"--prefix={check}/", env=validation_env)
        command(sys.executable, str(validator), "--root", str(check))
        stamps = "\n".join(
            f"Skill-Sync-Stamp: {path} {revision.tree} {revision.updated}"
            for path, revision in changes.items()
        )
        return git(
            work, "commit-tree", tree, "-p", head,
            input_text=f"Synchronize skills by last update timestamp\n\n{stamps}\n",
        )


def run(apply):
    repos, excluded = discover()
    validator = Path(__file__).resolve().with_name("validate_skills.py")
    report = {"mode": "apply" if apply else "dry-run", "excluded": excluded, "repositories": {}}
    try:
        with tempfile.TemporaryDirectory(prefix="dmc-skill-sync-") as work:
            git(work, "init", "--bare", "-q")
            heads, inventories, failed = {}, {}, False
            for repo in repos:
                try:
                    ref = f"refs/skill-sync/{repo.name}"
                    git(work, "fetch", "--quiet", "--no-tags", repo.url, f"refs/heads/{repo.branch}:{ref}")
                    head = git(work, "rev-parse", ref)
                    heads[repo] = head
                    inventories[repo] = inventory(work, repo, head)
                    report["repositories"][repo.name] = {"head": head, "skills": len(inventories[repo])}
                except (OSError, RuntimeError) as exc:
                    failed = True
                    report["repositories"][repo.name] = {"error": str(exc)}
            if failed:
                raise RuntimeError("Inventory incomplete; no reconciliation or pushes attempted")
            plans, report["changes"], report["withheld"] = make_plans(repos, inventories)
            prepared = {}
            checked = set()
            for repo, changes in plans.items():
                if changes:
                    unseen = {path: v for path, v in changes.items() if (path, v.tree) not in checked}
                    verify_transfer(work, unseen)
                    checked.update((path, v.tree) for path, v in unseen.items())
                    prepared[repo] = prepare(work, repo, heads[repo], changes, validator)
            for repo in repos:
                if remote_head(work, repo) != heads[repo]:
                    raise RuntimeError(f"{repo.name}: head changed during planning; rerun")
            for repo in repos:
                expected = prepared.get(repo, heads[repo]) if apply else heads[repo]
                if apply and repo in prepared:
                    git(work, "push", "--porcelain", repo.url, f"{expected}:refs/heads/{repo.branch}")
                    report["repositories"][repo.name]["pushed_head"] = expected
            for repo in repos:
                expected = prepared.get(repo, heads[repo]) if apply else heads[repo]
                observed = remote_head(work, repo)
                report["repositories"][repo.name]["verified_head"] = observed
                if observed != expected:
                    raise RuntimeError(f"{repo.name}: remote head did not match expected commit")
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        report["error"] = str(exc)
        print(json.dumps(report, indent=2))
        return 1
    print(json.dumps(report, indent=2))
    return 2 if report["withheld"] or excluded else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Push and verify fast-forward updates")
    args = parser.parse_args()
    try:
        return run(args.apply)
    except (OSError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
