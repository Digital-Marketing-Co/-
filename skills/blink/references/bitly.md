# Bitly keyword workflow

The helper defaults to local mnemonic proposals. It makes no title-fetch or public availability claim. A 404, blocked probe, or timeout cannot reserve a keyword. Confirm creation with the authenticated API, then verify the actual redirect separately.

Use `scripts/blink.py URL --keyword WORD --create` only when link creation is part of the user's requested task. Credentials come from `BITLY_ACCESS_TOKEN` and `BITLY_GROUP_GUID`, never command-line token arguments or printed logs. Without credentials return clearly unverified candidates. Custom keyword access depends on account capability and can fail. Avoid automatic retries after ambiguous writes.

The helper uses POST /v4/bitlinks with long_url, domain, keyword, and group_guid, and verifies returned destination and requested keyword. See https://dev.bitly.com/api-reference/ (checked 2026-10-10). Live creation and redirect verification require separate execution evidence; offline unit fixtures do not prove either.
