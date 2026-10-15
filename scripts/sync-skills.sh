#!/usr/bin/env bash
# Synchronize canonical skills while retaining backups of replaced local files.
set -euo pipefail
REPO_URL="${SKILLS_REPO_URL:-https://github.com/Digital-Marketing-Co/-.git}"
CACHE_DIR="${SKILLS_CACHE_DIR:-$HOME/.cache/dmc-skills-repo}"
TARGET_DIR="${SKILLS_TARGET_DIR:-$HOME/.local/share/dmc-skills}"
BACKUP_DIR="${SKILLS_BACKUP_DIR:-$HOME/.local/share/dmc-skills-backups/$(date -u +%Y%m%dT%H%M%SZ)}"
if [ ! -d "$CACHE_DIR/.git" ]; then
  git clone --filter=blob:none "$REPO_URL" "$CACHE_DIR"
fi
git -C "$CACHE_DIR" fetch --prune origin main
git -C "$CACHE_DIR" checkout -B main origin/main
test -d "$CACHE_DIR/skills" || { echo "Missing upstream skills directory"; exit 1; }
mkdir -p "$TARGET_DIR" "$BACKUP_DIR"
# Mirror upstream versions; preserve overwritten customizations in timestamped backups.
# Never delete local-only skills.
rsync -av --checksum --backup --backup-dir="$BACKUP_DIR" "$CACHE_DIR/skills/" "$TARGET_DIR/"
# Verify every upstream SKILL.md is identical to the synchronized copy.
failed=0
while IFS= read -r -d '' file; do
  rel="${file#"$CACHE_DIR/skills/"}"
  if ! cmp -s "$file" "$TARGET_DIR/$rel"; then
    echo "SYNC MISMATCH: $rel" >&2
    failed=1
  fi
done < <(find "$CACHE_DIR/skills" -type f -name SKILL.md -print0)
if (( failed )); then exit 1; fi
echo "Skill sync verified at commit $(git -C "$CACHE_DIR" rev-parse HEAD)."
echo "Overwritten local files backed up at $BACKUP_DIR"
echo "Local-only files preserved. This does not install skills into ChatGPT's managed runtime."
