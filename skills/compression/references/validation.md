# Validation

1. Container — file opens / archive lists.
2. Structure — page count, member count, schema.
3. Content — pixels, PCM, extracted text, SHA-256 of payload.
4. Function — formulas, macros, playability when a checker exists.
5. Round-trip — extract final package, hash, compare to manifest.

Fail any required level → discard candidate → keep original.

Class A requires original_sha256 == roundtrip_sha256.
Class B requires decoded-equality evidence.
Class C requires structure plus application-relevant checks.
