#!/usr/bin/env python3
"""Build the generated pages of heybrahim.com from Markdown. No dependencies;
run from the repo root after changing any source:

    python3 tools/build_site.py

Collections (sources sit next to their output; the .md is published as-is):

    notes/<slug>.md          → /notes/<slug>.html            English only (#44)
    projects/<slug>.md       → /projects/<slug>.html         EN, paired with
    fr/projets/<slug>.md     → /fr/projets/<slug>.html       FR by filename (#46)

Front matter, between `---` lines, one `key: value` per line:

    all        title, description, date (YYYY-MM-DD), updated (optional),
               draft: true (optional; skipped)
    notes      tags (comma-separated), project (URL, optional)
    projects   tagline, repo, npm / live (optional URLs), stack, license, status

Also writes, all generated — never edit by hand:

    notes/index.html    the note list, newest first
    notes/feed.xml      Atom feed with full content
    sitemap.xml         static pages + every generated page, with EN/FR alternates
    llms.txt            the lists between <!-- notes:… --> / <!-- projects:… --> markers
    llms-full.txt       llms.txt + the full Markdown of every note and project

Shared pieces come from the hand-written pages so nothing drifts: `#person` and
`#website` from index.html, the contact band from pages/about.html (EN) and
fr/a-propos.html (FR). The Markdown converter covers: ## / ### headings,
paragraphs, - and 1. lists, > quotes, fenced code, pipe tables, **bold**,
*italic*, `code` and [links](url); write raw HTML for anything else.
After deploying, run tools/indexnow.py.
"""
import html
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://heybrahim.com"
WORDS_PER_MIN = 220

# Hand-written pages for the sitemap: (EN path, EN file, FR path, FR file).
STATIC_PAGES = [
    ("/", "index.html", "/fr/", "fr/index.html"),
    ("/pages/about.html", "pages/about.html", "/fr/a-propos.html", "fr/a-propos.html"),
]

LANG = {
    "en": {
        "locale": "en_US", "alt_locale": "fr_FR", "card": "og-card.png",
        "card_alt": "Brahim Bousnguar — Senior E-Commerce Integration Consultant: SAP Commerce Cloud, MuleSoft and Salesforce. heybrahim.com",
        "home": "/", "about": "/pages/about.html", "contact_src": "pages/about.html",
        "skip": "Skip to content", "nav_label": "Main", "home_crumb": "Home",
        "nav": [("work", "/#work", "Work", ""), ("projects", "/#projects", "Projects", ""),
                ("experience", "/#experience", "Experience", ""), ("stack", "/#stack", "Stack", ' class="nav-optional"'),
                ("about", "/pages/about.html", "About", ""), ("notes", "/notes/", "Notes", ""),
                ("contact", "#contact", "Contact", "")],
    },
    "fr": {
        "locale": "fr_FR", "alt_locale": "en_US", "card": "og-card-fr.png",
        "card_alt": "Brahim Bousnguar — Consultant senior en intégration e-commerce : SAP Commerce Cloud, MuleSoft et Salesforce. heybrahim.com",
        "home": "/fr/", "about": "/fr/a-propos.html", "contact_src": "fr/a-propos.html",
        "skip": "Aller au contenu", "nav_label": "Navigation principale", "home_crumb": "Accueil",
        "nav": [("work", "/fr/#work", "Missions", ""), ("projects", "/fr/#projects", "Projets", ""),
                ("experience", "/fr/#experience", "Parcours", ""), ("stack", "/fr/#stack", "Stack", ' class="nav-optional"'),
                ("about", "/fr/a-propos.html", "À propos", ""), ("notes", "/notes/", "Notes", ' hreflang="en"'),
                ("contact", "#contact", "Contact", "")],
    },
}

COLLECTIONS = {
    "notes": {"en": ("notes", "/notes/")},
    "projects": {"en": ("projects", "/projects/"), "fr": ("fr/projets", "/fr/projets/")},
}



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

