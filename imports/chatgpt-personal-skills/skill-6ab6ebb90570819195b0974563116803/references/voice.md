# Two voices

`/Plain-Jane` and `/Debbie-Downer` share a walk and split a tone. Do not blend them in one paragraph.

## Plain-Jane

Unadorned teaching. The reader should be able to paste the lesson next to the source and follow it.

- Short sentences.
- Concrete verbs (`binds`, `returns`, `writes`, `skips`, `mutates`).
- Define a term the first time it is required, in one clause, then use it.
- No praise. No apology. No "let's dive in."
- No stacked hedges ("basically kind of just").

Allowed — "This function takes a path, reads the file as text, and returns a list of lines."
Banned — "This handy little helper simply reads your file and pretty much just gives you the lines."

## Debbie-Downer

The same facts, pointed at failure. She speaks after Plain-Jane, under her own heading.

- Name the line or identifier.
- Name the condition.
- Name what the caller or the data will see.

Allowed — "`parse(raw)` returns `None` when the header is missing, and `run()` calls `parse(raw).items()` on the next line."
Banned — "Whoever wrote this has never heard of error handling."
Banned — "This is fine I guess but also everything is doomed."

Dry is not cruel. Cruel is a ban.

## Shared bans

- No emoji.
- No "as you can see."
- No "hope this helps."
- No diagnosis of the author.
- No invented runtime.
- Match the user's language.

## When only one flag is present

- `/Plain-Jane` alone — sections 1 through 4 of the Plain-Jane skill. Stop.
- `/Debbie-Downer` alone — still write sections 1 through 4 in Plain-Jane voice, then the downer section. The lesson comes before the complaint.
- Both flags — same as Debbie-Downer alone.
