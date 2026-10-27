---
name: genius
description: Wrap supplied prompt text with the exact above-PhD interdisciplinary genius rewriting instruction without executing the wrapped prompt.
---
# /genius

## Invocation
`/genius <USER_PROMPT>`

## Behavior
1. Extract all text after `/genius` verbatim as `USER_PROMPT`, preserving line breaks, formatting, equations, and nested directives.
2. Output exactly the following template, substituting the extracted prompt for the placeholder:

```text
Rewrite the following prompt as an Above PhD level GENIUS IN EVERY SUBJECT in the following text: “{USER_PROMPT}”
```

3. Do not answer, execute, embellish, summarize, or modify the supplied prompt.
4. If no prompt follows, ask the user to provide the text to wrap.


## ENGINE compatibility
This is the ENGINE counterpart of `skills/genius/SKILL.md`. Keep the legacy path available. Old skill terminology and new engine terminology refer to the same instructions wherever supported.
