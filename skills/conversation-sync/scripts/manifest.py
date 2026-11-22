#!/usr/bin/env python3
"""Deterministic manifest and SHA-256 helpers for ConversationSync.

Build a stable manifest identity per source revision. Reuse staged encrypted bytes on retry.
"""
import hashlib
import json
from typing import Any, Dict, List

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))

def build_manifest(
    provider_surface: str,
    account_scope: str,
    conversation_id: str,
    revision_id: str,
    messages: List[Dict[str, Any]],
    attachments: List[Dict[str, Any]],
    project_memberships: List[str],
) -> Dict[str, Any]:
    """Deterministic manifest. Sort keys and lists for stability."""
    manifest = {
        "schema_version": "1.0",
        "provider_surface": provider_surface,
        "account_scope": account_scope,
        "conversation_id": conversation_id,
        "revision_id": revision_id,
        "project_memberships": sorted(project_memberships),
        "message_count": len(messages),
        "attachment_count": len(attachments),
        "content_sha256": sha256_text(json.dumps(messages, sort_keys=True, separators=(",", ":"))),
        "attachments": sorted(
            [
                {
                    "name": a.get("original_name", ""),
                    "sha256": a.get("sha256", ""),
                    "size": a.get("size", 0),
                }
                for a in attachments
            ],
            key=lambda x: (x["name"], x["sha256"]),
        ),
    }
    manifest["manifest_sha256"] = sha256_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    return manifest

if __name__ == "__main__":
    m = build_manifest("grok", "user@example.com", "conv-1", "rev-1", [{"role": "user", "content": "hi"}], [], ["proj-a"])
    print(json.dumps(m, indent=2))
