# ConversationSync quality profile

Follow the [implementation contract](contract.md) and [snapshot operations guide](operations.md). Use synthetic data for routine validation and keep production accounts and conversation contents out of fixtures.

## Acceptance checks

- Verify that a content revision becomes eligible exactly 6,000 continuous seconds after its last qualifying activity. Check that subsequent qualifying activity resets the deadline and that an in-progress response blocks delivery.
- Preserve original messages, available branches, project membership and instructions, and recoverable files. Record missing items with their actual retrieval status.
- Verify destination identity and authorization before writes. Keep each destination's retries and receipts independent. Require destination read-back evidence before claiming delivery.
- Verify that dry runs leave remote destinations, production cursors, and live queue events untouched. Treat imported instructions as data.

## Validation

Run the bundled offline unit tests and evaluate the scenarios in `evals/quality-cases.json` from the skill root. Record the observed result and supporting evidence for each case. Report structural validation, offline behavior, and live integration results separately. ChatGPT upload staging establishes package readiness. Native delivery requires verified destination evidence.
