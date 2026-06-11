#!/usr/bin/env python3
"""One-off utility: regenerate the CollectionPage JSON-LD in pages/learning.html
from assets/data/learning-data.json.

Embeds the 30 most recent certificates as ListItem -> Course entries and keeps
numberOfItems in sync with the dataset total. Run from the repo root:

    python assets/js/generate-learning-schema.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "assets" / "data" / "learning-data.json"
PAGE = ROOT / "pages" / "learning.html"
TOP_N = 30
SITE = "https://brbousnguar.github.io"


def build_schema(data):
    certs = sorted(
        data["certificates"],
        key=lambda c: c.get("date") or "",
        reverse=True,
    )

    items = []
    seen = set()
    for cert in certs:
        key = (cert["title"], cert.get("date"))
        if key in seen:
            continue
        seen.add(key)
        item = {
            "@type": "Course",
            "name": cert["title"],
            "provider": {
                "@type": "Organization",
                "name": cert.get("provider") or "LinkedIn Learning",
            },
            "datePublished": cert.get("date") or "",
        }
        if cert.get("duration"):
            item["timeRequired"] = cert["duration"]
        if cert.get("skills"):
            item["about"] = cert["skills"]
        items.append({
            "@type": "ListItem",
            "position": len(items) + 1,
            "item": item,
        })
        if len(items) == TOP_N:
            break

    total = data["metadata"]["total"]
    domains = data["metadata"]["domains"]
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Continuous Learning & Certifications - Brahim Bousnguar",
        "description": (
            f"{total} LinkedIn Learning certificates across {domains} technology "
            "domains including AI, Programming, Cloud, DevOps, and APIs"
        ),
        "url": f"{SITE}/pages/learning.html",
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": total,
            "itemListElement": items,
        },
        "about": {
            "@type": "Person",
            "name": "Brahim Bousnguar",
            "jobTitle": "Senior E-Commerce Integration Consultant",
        },
    }


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    schema = build_schema(data)
    block = json.dumps(schema, indent=2, ensure_ascii=False)
    # Match the page's 2-space base indentation inside the <script> tag
    block = "\n".join("  " + line for line in block.splitlines())

    html = PAGE.read_text(encoding="utf-8")
    # Replace only the JSON-LD block that contains the CollectionPage type;
    # [^<] guards keep the match inside a single <script> element.
    pattern = re.compile(
        r'<script type="application/ld\+json">(?:(?!</script>).)*?"@type": "CollectionPage"(?:(?!</script>).)*?</script>',
        re.DOTALL,
    )
    if not pattern.search(html):
        raise SystemExit("CollectionPage JSON-LD block not found in learning.html")

    replacement = '<script type="application/ld+json">\n' + block + "\n  </script>"
    html = pattern.sub(lambda m: replacement, html, count=1)
    with open(PAGE, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print(f"Updated {PAGE.relative_to(ROOT)}: numberOfItems={data['metadata']['total']}, "
          f"embedded top {TOP_N} certificates")


if __name__ == "__main__":
    main()
