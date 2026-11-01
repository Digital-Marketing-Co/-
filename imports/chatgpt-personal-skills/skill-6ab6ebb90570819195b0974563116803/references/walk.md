# Block walk

Cut the locked source into blocks. Teach one block at a time in file order.

## What a block is

A block is the smallest stretch of source that does one job a reader can name.

Usual cuts

1. Shebang, encoding, or file header
2. Imports / includes / use / require
3. Module-level constants, types, and configuration
4. One function, method, or class at a time
5. Inside a long function — one paragraph of statements that share a job (parse, guard, transform, write, return)
6. The entry point (`main`, `if __name__`, request handler, `window.onload`)
7. Dead or commented-out code, called out as such

Do not cut on every line. Do not merge two functions because they "feel related."

## What each block must answer

After the excerpt, answer all five. If an answer is "nothing," say that.

- What does this block do?
- What does it read (arguments, globals, files, prior locals)?
- What does it write (return value, mutated object, I/O, new binding)?
- When does it run (once at import, once per call, per item, only on a branch)?
- Why is it here and not later or earlier?

## Excerpt rules

- Fence with the language tag of the lock file.
- Quote the block as given. Do not reindent to "fix" it.
- If the block is longer than about 25 lines and is repetitive, quote the first distinctive stretch and note how many similar lines follow.
- Never paste the entire blob again after the lock.

## Language cues

Infer language from the fence, filename, shebang, or obvious syntax. State the inference once in `scope.md` and in the What-it-does paragraph. If two languages are plausible, pick the stronger cue and say the other remains possible.

## Fragments and diffs

- A function with no callers — teach the function. Do not invent a caller.
- A unified diff — walk added lines as the new behavior and mention removed lines only when they change the mental model.
- A screenshot transcript or OCR — teach the visible text and mark uncertain tokens.

## Order

Top to bottom of the file the user gave. If they pasted two files, finish the first file, then the second. Do not interleave.
