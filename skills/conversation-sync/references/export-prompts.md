# Export Prompt Templates

Generate one copyable version per adapter by substituting {PROVIDER}.

```
Prepare a ConversationSync export for the authorized account or workspace on **{PROVIDER}**. Use the documented account export or connected history interface when available. Include all accessible standalone, archived, and project conversations, including original messages, roles, timestamps, order, stable identifiers, visible branches, project memberships, project instructions, uploads, project-level files, and recoverable generated outputs. For every discovered project, including projects with no chats, export its exact project-level instructions and any explicitly configured instruction files. Identify each instruction’s project ID, scope, source location, position or precedence, and revision where exposed. Indicate whether instructions are present, confirmed empty, inaccessible, or missing from the export. Return structured data and original file bytes where available. List each unresolved item and the reason it could not be retrieved. State exactly which accounts, workspaces, projects, and history surfaces the export covers. If you can only see the current thread or supplied files, state that boundary and provide the verified full-account export procedure if available. Preserve source text and metadata as supplied. Report missing fields explicitly.
```

The adapter must distinguish the current-thread response from an actual account export.
