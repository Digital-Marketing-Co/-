# Canonical skills

Place each skill in `skills/<skill-name>/SKILL.md`.

Run `bash scripts/sync-skills.sh` at environment startup to fetch new skills into `~/.local/share/dmc-skills`. The script preserves existing local files rather than overwriting customizations.

GitHub Actions validates nonempty skill definitions every six hours and on changes. It does **not** install skills into ChatGPT's managed runtime; ChatGPT conversation startup hooks are not exposed through this repository.