def parse(path):
    raw = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    for key in ("title", "description", "date"):
        if not meta.get(key):
            raise SystemExit(f"{path}: front matter needs {key}")
    body_md = m.group(2).strip()
    body_html, toc = markdown(body_md)
    return meta, body_md, body_html, toc


def load(collection):
    """Pages of a collection: one dict per (slug, lang), with its counterpart URL."""
    pages = []
    langs = COLLECTIONS[collection]
    for lang, (folder, base) in langs.items():
        for path in sorted((ROOT / folder).glob("*.md")):
            meta, body_md, body_html, toc = parse(path)
            if meta.get("draft", "").lower() == "true":
                continue
            words = len(re.findall(r"\w+", body_md))
            pages.append({
                **meta,
                "collection": collection, "lang": lang, "slug": path.stem,
                "file": f"{folder}/{path.stem}.html",
                "url": f"{SITE}{base}{path.stem}.html",
                "md_path": f"{base}{path.stem}.md",
                "updated": meta.get("updated") or meta["date"],
                "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                "minutes": max(1, round(words / WORDS_PER_MIN)), "words": words,
                "html": body_html, "toc": toc, "markdown": body_md,
            })
    by_key = {(p["slug"], p["lang"]): p for p in pages}
    for p in pages:
        p["alternates"] = {lang: by_key[(p["slug"], lang)]["url"] for lang in langs if (p["slug"], lang) in by_key}
    return sorted(pages, key=lambda p: p["date"], reverse=True)


def site_graph():
    """The #person and #website nodes, taken from the home page so they never drift."""
    home = (ROOT / "index.html").read_text()
    data = json.loads(re.search(r'<script type="application/ld\+json">\n(.*?)\n  </script>', home, re.S).group(1))
    return [n for n in data["@graph"] if n["@type"] in ("Person", "WebSite")]


def contact_block(lang):
    """The contact band from the About page of that language, with root-absolute links."""
    about = (ROOT / LANG[lang]["contact_src"]).read_text()
    block = re.search(r'      <section class="contact".*?</section>\n', about, re.S).group(0)
    return block.replace('href="../', 'href="/')


# ── Templates ───────────────────────────────────────────────────────────────

MONTHS_FR = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


def human_date(iso, lang="en"):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}" if lang == "fr" else d.strftime("%-d %b %Y")


def ld_script(graph):
    body = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return '  <script type="application/ld+json">\n' + "\n".join("  " + l for l in body.splitlines()) + "\n  </script>"


def head(lang, title, description, url, og_type, graph, alternates=None, extra=""):
    L = LANG[lang]
    t, d = html.escape(title), html.escape(description)
    t_text = html.escape(title, quote=False)
    card = f"{SITE}/assets/img/{L['card']}?v=1"
    alt_locale = f'  <meta property="og:locale:alternate" content="{L["alt_locale"]}">\n' if alternates and len(alternates) > 1 else ""
    hreflang = ""
    if alternates and len(alternates) > 1:
        hreflang = "".join(f'  <link rel="alternate" hreflang="{l}" href="{u}">\n' for l, u in alternates.items())
        hreflang += f'  <link rel="alternate" hreflang="x-default" href="{alternates["en"]}">\n'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t_text}</title>
  <meta name="description" content="{d}">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Brahim Bousnguar">
  <meta property="og:locale" content="{L['locale']}">
{alt_locale}  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:image" content="{card}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="{L['card_alt']}">
{extra}
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{card}">
  <meta name="twitter:image:alt" content="{L['card_alt']}">

  <meta name="author" content="Brahim Bousnguar">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">
{hreflang}  <link rel="alternate" type="application/atom+xml" title="Notes — Brahim Bousnguar" href="/notes/feed.xml">

  <link rel="icon" href="/favicon.ico?v=2" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png?v=2">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/img/favicon-192.png?v=2">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/apple-touch-icon.png?v=2">
  <meta name="theme-color" content="#fbfaf7">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">

  <!-- JSON-LD: one linked graph; #person comes from index.html via tools/build_site.py -->
{ld_script(graph)}
</head>
"""


def header(lang, current, switch):
    """switch = {"en": url, "fr": url}; a language without a counterpart links to its home page."""
    L = LANG[lang]
    nav = "".join(
        f'        <a href="{href}"{attrs}{" aria-current=\"page\"" if key == current else ""}>{label}</a>\n'
        for key, href, label, attrs in L["nav"])
    en_url = switch.get("en", LANG["en"]["home"])
    fr_url = switch.get("fr", LANG["fr"]["home"])
    fr_label = "Français" if "fr" in switch else "Site en français"
    en_label = "English" if "en" in switch else "English site"
    cur = lambda l: ' aria-current="true"' if l == lang else ""
    return f"""<body>
  <a href="#main-content" class="skip-link">{L['skip']}</a>

  <header class="site-head">
    <div class="wrap">
      <a href="{L['home']}" class="brand">
        <span class="brand-mark" aria-hidden="true">BB</span>
        <span>Brahim Bousnguar</span>
      </a>
      <nav class="site-nav" aria-label="{L['nav_label']}">
{nav}      </nav>
      <nav class="lang-switch" aria-label="Language / Langue">
        <a href="{en_url}" hreflang="en" lang="en"{cur("en")} aria-label="{en_label}">EN</a>
        <a href="{fr_url}" hreflang="fr" lang="fr"{cur("fr")} aria-label="{fr_label}">FR</a>
      </nav>
    </div>
  </header>

  <main id="main-content">
