#!/usr/bin/env bash
set -euo pipefail

src="_site/pages"
dst="_site"

# Nothing to do if pages output doesn’t exist yet
[ -d "$src" ] || exit 0

# Move directories from /pages to site root,
# but keep /pages/index.html intact.
for entry in "$src"/*; do
  [ -d "$entry" ] || continue
  name="$(basename "$entry")"
  target="$dst/$name"

  # Replace previous target directory if present.
  rm -rf "$target"
  mv "$entry" "$target"
done
