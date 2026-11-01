# Thinking in code

The point of the walk is not a glossary. It is to leave the reader able to simulate the program without looking.

## Before / after

For every block, state two snapshots.

- Before this block runs, these names hold these kinds of value.
- After this block runs, these names changed, or control moved.

If a name is unchanged, do not list it.

## Control flow in spoken English

Use these phrases. Do not decorate them.

- This runs once, when the file is loaded.
- This runs every time the function is called.
- This runs once per item in X.
- This is skipped when Y is empty / false / missing.
- This returns early, so the lines below do not run.
- This raises / throws, so the caller must handle it or the process stops.

## Teach the pattern after the reader has seen it

Wrong — "This is a classic reducer."
Right — "Each pass takes the total so far and the next row and returns a new total. That shape is a reduce."

Same rule for guard clause, factory, middleware, decorator, closure, generator, promise chain, and context manager.

## Names

Keep the source names. If a name hides the job, one sentence of translation, then the original name again.

Example — "`tmp` here is the parsed config, not a throwaway. The rest of this note still calls it `tmp`."

## State versus value

- A value is used and forgotten.
- State lasts — a variable that later blocks read, a file on disk, a row in a store, a mutated list.

Mark state when it appears. Beginners lose the plot when a list is mutated three functions away.

## Recursion, async, and concurrency

Only when the blob uses them.

- Recursion — name the base case and what shrinks.
- Async — name what waits, what continues, and what still runs in between.
- Threads, processes, or locks — name the shared object and who writes it. Do not lecture on memory models the blob does not touch.

## What not to do

- Do not analogize to cooking, trains, or "a restaurant kitchen" unless the user asked for a metaphor.
- Do not say the code is intuitive.
- Do not skip a block because it looks boilerplate. Imports teach dependencies. Empty `except` teaches silence.
- Do not finish with extra exercises unless the user asked to be drilled.
