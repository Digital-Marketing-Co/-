#!/usr/bin/env bash
# Pull the latest tracked skills from the canonical GitHub repository.
set -euo pipefail
REPO_URL="${SKILLS_REPO_URL:-https://github.com/Digital-Marketing-Co/-.git}"
CACHE_DIR="${SKILLS_CACHE_DIR:-$HOME/.cache/dmc-skills-repo}"
TARGET_DIR="${SKILLS_TARGET_DIR:-$HOME/.local/share/dmc-skills}"
if [ ! -d "$CACHE_DIR/.git" ]; then
  git clone --filter=blob:none "$REPO_URL" "$CACHE_DIR"
fi
git -C "$CACHE_DIR" fetch --prune origin main
git -C "$CACHE_DIR" checkout -B main origin/main
if [ ! -d "$CACHE_DIR/skills" ]; then
  echo "No skills/ directory upstream; leaving local skills unchanged."
  exit 0
fi
mkdir -p "$TARGET_DIR"
# No --delete: preserve locally customized skills and files.
rsync -av --ignore-existing "$CACHE_DIR/skills/" "$TARGET_DIR/"
echo "New skills copied. Existing local files preserved; review upstream changes manually."
