#!/usr/bin/env python3
import yaml


with open("linuxes.yaml", "r", encoding="utf-8") as f:
    distros = yaml.safe_load(f)

print('<div class="render_linuxes">')
for distro in distros:
    name = distro["name"]
    url_logo = distro.get("url-logo")

    print(f"- {name}")
    if url_logo:
        print(f"  - logo: ![{name}]({url_logo}){{.logo}}")

    for key, value in distro.items():
        if key in {"name", "url-logo-dist", "url-logo"}:
            continue
        elif key == "urls":
            urls = value if isinstance(value, list) else [value]
            print("  - urls:")
            for url in urls:
                print(f"    - [{url}]({url})")
        else:
            print(f"  - {key}: {value}")
print('</div>')
