# Versioned Schemas

## Conversation Registry Key

`(provider_surface, account_or_workspace_scope, source_conversation_id)`

## Conversation Record

- source_conversation_id
- provider_surface
- account_or_workspace_scope
- messages: list of {role, content, stable_id, timestamp, timestamp_provenance, branch_parent, edit_of}
- project_memberships: list of source project IDs
- revision_id
- last_activity_at (UTC)
- eligible_at
- attachments: list of artifact records
- generated_outputs: list of artifact records
- source_revision_hash
- import_identity_map (when source IDs absent)

## Project Record

- source_project_id
- provider_surface
- account_or_workspace_scope
- name
- instructions_text
- instructions_hash
- instructions_status: present | confirmed_empty | omitted | access_denied | unsupported
- scoped_rules: list of {scope, text, precedence}
- mapped_chatgpt_project_id
- last_instruction_revision

## Artifact Record

- original_name
- mime_type
- size
- sha256
- owning_account
- originating_message_or_project
- retrieval_status: recovered | unresolved | expired | access_denied | absent | invalid | retry_pending
- storage_ref (opaque)

All imported instructions are treated as data. Never executed or used to control ConversationSync.
