#!/usr/bin/env python3

"""

Generation of prev/next buttons.

"""

from __future__ import annotations

import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

HREF_PLACEHOLDER_RE = re.compile(r'href="#"')


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
        path_parts = [p for p in parsed.path.split("/") if p]
        if "posts" not in path_parts:
            continue
        posts_idx = path_parts.index("posts")
        post_parts = path_parts[posts_idx + 1 :]
        if not post_parts:
            continue
        rel_post_path = "/".join(post_parts)
        if rel_post_path.endswith("/"):
            rel_post_path += "index.html"
        elif "." not in Path(rel_post_path).name:
            rel_post_path = f"{rel_post_path}/index.html"
        rows.append(rel_post_path)

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
            prev_link = "../../"
        else:
            prev_target = f"posts/{post_names[i - 1]}"
            prev_link = posixpath.relpath(prev_target, current_dir)

        if i == total - 1:
            next_link = "../../"
        else:
            next_target = f"posts/{post_names[i + 1]}"
            next_link = posixpath.relpath(next_target, current_dir)

        links[current] = {"prev": prev_link, "next": next_link}

    return links


def replace_href_placeholders(text: str, prev_link: str, next_link: str) -> str:
    """Replace all href placeholders by alternating prev/next links."""
    i = 0

    def repl(_: re.Match[str]) -> str:
        nonlocal i
        link = prev_link if i % 2 == 0 else next_link
        i += 1
        return f'href="{link}"'

    return HREF_PLACEHOLDER_RE.sub(repl, text)


def inject_prev_next_into_posts(prev_next_links: dict[str, dict[str, str]]) -> None:
    """Inject prev/next links directly in rendered _site post files."""
    for post_path, links in prev_next_links.items():
        html_path = Path("_site/posts") / post_path
        if not html_path.exists():
            continue
        original = html_path.read_text(encoding="utf-8")
        if 'href="#"' not in original:
            continue
        updated = replace_href_placeholders(original, links["prev"], links["next"])
        if updated != original:
            html_path.write_text(updated, encoding="utf-8")


def inject_prev_next_into_home_page(post_names: list[str]) -> None:
    """Inject prev/next links in _site/index.html only.

    Home page behavior:
      - prev -> most recent post
      - next -> oldest post
    """
    if not post_names:
        return

    home_path = Path("_site/index.html")
    if not home_path.exists():
        return

    oldest_target = f"posts/{post_names[0]}"
    newest_target = f"posts/{post_names[-1]}"
    home_dir = posixpath.dirname("index.html")

    prev_link = posixpath.relpath(newest_target, home_dir or ".")
    next_link = posixpath.relpath(oldest_target, home_dir or ".")

    original = home_path.read_text(encoding="utf-8")
    updated = replace_href_placeholders(original, prev_link, next_link)
    updated = re.sub(r">Précédent<", ">Dernier billet<", updated)
    updated = re.sub(r">Suivant<", ">Premier billet<", updated)
    if updated != original:
        home_path.write_text(updated, encoding="utf-8")


def main() -> dict[str, dict[str, str]]:
    post_names = get_post_names()
    prev_next_links = get_prev_next_links(post_names)
    inject_prev_next_into_posts(prev_next_links)
    inject_prev_next_into_home_page(post_names)
    return prev_next_links


if __name__ == "__main__":
    links = main()
    print(f"prev/next links generated for {len(links)} posts")