"""


FOOTER = """  </main>
</body>
</html>
"""


def page_nodes(lang, url, name, description, typ, crumbs, **extra):
    node = {"@type": typ, "@id": url + "#webpage", "url": url, "name": name, "description": description,
            "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"}, "breadcrumb": {"@id": url + "#breadcrumb"}}
    node.update(extra)
    crumb = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    return [node, crumb]


# ── Notes ───────────────────────────────────────────────────────────────────

def note_page(note, graph):
    url = note["url"]
    article = {
        "@type": "TechArticle", "@id": url + "#article", "headline": note["title"], "description": note["description"],
        "datePublished": note["date"], "dateModified": note["updated"], "inLanguage": "en",
        "author": {"@id": SITE + "/#person"}, "publisher": {"@id": SITE + "/#person"},
        "mainEntityOfPage": {"@id": url + "#webpage"}, "image": f"{SITE}/assets/img/og-card.png",
        "keywords": note["tags"], "wordCount": note["words"],
        "encoding": {"@type": "MediaObject", "contentUrl": SITE + note["md_path"], "encodingFormat": "text/markdown"},
    }
    if note.get("project"):
        article["about"] = {"@type": "SoftwareSourceCode", "codeRepository": note["project"]}
    nodes = graph + page_nodes("en", url, note["title"], note["description"], "WebPage",
                               [("Home", SITE + "/"), ("Notes", SITE + "/notes/"), (note["title"], url)],
                               mainEntity={"@id": url + "#article"}) + [article]
    extra = (f'  <meta property="article:published_time" content="{note["date"]}">\n'
             f'  <meta property="article:modified_time" content="{note["updated"]}">\n'
             f'  <meta property="article:author" content="{SITE}/">\n'
             + "".join(f'  <meta property="article:tag" content="{html.escape(t)}">\n' for t in note["tags"])
             + f'  <link rel="alternate" type="text/markdown" href="{note["md_path"]}">\n')
    updated = (f' · updated <time datetime="{note["updated"]}">{human_date(note["updated"])}</time>'
               if note["updated"] != note["date"] else "")
    tags = "".join(f"<li>{html.escape(t)}</li>" for t in note["tags"])
    toc = "".join(f'<li><a href="#{hid}">{text}</a></li>' for hid, text in note["toc"])
    return (head("en", f'{note["title"]} | Brahim Bousnguar', note["description"], url, "article", nodes, extra=extra)
            + header("en", "notes", {"en": "/notes/"}) + f"""
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
          <p class="note-source mono">Plain text: <a href="{note["md_path"]}">{note["slug"]}.md</a> · <a href="/notes/feed.xml">Atom feed</a> · <a href="/notes/">All notes</a></p>
        </div>
       </div>
      </div>
    </article>

