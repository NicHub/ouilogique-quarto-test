#!/usr/bin/env python3
"""Proof of concept for prev/next generation.

Current steps:
1. Read sitemap.xml
2. Keep only post URLs
3. Sort alphabetically
4. Print the result
"""

from __future__ import annotations

import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


def get_post_names() -> list[str]:
    sitemap_path = Path("_site/sitemap.xml")
    if not sitemap_path.exists():
        return []

    try:
        root = ET.parse(sitemap_path).getroot()
    except ET.ParseError:
        return []

    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    loc_nodes = root.findall(".//sm:url/sm:loc", ns)

    if not loc_nodes:
        return []

    urls = [node.text.strip() for node in loc_nodes if node.text]
    post_urls = [url for url in urls if "/posts/" in url]
    post_urls.sort()

    if not post_urls:
        return []

    rows: list[str] = []
    for url in post_urls:
        parsed = urlparse(url)
        rel_path = parsed.path.lstrip("/")
        if rel_path.startswith("posts/"):
            rows.append(rel_path[len("posts/") :])

    return rows


def get_prev_next_links(post_names: list[str]) -> dict[str, dict[str, str]]:
    """Build relative prev/next links for each post path.

    Args:
        post_names: paths like "2014-12-03-foo/index.html".

    Returns:
        Mapping:
          {
            "<post_path>": {"prev": "<relative_url_or_/>", "next": "<relative_url_or_/>"},
            ...
          }
    """
    links: dict[str, dict[str, str]] = {}
    if not post_names:
        return links

    total = len(post_names)
    for i, current in enumerate(post_names):
        current_full = f"posts/{current}"
        current_dir = posixpath.dirname(current_full)

        if i == 0:
            prev_link = "/"
        else:
            prev_target = f"posts/{post_names[i - 1]}"
            prev_link = posixpath.relpath(prev_target, current_dir)

        if i == total - 1:
            next_link = "/"
        else:
            next_target = f"posts/{post_names[i + 1]}"
            next_link = posixpath.relpath(next_target, current_dir)

        links[current] = {"prev": prev_link, "next": next_link}

    return links


def inject_prev_next_into_site(prev_next_links: dict[str, dict[str, str]]) -> None:
    """Inject prev/next links directly in rendered _site post files."""
    for post_path, links in prev_next_links.items():
        html_path = Path("_site/posts") / post_path
        if not html_path.exists():
            continue
        content = html_path.read_text(encoding="utf-8")
        content = re.sub(r'href="#"', f'href="{links["prev"]}"', content, count=1)
        content = re.sub(r'href="#"', f'href="{links["next"]}"', content, count=1)
        html_path.write_text(content, encoding="utf-8")


def main() -> dict[str, dict[str, str]]:
    post_names = get_post_names()
    prev_next_links = get_prev_next_links(post_names)
    inject_prev_next_into_site(prev_next_links)
    return prev_next_links


if __name__ == "__main__":
    print(main())
