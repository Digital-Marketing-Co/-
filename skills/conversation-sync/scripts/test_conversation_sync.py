import json
from pathlib import Path
import tempfile
import unittest

from conversation_sync import chatgpt_export, eligible, ingest, instant, ledger, normalize, push, stage_chatgpt


class GitHubFixture:
    repository_id = 42
    branch = "archive"

    def __init__(self):
        self.values = {}
        self.writes = 0

    def verify_destination(self):
        return str(self.writes)

    def read(self, path, ref=None):
        return self.values.get(path)

    def create(self, path, bundle):
        self.writes += 1
        self.values[path] = bundle
        raise TimeoutError("synthetic disconnect after commit")


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.db = ledger(self.root / "state.db")
        self.addCleanup(self.db.close)
        self.activity = "2026-01-01T00:00:00.123456+00:00"
        self.start = instant(self.activity)
        self.due = self.start + 6_000_000_000
        self.snapshot = {"provider": "fixture", "scope": "account", "projects": [
            {"id": "p1", "instruction_status": "present", "instructions": "Use UTC."}],
            "conversations": [{"id": "c1", "last_activity_at": self.activity,
                               "project_ids": ["p1", "p1"],
                               "messages": [{"text": "Private synthetic text"}]}]}
        self.projects, self.rows = normalize(self.snapshot, self.due)
        self.revision = next(iter(self.rows))[0]

    def test_boundary_and_manual_package(self):
        self.assertEqual(ingest(self.db, self.projects, self.rows)["inserted"], 1)
        with self.assertRaises(ValueError):
            eligible(self.db, self.revision, self.due - 1)
        output = self.root / "upload.json"
        result = stage_chatgpt(self.db, self.revision, self.due, "receiver", output)
        self.assertEqual(result["status"], "upload_required")
        content = json.loads(output.read_bytes())
        self.assertEqual(content["projects"][0]["record"]["instructions"], "Use UTC.")
        self.assertEqual(len(content["projects"]), 1)
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_verified_push_after_timeout_reuses_ciphertext(self):
        ingest(self.db, self.projects, self.rows)
        github = GitHubFixture()
        first = push(self.db, self.revision, self.due, github, bytes(32))
        second = push(self.db, self.revision, self.due, github, bytes(32))
        self.assertEqual(first["verified_branch_head"], "1")
        self.assertEqual(first["ciphertext_sha256"], second["ciphertext_sha256"])
        self.assertEqual(github.writes, 1)
        self.assertNotIn(b"Private synthetic text", next(iter(github.values.values())))

    def test_replay_and_out_of_order_record(self):
        ingest(self.db, self.projects, self.rows)
        self.assertEqual(ingest(self.db, self.projects, self.rows)["unchanged"], 1)
        self.snapshot["conversations"][0]["last_activity_at"] = "2025-12-31T23:59:59+00:00"
        self.snapshot["conversations"][0]["messages"] = []
        projects, rows = normalize(self.snapshot, self.due)
        self.assertEqual(ingest(self.db, projects, rows)["conflict"], 1)
        self.assertEqual(eligible(self.db, self.revision, self.due)["id"], self.revision)

    def test_chatgpt_export_preserves_alternate_branch(self):
        records = [{"id": "original", "current_node": "second", "mapping": {
            "first": {"parent": None, "message": {"id": "first", "create_time": 1}},
            "second": {"parent": "first", "message": {"id": "second", "create_time": 2}},
            "alternate": {"parent": "first", "message": {"id": "alternate", "create_time": 3}},
        }}]
        record = chatgpt_export(records, "scope")["conversations"][0]
        self.assertEqual([message["id"] for message in record["messages"]], ["first", "second"])
        self.assertEqual(record["last_activity_at"], "1970-01-01T00:00:03+00:00")
        self.assertEqual(record["source_record"], records[0])
        self.assertEqual(record["project_ids"], [])

    def test_chatgpt_export_rejects_cycle_and_preserves_unknown_clock(self):
        record = {"id": "original", "current_node": "first", "mapping": {
            "first": {"parent": "first", "message": {"id": "first"}},
        }}
        with self.assertRaises(ValueError):
            chatgpt_export([record], "scope")
        record["mapping"]["first"]["parent"] = None
        result = chatgpt_export([record], "scope")["conversations"][0]
        self.assertIsNone(result["last_activity_at"])

    def test_in_progress_blocks_write(self):
        self.snapshot["conversations"][0]["in_progress"] = True
        projects, rows = normalize(self.snapshot, self.due)
        ingest(self.db, projects, rows)
        with self.assertRaises(ValueError):
            eligible(self.db, next(iter(rows))[0], self.due)


if __name__ == "__main__":
    unittest.main()
