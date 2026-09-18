#!/usr/bin/env python3
"""Build the /notes/ section from Markdown. No dependencies; run from the repo root:

    python3 tools/build_notes.py

Sources are `notes/<slug>.md`, each with a front matter block:

    ---
    title: Hook-style title
    description: One or two sentences; used as meta description and index summary
    date: 2026-09-18
    updated: 2026-10-02        (optional)
    tags: MuleSoft, MCP        (optional, comma-separated)
    project: https://…         (optional, the repo or page the note is about)
    draft: true                (optional; drafts are skipped)
    ---

The `.md` files are published as-is next to the HTML (`/notes/<slug>.md`) so
agents can read the plain text. Writes, all generated — never edit by hand:

    notes/<slug>.html   one page per note (TechArticle JSON-LD, author → #person)
    notes/index.html    the list, newest first
    notes/feed.xml      Atom feed with full content
    sitemap.xml         static pages (with EN/FR alternates) + notes
    llms.txt            the note list between <!-- notes:start/end --> markers
    llms-full.txt       llms.txt + the full Markdown of every note

The Markdown converter covers what notes use: ## / ### headings, paragraphs,
- and 1. lists, > quotes, fenced code, pipe tables, **bold**, *italic*,
`code` and [links](url). Anything fancier: write the HTML inline.
Notes are English-only (#44). After deploying, run tools/indexnow.py.
"""
import html
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://heybrahim.com"
NOTES = ROOT / "notes"
WORDS_PER_MIN = 220

# Static pages for the sitemap: (path, file, French counterpart path or None).
STATIC_PAGES = [
    ("/", "index.html", "/fr/"),
    ("/fr/", "fr/index.html", "/"),
    ("/pages/about.html", "pages/about.html", "/fr/a-propos.html"),
    ("/fr/a-propos.html", "fr/a-propos.html", "/pages/about.html"),
]


# ── Markdown (subset) ───────────────────────────────────────────────────────

