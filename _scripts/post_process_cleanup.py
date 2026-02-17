#!/usr/bin/env python3

"""
Post-processing cleanup script.

This script is intentionally simple and can be extended over time by adding
new replacement rules in REPLACEMENTS.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

# Add future cleanup rules here.
REPLACEMENTS: list[tuple[str, str]] = [
    # ('const icon = "";', 'const icon = "😎";'),
    ("", "😎"),
    ('alt=""', 'alt="image"'),
]

# Limit processing to text-oriented files.
ALLOWED_SUFFIXES = {".html", ".js", ".css", ".xml", ".txt"}
ALT_CHOICES = [
    "image",
]


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


def add_random_alt_to_images(soup: BeautifulSoup) -> int:
    added = 0
    for img in soup.find_all("img"):
        if not img.has_attr("alt"):
            img["alt"] = random.choice(ALT_CHOICES)
            added += 1
    return added


def apply_cleanup(file_path: Path) -> tuple[int, int, bool]:
    content = file_path.read_text(encoding="utf-8")
    updated = content
    replacements_count = 0
    alts_added = 0

    for source, target in REPLACEMENTS:
        occurrences = updated.count(source)
        if occurrences:
            updated = updated.replace(source, target)
            replacements_count += occurrences

    if file_path.suffix.lower() == ".html":
        soup = BeautifulSoup(updated, "html.parser")
        alts_added = add_random_alt_to_images(soup)
        updated = soup.prettify(formatter="minimal")

    changed = updated != content
    if updated != content:
        file_path.write_text(updated, encoding="utf-8")

    return replacements_count, alts_added, changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run post-processing cleanup replacements."
    )
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
    total_alts_added = 0

    for file_path in iter_target_files(targets):
        replacements_count, alts_added, changed = apply_cleanup(file_path)
        total_replacements += replacements_count
        total_alts_added += alts_added

        if changed:
            files_changed += 1
            print(
                "updated: "
                f"{file_path} "
                f"(replacements={replacements_count}, alt_added={alts_added}, "
                "pretty_print=bs4)"
            )

    print(
        "cleanup done: "
        f"{total_replacements} replacement(s), "
        f"{total_alts_added} alt attribute(s) added "
        f"across {files_changed} file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