""" + contact_block("en") + FOOTER)


def notes_index(notes, graph):
    url = SITE + "/notes/"
    title = "Notes on MuleSoft, SAP Commerce and AI-augmented engineering | Brahim Bousnguar"
    description = ("Technical notes by Brahim Bousnguar on MuleSoft Anypoint, SAP Commerce Cloud, Salesforce integration, "
                   "MCP servers and AI-augmented engineering — problems solved on real projects.")
    blog = {"@type": "Blog", "@id": url + "#blog", "name": "Notes — Brahim Bousnguar", "url": url, "inLanguage": "en",
            "author": {"@id": SITE + "/#person"},
            "blogPost": [{"@type": "TechArticle", "@id": n["url"] + "#article", "headline": n["title"], "url": n["url"],
                          "datePublished": n["date"]} for n in notes]}
    nodes = graph + page_nodes("en", url, title, description, "CollectionPage", [("Home", SITE + "/"), ("Notes", url)],
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
    return (head("en", title, description, url, "website", nodes) + header("en", "notes", {"en": "/notes/"}) + f"""
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

""" + contact_block("en") + FOOTER)


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


# ── Projects ────────────────────────────────────────────────────────────────

PROJECT_TEXT = {
    "en": {"eyebrow": "Side project", "crumb": "Projects", "facts": "At a glance", "status": "Status",
           "stack": "Stack", "license": "License", "links": "Links", "repo": "GitHub", "npm": "npm", "live": "Live app",
           "source": "Plain text", "more": "All projects"},
    "fr": {"eyebrow": "Projet perso", "crumb": "Projets", "facts": "En bref", "status": "Statut",
           "stack": "Stack", "license": "Licence", "links": "Liens", "repo": "GitHub", "npm": "npm", "live": "Application",
           "source": "Texte brut", "more": "Tous les projets"},
}


def project_page(p, graph):
    lang, url, T, L = p["lang"], p["url"], PROJECT_TEXT[p["lang"]], LANG[p["lang"]]
    links = [(T[k], p[k]) for k in ("repo", "npm", "live") if p.get(k)]
    code = {
        "@type": "SoftwareSourceCode", "@id": url + "#software", "name": p["title"], "description": p["description"],
        "codeRepository": p["repo"], "programmingLanguage": [s.strip() for s in p.get("stack", "").split("·") if s.strip()],
        "license": p.get("license"), "author": {"@id": SITE + "/#person"}, "creator": {"@id": SITE + "/#person"},
        "dateCreated": p["date"], "dateModified": p["updated"], "url": url,
        "sameAs": [u for _, u in links], "inLanguage": lang,
    }
    home_projects = L["home"] + "#projects"
    nodes = graph + page_nodes(lang, url, p["title"], p["description"], "WebPage",
                               [(L["home_crumb"], SITE + L["home"]), (T["crumb"], SITE + home_projects), (p["title"], url)],
                               mainEntity={"@id": url + "#software"}) + [code]
    switch = {l: u.replace(SITE, "") for l, u in p["alternates"].items()}
    facts = "".join(f"<div><dt>{label}</dt><dd>{html.escape(p[key])}</dd></div>"
                    for key, label in (("status", T["status"]), ("stack", T["stack"]), ("license", T["license"])) if p.get(key))
    link_items = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener noreferrer">{label} ↗</a></li>'
                         for label, u in links)
    return (head(lang, f'{p["title"]} — {p["tagline"]} | Brahim Bousnguar', p["description"], url, "website", nodes,
                 alternates=p["alternates"], extra=f'  <link rel="alternate" type="text/markdown" href="{p["md_path"]}">\n')
            + header(lang, "projects", switch) + f"""
    <article class="project" aria-labelledby="project-title">
      <header class="page-intro note-intro">
        <div class="wrap">
          <p class="eyebrow"><a href="{home_projects}">{T["eyebrow"]}</a></p>
          <h1 id="project-title">{html.escape(p["title"])}</h1>
          <p class="hero-lede">{html.escape(p["tagline"])}</p>
        </div>
      </header>

      <div class="wrap">
       <div class="note-layout">
        <aside class="note-aside" aria-label="{T["facts"]}">
          <p class="note-aside-title mono">{T["facts"]}</p>
          <dl class="project-facts">{facts}</dl>
          <ul class="project-links">{link_items}</ul>
        </aside>
        <div class="note-body prose">
{p["html"]}
          <p class="note-source mono">{T["source"]}: <a href="{p["md_path"]}">{p["slug"]}.md</a> · <a href="{home_projects}">{T["more"]}</a></p>
        </div>
       </div>
      </div>
    </article>