def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def inline(text):
    codes = []

    def keep_code(m):
        codes.append(f"<code>{html.escape(m.group(1), quote=False)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)

    def link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith("http") and not url.startswith(SITE)
        attrs = ' target="_blank" rel="noopener noreferrer"' if ext else ""
        return f'<a href="{html.escape(html.unescape(url))}"{attrs}>{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]
    out = ['<div class="note-table"><table>', "<thead><tr>"]
    out += [f'<th scope="col">{inline(c)}</th>' for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def markdown(src):
    lines = src.splitlines()
    out, toc, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            lang = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            label = f' data-lang="{html.escape(lang)}"' if lang else ""
            out.append(f'<pre{label}><code>{html.escape(chr(10).join(code), quote=False)}</code></pre>')
        elif m := re.match(r"(#{2,3}) (.+)", line):
            level, text = len(m.group(1)), inline(m.group(2))
            hid = slugify(text)
            if level == 2:
                toc.append((hid, text))
            out.append(f'<h{level} id="{hid}">{text}</h{level}>')
            i += 1
        elif re.match(r"(-|\d+\.) ", line):
            ordered = line[0].isdigit()
            items = []
            while i < len(lines) and re.match(r"(-|\d+\.) ", lines[i]):
                item = re.sub(r"^(-|\d+\.) ", "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                    item += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{inline(item)}</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
        elif line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> "))
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
        elif line.startswith("|") and i + 1 < len(lines) and re.match(r"\|?\s*:?-", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
        elif line.startswith("<"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(```|#{2,3} |(-|\d+\.) |>|\|)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out), toc


# ── Sources ─────────────────────────────────────────────────────────────────

def load_notes():
    notes = []
    for path in sorted(NOTES.glob("*.md")):
        raw = path.read_text()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m:
            raise SystemExit(f"{path}: missing front matter")
        meta = {}
        for line in m.group(1).splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        if meta.get("draft", "").lower() == "true":
            continue
        for key in ("title", "description", "date"):
            if not meta.get(key):
                raise SystemExit(f"{path}: front matter needs {key}")
        body_md = m.group(2).strip()
        body_html, toc = markdown(body_md)
        words = len(re.findall(r"\w+", body_md))
        notes.append({
            "slug": path.stem,
            "url": f"{SITE}/notes/{path.stem}.html",
            "md_url": f"{SITE}/notes/{path.stem}.md",
            "title": meta["title"],
            "description": meta["description"],
            "date": meta["date"],
            "updated": meta.get("updated") or meta["date"],
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "project": meta.get("project"),
            "minutes": max(1, round(words / WORDS_PER_MIN)),
            "html": body_html,
            "toc": toc,
            "markdown": body_md,
        })
    return sorted(notes, key=lambda n: n["date"], reverse=True)


def site_graph():
    """The #person and #website nodes, taken from the home page so they never drift."""
    home = (ROOT / "index.html").read_text()
    data = json.loads(re.search(r'<script type="application/ld\+json">\n(.*?)\n  </script>', home, re.S).group(1))
    return [n for n in data["@graph"] if n["@type"] in ("Person", "WebSite")]


def contact_block():
    """The English contact band from the About page, with root-absolute links."""
    about = (ROOT / "pages/about.html").read_text()
    block = re.search(r'      <section class="contact".*?</section>\n', about, re.S).group(0)
    return block.replace('href="../', 'href="/')


# ── Templates ───────────────────────────────────────────────────────────────

def human_date(iso):
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %b %Y")


def ld_script(graph):
    body = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return '  <script type="application/ld+json">\n' + "\n".join("  " + l for l in body.splitlines()) + "\n  </script>"


def head(title, description, url, og_type, graph, extra=""):
    t, d = html.escape(title), html.escape(description)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t}</title>
  <meta name="description" content="{d}">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Brahim Bousnguar">
  <meta property="og:locale" content="en_US">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{SITE}/assets/img/og-card.png?v=1">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="Brahim Bousnguar — Senior E-Commerce Integration Consultant: SAP Commerce Cloud, MuleSoft and Salesforce. heybrahim.com">
{extra}
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{SITE}/assets/img/og-card.png?v=1">
  <meta name="twitter:image:alt" content="Brahim Bousnguar — Senior E-Commerce Integration Consultant: SAP Commerce Cloud, MuleSoft and Salesforce. heybrahim.com">

  <meta name="author" content="Brahim Bousnguar">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <link rel="alternate" type="application/atom+xml" title="Notes — Brahim Bousnguar" href="/notes/feed.xml">

  <link rel="icon" href="/favicon.ico?v=2" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png?v=2">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/img/favicon-192.png?v=2">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/apple-touch-icon.png?v=2">
  <meta name="theme-color" content="#fbfaf7">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">

  <!-- JSON-LD: one linked graph; #person comes from index.html via tools/build_notes.py -->
{ld_script(graph)}
</head>
"""


HEADER = """<body>
  <a href="#main-content" class="skip-link">Skip to content</a>

  <header class="site-head">
    <div class="wrap">
      <a href="/" class="brand">
        <span class="brand-mark" aria-hidden="true">BB</span>
        <span>Brahim Bousnguar</span>
      </a>
      <nav class="site-nav" aria-label="Main">
        <a href="/#work">Work</a>
        <a href="/#projects">Projects</a>
        <a href="/#experience">Experience</a>
        <a href="/#stack" class="nav-optional">Stack</a>
        <a href="/pages/about.html">About</a>
        <a href="/notes/" aria-current="page">Notes</a>
        <a href="#contact">Contact</a>
      </nav>
      <nav class="lang-switch" aria-label="Language / Langue">
        <a href="/notes/" hreflang="en" lang="en" aria-current="true" aria-label="English">EN</a>
        <a href="/fr/" hreflang="fr" lang="fr" aria-label="Site en français">FR</a>
      </nav>
    </div>
  </header>

  <main id="main-content">
"""

FOOTER = """  </main>
</body>
</html>
"""


def page_nodes(url, name, description, typ, crumbs, **extra):
    node = {"@type": typ, "@id": url + "#webpage", "url": url, "name": name, "description": description,
            "inLanguage": "en", "isPartOf": {"@id": SITE + "/#website"}, "breadcrumb": {"@id": url + "#breadcrumb"}}
    node.update(extra)
    crumb = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    return [node, crumb]


def note_page(note, graph, contact):
    url = note["url"]
    article = {
        "@type": "TechArticle", "@id": url + "#article", "headline": note["title"], "description": note["description"],
        "datePublished": note["date"], "dateModified": note["updated"], "inLanguage": "en",
        "author": {"@id": SITE + "/#person"}, "publisher": {"@id": SITE + "/#person"},
        "mainEntityOfPage": {"@id": url + "#webpage"}, "image": f"{SITE}/assets/img/og-card.png",
        "keywords": note["tags"], "wordCount": len(re.findall(r"\w+", note["markdown"])),
        "encoding": {"@type": "MediaObject", "contentUrl": note["md_url"], "encodingFormat": "text/markdown"},
    }
    if note["project"]:
        article["about"] = {"@type": "SoftwareSourceCode", "codeRepository": note["project"]}
    nodes = graph + page_nodes(url, note["title"], note["description"], "WebPage",
                               [("Home", SITE + "/"), ("Notes", SITE + "/notes/"), (note["title"], url)],
                               mainEntity={"@id": url + "#article"}) + [article]
    extra = (f'  <meta property="article:published_time" content="{note["date"]}">\n'
             f'  <meta property="article:modified_time" content="{note["updated"]}">\n'
             f'  <meta property="article:author" content="{SITE}/">\n'
             + "".join(f'  <meta property="article:tag" content="{html.escape(t)}">\n' for t in note["tags"])
             + f'  <link rel="alternate" type="text/markdown" href="/notes/{note["slug"]}.md">\n')
    updated = (f' · updated <time datetime="{note["updated"]}">{human_date(note["updated"])}</time>'
               if note["updated"] != note["date"] else "")
    tags = "".join(f"<li>{html.escape(t)}</li>" for t in note["tags"])
    toc = "".join(f'<li><a href="#{hid}">{text}</a></li>' for hid, text in note["toc"])
    return (head(f'{note["title"]} | Brahim Bousnguar', note["description"], url, "article", nodes, extra) + HEADER + f"""
    <article class="note" aria-labelledby="note-title">
      <header class="page-intro note-intro">
        <div class="wrap">
          <p class="eyebrow"><a href="/notes/">Notes</a></p>
          <h1 id="note-title">{html.escape(note["title"])}</h1>
          <p class="note-meta mono">By <a href="/pages/about.html" rel="author">Brahim Bousnguar</a> · <time datetime="{note["date"]}">{human_date(note["date"])}</time>{updated} · {note["minutes"]} min read</p>
        </div>
      </header>

      <div class="wrap">
       <div class="note-layout">
        <aside class="note-aside" aria-label="On this page">
          <p class="note-aside-title mono">On this page</p>
          <ol class="note-toc">{toc}</ol>
          <ul class="note-tags" aria-label="Topics">{tags}</ul>
        </aside>
        <div class="note-body prose">
{note["html"]}
          <p class="note-source mono">Plain text: <a href="/notes/{note["slug"]}.md">{note["slug"]}.md</a> · <a href="/notes/feed.xml">Atom feed</a> · <a href="/notes/">All notes</a></p>
        </div>
       </div>
      </div>
    </article>

""" + contact + FOOTER)


def index_page(notes, graph, contact):
    url = SITE + "/notes/"
    title = "Notes on MuleSoft, SAP Commerce and AI-augmented engineering | Brahim Bousnguar"
    description = ("Technical notes by Brahim Bousnguar on MuleSoft Anypoint, SAP Commerce Cloud, Salesforce integration, "
                   "MCP servers and AI-augmented engineering — problems solved on real projects.")
    blog = {"@type": "Blog", "@id": url + "#blog", "name": "Notes — Brahim Bousnguar", "url": url, "inLanguage": "en",
            "author": {"@id": SITE + "/#person"},
            "blogPost": [{"@type": "TechArticle", "@id": n["url"] + "#article", "headline": n["title"], "url": n["url"],
                          "datePublished": n["date"]} for n in notes]}
    nodes = graph + page_nodes(url, title, description, "CollectionPage", [("Home", SITE + "/"), ("Notes", url)],
                               mainEntity={"@id": url + "#blog"}) + [blog]
    items = "".join(f"""
          <li class="note-row">
            <time class="mono" datetime="{n["date"]}">{human_date(n["date"])}</time>
            <div>
              <h2><a href="/notes/{n["slug"]}.html">{html.escape(n["title"])}</a></h2>
              <p>{html.escape(n["description"])}</p>
              <p class="note-row-meta mono">{" · ".join(html.escape(t) for t in n["tags"])} · {n["minutes"]} min read</p>
            </div>
          </li>""" for n in notes)
    return (head(title, description, url, "website", nodes) + HEADER + f"""
    <section class="page-intro">
      <div class="wrap">
        <p class="eyebrow">Notes</p>
        <h1>Notes from the integration layer.</h1>
        <p class="hero-lede">Stuff I build and figure out. MuleSoft, SAP Commerce, Salesforce, and a lot of AI tooling on the side.</p>
        <p class="note-feed mono"><a href="/notes/feed.xml">Atom feed</a> · written in English</p>
      </div>
    </section>

    <div class="wrap">
      <ol class="note-list">{items}
      </ol>
    </div>

""" + contact + FOOTER)


def feed(notes):
    updated = max(n["updated"] for n in notes) + "T00:00:00Z"
    entries = "".join(f"""
  <entry>
    <title>{html.escape(n["title"])}</title>
    <link rel="alternate" type="text/html" href="{n["url"]}"/>
    <id>{n["url"]}</id>
    <published>{n["date"]}T00:00:00Z</published>
    <updated>{n["updated"]}T00:00:00Z</updated>
    <summary>{html.escape(n["description"])}</summary>
    {"".join(f'<category term="{html.escape(t)}"/>' for t in n["tags"])}
    <content type="html">{html.escape(n["html"])}</content>
  </entry>""" for n in notes)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
  <title>Notes — Brahim Bousnguar</title>
  <subtitle>MuleSoft, SAP Commerce, Salesforce integration and AI-augmented engineering.</subtitle>
  <link rel="self" type="application/atom+xml" href="{SITE}/notes/feed.xml"/>
  <link rel="alternate" type="text/html" href="{SITE}/notes/"/>
  <id>{SITE}/notes/</id>
  <updated>{updated}</updated>
  <author><name>Brahim Bousnguar</name><uri>{SITE}/</uri></author>{entries}
</feed>
"""


def last_commit_date(rel):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or date.today().isoformat()


def sitemap(notes):
    urls = []
    for path, rel, alt in STATIC_PAGES:
        en, fr = (path, alt) if not path.startswith("/fr/") else (alt, path)
        links = (f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>\n'
                 f'    <xhtml:link rel="alternate" hreflang="fr" href="{SITE}{fr}"/>\n'
                 f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{en}"/>\n')
        urls.append(f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{last_commit_date(rel)}</lastmod>\n{links}  </url>")
    urls.append(f"  <url>\n    <loc>{SITE}/notes/</loc>\n    <lastmod>{max(n['updated'] for n in notes)}</lastmod>\n  </url>")
    for n in notes:
        urls.append(f"  <url>\n    <loc>{n['url']}</loc>\n    <lastmod>{n['updated']}</lastmod>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


def update_llms_index(notes):
    """Rewrite the note list between the markers in llms.txt."""
    path = ROOT / "llms.txt"
    lines = "".join(f"- [{n['title']}]({n['url']}) ({n['date']}): {n['description']} Markdown: {n['md_url']}\n" for n in notes)
    text = re.sub(r"<!-- notes:start -->\n.*?<!-- notes:end -->", lambda _: f"<!-- notes:start -->\n{lines}<!-- notes:end -->",
                  path.read_text(), flags=re.S)
    path.write_text(text)


def llms_full(notes):
    base = (ROOT / "llms.txt").read_text().rstrip()
    parts = [base, "\n\n# Notes (full text)\n"]
    for n in notes:
        parts.append(f"\n---\n\n## {n['title']}\n\nURL: {n['url']}\nPublished: {n['date']} · Updated: {n['updated']}\n"
                     f"Topics: {', '.join(n['tags'])}\n\n{n['markdown']}\n")
    return "".join(parts)


def main():
    notes = load_notes()
    if not notes:
        raise SystemExit("no published notes in notes/")
    graph = site_graph()
    contact = contact_block()
    for n in notes:
        (NOTES / f"{n['slug']}.html").write_text(note_page(n, graph, contact))
    (NOTES / "index.html").write_text(index_page(notes, graph, contact))
    (NOTES / "feed.xml").write_text(feed(notes))
    (ROOT / "sitemap.xml").write_text(sitemap(notes))
    update_llms_index(notes)
    (ROOT / "llms-full.txt").write_text(llms_full(notes))
    print(f"built {len(notes)} note(s): " + ", ".join(n["slug"] for n in notes))


if __name__ == "__main__":
    main()
