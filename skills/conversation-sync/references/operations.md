# Operate ConversationSync

The bundled runtime ingests explicit snapshots, stores conversation deadlines in SQLite, pushes an encrypted conversation revision to a verified private GitHub branch, and prepares a private ChatGPT upload package. It supports manual operator runs. Live provider polling, webhook release orchestration, native ChatGPT writes, and automatic installation in Project instructions require separate verified adapters. A public skills release includes code and synthetic fixtures only.

## Prepare an authorized snapshot

Use an official export or selected local export. Normalize it into this envelope without inventing missing source timestamps, conversation IDs, or project settings. Keep source exports in the same private storage boundary. Provider-specific discovery candidates and export prompts are in [the contract](contract.md).

```json
{
  "provider": "example-surface",
  "scope": "synthetic-workspace",
  "projects": [
    {"id": "p1", "instruction_status": "present", "instructions": "Use UTC."}
  ],
  "conversations": [
    {
      "id": "c1",
      "last_activity_at": "2026-01-01T12:00:00.123456+00:00",
      "in_progress": false,
      "project_ids": ["p1"],
      "messages": [{"id": "m1", "role": "user", "content": "Synthetic message."}]
    }
  ]
}
```

Use one assembled record per conversation with all memberships. Keep branches, artifact references and source metadata as additional fields. The runtime preserves these fields. Standalone attachment bytes remain in the authorized source or staging store. Include the original filename, MIME type, size, checksum and private reference in each artifact record when known. Use no signed URLs or credentials in records. Resolve conflicting project settings exports manually. Omit an unverified activity timestamp or use null.

## Read ChatGPT conversation JSON directly

For an authorized ChatGPT export, select the conversation JSON array from the extracted export. Run a private, read-only preview with the operator-confirmed source account or workspace label:

```sh
python3 scripts/conversation_sync.py --db /private/state.db ingest /private/conversations.json --chatgpt-export-scope CONFIRMED-SOURCE --dry-run
```

The importer handles records with a node mapping. It preserves the source graph and orders the selected branch by its parent links. It uses available message times as snapshot evidence, including messages on alternate branches. An absent activity time leaves the revision ineligible. Project mapping, instruction fields, attachment bytes, and other export formats require separate verification or the normalized envelope above.

## Run locally

Run from the skill directory. Use Python 3.11 or later. Install the Python cryptography dependency where supported for GitHub encryption. Point state and output paths to a private directory. Keep the generated key in an approved secret store and retain it for recovery. Configure a GitHub credential with write access to the approved private repository and read access for verification.

```sh
python3 scripts/conversation_sync.py --db /private/state.db ingest /private/export.json --dry-run
python3 scripts/conversation_sync.py --db /private/state.db ingest /private/export.json
python3 scripts/conversation_sync.py --db /private/state.db status
python3 scripts/conversation_sync.py --db /private/state.db stage-chatgpt REVISION --authorize-snapshot --workspace RECEIVER --output /private/chatgpt-upload.json
python3 scripts/conversation_sync.py --db /private/state.db push-github REVISION --authorize-snapshot --repository OWNER/PRIVATE-REPO --repository-id ID --branch BRANCH
```

Set `CONVERSATION_SYNC_GITHUB_TOKEN` and `CONVERSATION_SYNC_KEY` via the runtime's secret configuration. The key must be a base64-encoded 32-byte key. Keep destination IDs consistent across attempts. The encrypted file format is three ASCII bytes CS1, a 12-byte nonce, and AES-256-GCM ciphertext plus its authentication tag. Associated data is canonical JSON encoding of the repository ID, branch, and revision in an array. The verified branch head in the receipt is the immutable ref used for file read-back. This adapter caps encrypted payloads at 900,000 bytes for read-back. Larger revisions and unresolved file deliveries remain pending.

Use the ChatGPT package in the intended workspace after confirming the mapped project and matching Project instructions. The package represents manual upload work. OpenAI documents a reference upload for account transfer. Verify any other ChatGPT capability independently. Record any manual upload receipt only after checking the receiving surface.

- [ChatGPT account transfer](https://help.openai.com/en/articles/9106926-transferring-conversations-from-1-chatgpt-account-to-another-chatgpt-account)
- [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
