#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver) that pages changed.

Bing's index also feeds ChatGPT search, Copilot and DuckDuckGo, so a ping after
a deploy gets new or edited pages picked up in hours instead of weeks.

Usage (after GitHub Pages has finished deploying):
    python3 tools/indexnow.py            # every URL in sitemap.xml
    python3 tools/indexnow.py URL [URL]  # only these URLs

The key is public by design: it is served at https://heybrahim.com/<KEY>.txt
to prove we own the host. Keep that file at the repo root.
"""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "heybrahim.com"
KEY = "e163ae94f3a76216d86baae9ec74bcd2"
ROOT = Path(__file__).resolve().parent.parent
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def sitemap_urls():
    tree = ET.parse(ROOT / "sitemap.xml")
    return [loc.text.strip() for loc in tree.findall(".//sm:loc", SITEMAP_NS)]


def main():
    urls = sys.argv[1:] or sitemap_urls()
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls,
    }
    # curl, not urllib: python.org builds on macOS often lack CA certificates.
    result = subprocess.run(
        [
            "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "30",
            "-X", "POST", "https://api.indexnow.org/indexnow",
            "-H", "Content-Type: application/json; charset=utf-8",
            "--data-binary", json.dumps(payload),
        ],
        capture_output=True, text=True, check=True,
    )
    status = result.stdout.strip()
    # 200 = accepted, 202 = accepted, key validation pending
    print(f"IndexNow {status}: submitted {len(urls)} URL(s)")
    for url in urls:
        print(f"  {url}")
    if status not in ("200", "202"):
        sys.exit(1)


if __name__ == "__main__":
    main()
