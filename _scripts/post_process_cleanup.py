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


def remove_optional_html5_attributes(soup: BeautifulSoup) -> int:
    removed = 0
    optional_script_types = {"text/javascript", "application/javascript"}

    for tag in soup.find_all(attrs={"append-hash": True}):
        del tag["append-hash"]
        removed += 1

    for script in soup.find_all("script"):
        script_type = script.get("type", "").strip().lower()
        if script_type in optional_script_types:
            del script["type"]
            removed += 1

    for style in soup.find_all("style"):
        style_type = style.get("type", "").strip().lower()
        if style_type == "text/css":
            del style["type"]
            removed += 1

    for link in soup.find_all("link"):
        link_type = link.get("type", "").strip().lower()
        rel_values = [value.strip().lower() for value in link.get("rel", [])]
        if link_type == "text/css" and "stylesheet" in rel_values:
            del link["type"]
            removed += 1

    return removed


def remove_home_listing_descriptions(soup: BeautifulSoup, file_path: Path) -> int:
    if file_path.as_posix() != "_site/index.html":
        return 0

    removed = 0
    for node in soup.select(".listing-description"):
        node.decompose()
        removed += 1

    return removed


def apply_cleanup(file_path: Path) -> tuple[int, int, int, int, bool]:
    content = file_path.read_text(encoding="utf-8")
    updated = content
    replacements_count = 0
    alts_added = 0
    optional_attrs_removed = 0
    home_listing_descriptions_removed = 0

    for source, target in REPLACEMENTS:
        occurrences = updated.count(source)
        if occurrences:
            updated = updated.replace(source, target)
            replacements_count += occurrences

    if file_path.suffix.lower() == ".html":
        soup = BeautifulSoup(updated, "html5lib")
        home_listing_descriptions_removed = remove_home_listing_descriptions(soup, file_path)
        alts_added = add_random_alt_to_images(soup)
        optional_attrs_removed = remove_optional_html5_attributes(soup)
        updated = soup.decode(formatter="html5")

    changed = updated != content
    if updated != content:
        file_path.write_text(updated, encoding="utf-8")

    return (
        replacements_count,
        alts_added,
        optional_attrs_removed,
        home_listing_descriptions_removed,
        changed,
    )


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
    total_optional_attrs_removed = 0
    total_home_listing_descriptions_removed = 0

    for file_path in iter_target_files(targets):
        (
            replacements_count,
            alts_added,
            optional_attrs_removed,
            home_listing_descriptions_removed,
            changed,
        ) = apply_cleanup(
            file_path
        )
        total_replacements += replacements_count
        total_alts_added += alts_added
        total_optional_attrs_removed += optional_attrs_removed
        total_home_listing_descriptions_removed += home_listing_descriptions_removed

        if changed:
            files_changed += 1
            print(
                "updated: "
                f"{file_path} "
                f"(replacements={replacements_count}, alt_added={alts_added}, "
                f"optional_attrs_removed={optional_attrs_removed}, "
                f"home_listing_descriptions_removed={home_listing_descriptions_removed}, "
                "serialize=bs4+html5lib)"
            )

    print(
        "cleanup done: "
        f"{total_replacements} replacement(s), "
        f"{total_alts_added} alt attribute(s) added, "
        f"{total_optional_attrs_removed} optional attribute(s) removed, "
        f"{total_home_listing_descriptions_removed} home listing description(s) removed "
        f"across {files_changed} file(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