""" + contact_block(lang) + FOOTER)


# ── Site-wide outputs ───────────────────────────────────────────────────────

def last_commit_date(rel):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or date.today().isoformat()


def sitemap_url(loc, lastmod, alternates=None):
    links = ""
    if alternates and len(alternates) > 1:
        links = "".join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{u}"/>\n' for l, u in alternates.items())
        links += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{alternates["en"]}"/>\n'
    return f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n{links}  </url>"


def sitemap(notes, generated):
    urls = []
    for en_path, en_file, fr_path, fr_file in STATIC_PAGES:
        alts = {"en": SITE + en_path, "fr": SITE + fr_path}
        urls.append(sitemap_url(SITE + en_path, last_commit_date(en_file), alts))
        urls.append(sitemap_url(SITE + fr_path, last_commit_date(fr_file), alts))
    urls.append(sitemap_url(SITE + "/notes/", max(n["updated"] for n in notes)))
    for p in generated:
        urls.append(sitemap_url(p["url"], p["updated"], p["alternates"]))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")


def update_llms_index(name, pages):
    """Rewrite one list between <!-- name:start --> / <!-- name:end --> in llms.txt."""
    path = ROOT / "llms.txt"
    lines = "".join(f"- [{p['title']}]({p['url']}) ({p['date']}): {p['description']} Markdown: {SITE}{p['md_path']}\n"
                    for p in pages)
    text = re.sub(rf"<!-- {name}:start -->\n.*?<!-- {name}:end -->", lambda _: f"<!-- {name}:start -->\n{lines}<!-- {name}:end -->",
                  path.read_text(), flags=re.S)
    path.write_text(text)


def llms_full(notes, projects):
    parts = [(ROOT / "llms.txt").read_text().rstrip()]
    for heading, pages in (("Notes (full text)", notes), ("Projects (full text)", projects)):
        parts.append(f"\n\n# {heading}\n")
        for p in pages:
            parts.append(f"\n---\n\n## {p['title']}\n\nURL: {p['url']}\nPublished: {p['date']} · Updated: {p['updated']}\n\n{p['markdown']}\n")
    return "".join(parts)


def main():
    notes = [p for p in load("notes")]
    projects = load("projects")
    if not notes:
        raise SystemExit("no published notes in notes/")
    graph = site_graph()
    for n in notes:
        (ROOT / n["file"]).write_text(note_page(n, graph))
    (ROOT / "notes/index.html").write_text(notes_index(notes, graph))
    (ROOT / "notes/feed.xml").write_text(feed(notes))
    for p in projects:
        (ROOT / p["file"]).write_text(project_page(p, graph))
    (ROOT / "sitemap.xml").write_text(sitemap(notes, notes + projects))
    update_llms_index("notes", notes)
    en_projects = [p for p in projects if p["lang"] == "en"]
    update_llms_index("projects", en_projects)
    (ROOT / "llms-full.txt").write_text(llms_full(notes, en_projects))
    print(f"built {len(notes)} note(s), {len(projects)} project page(s)")


if __name__ == "__main__":
    main()
