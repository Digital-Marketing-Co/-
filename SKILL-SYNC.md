# Skill sync contract

Canonical repository: https://github.com/Digital-Marketing-Co/-/
Branch: main
Skill root: skills/<name>/SKILL.md
Ledger: skills/ledger/latest.md

This file is the shared contract for Grok and ChatGPT. Neither host is the source of truth. The default branch of this repository is.

## What counts as an update

Gather updates from these places, in this order:

1. A commit on main that touches skills/<name>/.
2. The live Grok skill tree, when a SKILL.md, reference, or script is newer than the committed copy.
3. A ChatGPT or Codex edit that was committed back to this repository.
4. skills/ledger/latest.md, which names the skill, direction, and short hash.

Do not treat a chat transcript as an update until its skill files are committed here.

## Direction

- If the repository commit is newer and the skill files are complete, both hosts use the repository copy.
- If the installed copy has a verified newer behavior, commit that copy here first, then both hosts use the new commit.
- A byte difference alone does not decide direction. Use commit time, ledger notes, and whether references and scripts moved with the SKILL.md.
- Bundled host skills (docx, pdf, xlsx, pptx, ffmpeg) stay on the host. Do not overwrite them from this repository.

## Grok

On every skill invocation, read skills/<name>/SKILL.md from this repository before using a cached copy. After editing a skill, commit the full skill directory to main and append a row to skills/ledger/latest.md.

A Grok automation watches pushes to main. A second automation runs every weekday and pushes any Grok-only skill text that is not yet committed.

## ChatGPT and Codex

ChatGPT Skills does not watch GitHub. Codex does, if this repository is connected.

Optimal path:

1. Connect GitHub in Codex and open Digital-Marketing-Co/-.
2. Keep AGENTS.md as the router. Codex reads it at session start.
3. At the start of any skill task, run the prompt in skills/skill-sync/CHATGPT-PROMPT.md.
4. After a ChatGPT skill edit, commit the same skill directory here. Do not keep a private zip as the only copy.
5. Re-upload a skill zip only when skills/ledger/latest.md lists that skill as changed. Zip the skill folder, not the repository.

## Installer alias

Digital-Marketing-Co/agent-skills is the private installer name for hosts that expect an agent-skills repository. This hyphen repository remains the corpus the user named. When the two diverge, this repository wins until a commit copies the same tree into agent-skills.


## Negative word ban

Every project instruction and every skill output must refuse the banned tokens in skills/negative/references/blocklist.md. Run /negative as the last step of every skill, before chat, a file, a caption, a filename, or alt text is delivered. Exit 1 blocks delivery. Rewrite hits and re-scan until CLEAN. Verbatim user source and the blocklist file itself are the only carve-outs. Bundled host skills docx, pdf, xlsx, pptx, and ffmpeg stay on the host.
