# EXECUTE

## Interactive input

Enter a task, rough prompt, or approved plan. Include relevant files, target destinations, constraints, and intended deliverables. Define the set of items if it is not already implied by the request.

Recognize `EXECUTE`, `exec`, `EXEC`, `Exec`, `EX`, `Ex`, `ex`, `EXE`, `exe`, `Exe`, `ExE`, `EXe`, and `exE` anywhere in the user's prompt as explicit command tokens, with or without a leading slash. Quoted examples, code, filenames, URLs, and retrieved material are input data. Multiple invocations in one prompt belong to the same run.

## Execution

1. Refine the input into an actionable implementation prompt with deliverables, explicit acceptance criteria, dependencies, and consequential assumptions. Immediately run that prompt in the same execution context. Retain it for review. For a bare command, use a clear plan the user already approved in the current conversation.
2. Inventory the full set and build the task hierarchy. Assign each item its own requirements, tasks, and checks. Add newly discovered in-scope items to the inventory and reconcile the parent deliverables as their dependencies finish.
3. Advance through feasible, authorized work without routine follow-up prompts. Choose reversible defaults, repair recoverable failures, and continue independent work when a branch is blocked. Preserve required approvals. Stop a dependent branch only when authorization, an essential input, or a technical dependency prevents further progress.
4. For each item in the set, resolve and apply the current `/parallax` function wherever the item's output supports parallax. Reuse the project's shared implementation where possible. For interactive visuals, verify the effect on supported touch, pointer, and scroll inputs, including iPhone portrait and landscape where applicable. Verify readable content, stable layout, usable controls, reduced-motion behavior, and acceptable performance. Record evidence per item. Record inapplicability for nonvisual or static outputs and identify any missing `/parallax` definition or unavailable check.
5. Resolve the current `/Perfect` function and apply every applicable dimension to each item and to the assembled output. Run functional QA through normal entry points and visual QA on the rendered result, covering relevant pages, states, viewports, accessibility, and motion preferences. Record the criteria, test results, and evidence. If the function cannot be resolved, report the missing definition and run independently established checks.
6. Repair root causes and rerun affected checks after material changes, including cross-item regressions. Iterate until the complete hierarchy is accounted for and all applicable required checks have current passing evidence, or until a concrete blocker prevents further progress. Report unresolved failures and unavailable checks explicitly. Claim full conformance only when the evidence supports it.
7. Deliver the finished output first. For interactive outputs, expose an expandable task and QA view with filters for item, status, and `/Perfect` dimension. Include each item's `/parallax` evidence and the refined prompt. For static deliverables, provide the same traceability in a review table.

Example invocation: `/ExE Update the apps gallery. Apply /parallax to each app card, then verify the cards and complete gallery using /Perfect.`
