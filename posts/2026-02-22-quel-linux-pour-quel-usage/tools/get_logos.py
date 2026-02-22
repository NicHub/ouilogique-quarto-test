#!/usr/bin/env python3
"""Download distro logos listed in linuxes.yaml into an images directory."""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "distro"


def extension_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    filename = Path(urllib.parse.unquote(parsed.path)).name
    ext = Path(filename).suffix.lower()
    if ext in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return ext
    return ".img"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        raise ValueError("YAML root must be a list of distributions")
    return data


def download_with_retries(
    url: str,
    destination: Path,
    timeout: int = 30,
    retries: int = 5,
    backoff_base: float = 1.5,
) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "logo-downloader/1.0"})
    last_exc = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read()
            destination.write_bytes(content)
            return
        except Exception as exc:
            last_exc = exc
            if attempt >= retries:
                break
            sleep_s = backoff_base**attempt
            time.sleep(sleep_s)
    if last_exc:
        raise last_exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Download distro logos from linuxes.yaml")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force download even if the file already exists",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between each distro download attempt",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=5,
        help="Number of retries per logo on network/rate-limit errors",
    )
    args = parser.parse_args()

    yaml_path = Path("linuxes.yaml")
    out_dir = Path("images")

    if not yaml_path.exists():
        print(f"ERROR: YAML file not found: {yaml_path}", file=sys.stderr)
        return 1

    try:
        distros = load_yaml(yaml_path)
    except Exception as exc:
        print(f"ERROR: Failed to load YAML: {exc}", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    failed = 0

    for distro in distros:
        name = distro.get("name")
        logo_url = distro.get("url-logo-dist")
        if not name or not logo_url:
            skipped += 1
            continue

        filename = f"{slugify(str(name))}{extension_from_url(str(logo_url))}"
        destination = out_dir / filename

        if destination.exists() and not args.force:
            print(f"SKIP  {name}: already exists ({destination})")
            skipped += 1
            continue

        try:
            download_with_retries(
                str(logo_url),
                destination,
                timeout=args.timeout,
                retries=args.retries,
            )
            print(f"OK    {name}: {destination}")
            downloaded += 1
        except Exception as exc:
            print(f"FAIL  {name}: {logo_url} ({exc})", file=sys.stderr)
            failed += 1
        finally:
            time.sleep(max(args.delay, 0.0))

    print(f"Summary: downloaded={downloaded} skipped={skipped} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
