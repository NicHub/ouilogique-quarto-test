#!/usr/bin/env python3

"""
Post-processing cleanup script.

This script is intentionally simple and can be extended over time by adding
new replacement rules in REPLACEMENTS.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

# Add future cleanup rules here.
REPLACEMENTS: list[tuple[str, str]] = [
    # ('const icon = "";', 'const icon = "😎";'),
    ('', '😎'),
    ('alt=""', 'alt="image"'),
]

# Limit processing to text-oriented files.
ALLOWED_SUFFIXES = {".html", ".js", ".css", ".xml", ".txt"}


def iter_target_files(paths: list[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in ALLOWED_SUFFIXES:
                yield path
            continue

        if path.is_dir():
            for file_path in path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in ALLOWED_SUFFIXES:
                    yield file_path


def apply_cleanup(file_path: Path) -> int:
    content = file_path.read_text(encoding="utf-8")
    updated = content
    replacements_count = 0

    for source, target in REPLACEMENTS:
        occurrences = updated.count(source)
        if occurrences:
            updated = updated.replace(source, target)
            replacements_count += occurrences

    if updated != content:
        file_path.write_text(updated, encoding="utf-8")

    return replacements_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Run post-processing cleanup replacements.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["_site"],
        help="Files or directories to process (default: _site).",
    )
    args = parser.parse_args()

    targets = [Path(p) for p in args.paths]
    files_changed = 0
    total_replacements = 0

    for file_path in iter_target_files(targets):
        count = apply_cleanup(file_path)
        if count > 0:
            files_changed += 1
            total_replacements += count
            print(f"updated: {file_path} ({count} replacement(s))")

    print(
        f"cleanup done: {total_replacements} replacement(s) across {files_changed} file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
