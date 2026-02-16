#!/usr/bin/env bash
set -euo pipefail

# Logging helper
log() { echo "[flatten-pages] $*" >&2; }

src="_site/pages"
dst="_site"

# Nothing to do if pages output doesn't exist yet
if [ ! -d "$src" ]; then
  log "No pages directory found at $src, skipping"
  exit 0
fi

log "Starting page flattening from $src to $dst"

# Move directories from /pages to site root,
# but keep /pages/index.html intact.
count=0
for entry in "$src"/*; do
  [ -d "$entry" ] || continue
  name="$(basename "$entry")"
  target="$dst/$name"

  # Replace previous target directory if present.
  if [ -d "$target" ]; then
    log "  Removing existing: $target"
    rm -rf "$target" || {
      log "ERROR: Failed to remove $target"
      exit 1
    }
  fi

  log "  Moving: $name → $target"
  mv "$entry" "$target" || {
    log "ERROR: Failed to move $entry to $target"
    exit 1
  }
  count=$((count + 1))
done

log "✓ Successfully moved $count directories"
