# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Static GitHub Pages portfolio site for Brahim Bousnguar — Senior E-Commerce Integration Consultant. No build step, no package manager, no CI pipeline. Deployed automatically by GitHub Pages from the `main` branch.

## Local Development

**Preferred:** Use the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) VS Code extension — right-click any HTML file and select *Open with Live Server*. It auto-reloads on save, so no manual refresh needed.

**Fallback:**
```bash
python -m http.server 5173
# Then open http://localhost:5173
```

Hard refresh (Ctrl+F5) after HTML/CSS changes if not using Live Server.

## Pages & Key Files

| File | Purpose |
|------|---------|
| `index.html` | English home (`/`) — the portfolio: hero, facts strip, integration flow, client cases, side projects, experience, stack, credentials, contact |
| `pages/about.html` | English About — career story, timeline, current focus, what's next |
| `fr/index.html`, `fr/a-propos.html` | French counterparts at `/fr/` and `/fr/a-propos.html` |
| `assets/css/style.css` | The only stylesheet (Blueprint design system) |
| `llms.txt`, `profile.json` | Machine-readable profile for AI agents; linked from the footer |
| `notes/<slug>.md` | Note sources (English-only, front matter + Markdown); published as-is for agents |
| `work/<slug>.md`, `fr/missions/<slug>.md` | Anonymised client case-study sources, EN and FR paired by filename; generated into `.html` next to them |
| `projects/<slug>.md`, `fr/projets/<slug>.md` | Side-project page sources, EN and FR paired by filename; generated into `.html` next to them |
| `tools/build_site.py` | Builds `notes/*.html`, `notes/index.html`, `notes/feed.xml`, `sitemap.xml`, `llms-full.txt` and the note list in `llms.txt` — never hand-edit those outputs |
| `sitemap.xml` | **Generated** by `tools/build_site.py`; add a new static page to its `STATIC_PAGES` list, then rebuild |
| `robots.txt` | Search crawler directives, with an explicit AI-crawler allowlist |
| `tools/indexnow.py` | Pings IndexNow (Bing, Yandex…) with changed URLs after a deploy |

**Watch out — these are not the files you want to edit:**

- Root `about.html` is a **redirect stub** pointing at `pages/about.html`. Root `learning.html` and `pages/learning.html` are `noindex` redirect stubs to the home page — the LinkedIn Learning browser was removed on 2026-09-11; keep the stubs so old links don't 404.
- `tools/` holds the generators, not linked from the site: `cv.html` (below); `make_favicons.py`, which rebuilds `favicon.ico` and the `assets/img/` icon PNGs from the BB brand mark — bump the `?v=` query on the icon links after regenerating; and `make_og_card.py`, which renders the 1200×630 share cards `assets/img/og-card.png` (EN) and `og-card-fr.png` (FR, used once French has its own URL) from the hero copy — rerun it when the name, title or lede changes, bump the `?v=` on `og:image`/`twitter:image`, and re-scrape in the LinkedIn Post Inspector.
- `docs/Brahim_Bousnguar_CV.pdf` is **generated** from `tools/cv.html` (Blueprint styling, content mirrors `profile.json`) — edit the HTML and re-print it with the headless-Chrome command in its header comment; never edit the PDF by hand. Keep it at two A4 pages.

## Architecture: Bilingual System

**One language per URL.** English lives at `/` and `/pages/about.html`; French at `/fr/` and `/fr/a-propos.html`. Each page has one `lang`, one `<h1>`, its own title/description/OG tags (FR pages use `og-card-fr.png` and `og:locale` `fr_FR`), a self-canonical, and reciprocal `hreflang` links (`en`, `fr`, `x-default` → English). There is no runtime script and no `localStorage`: the header's EN/FR switch is two plain links to the counterpart page (`aria-current` marks the active one), so crawlers see both versions and nothing auto-redirects.

When you change visible content, change **both** the English file and its French counterpart; section IDs are the same in both languages (`#work`, `#contact`…). FR pages use root-absolute paths (`/assets/…`, `/fr/#work`). Adding a page means: both language files, the four `hreflang`/canonical links on each, and both URLs in `STATIC_PAGES` in `tools/build_site.py` (which writes `sitemap.xml` with `xhtml:link` alternates).

**Exception — notes are English-only** (decided 2026-09-18, #44): a note gets a French version only when it is worth translating, and only then does it carry `hreflang` alternates.

## Analytics

Cloudflare Web Analytics (#47): a cookieless beacon, so no consent banner. The snippet sits at the end of `<head>` in the four hand-written pages and in `ANALYTICS` in `tools/build_site.py` for generated pages. Every new hand-written page needs it too. The dashboard is in Brahim's Cloudflare account (heybrahim.com's DNS is on Cloudflare); the token is public by design.

## Generated pages (`tools/build_site.py`)

Notes and project pages are Markdown sources built into HTML by `python3 tools/build_site.py` (no dependencies). Commit the sources **and** the outputs together, and never hand-edit an output: `notes/*.html`, `notes/index.html`, `notes/feed.xml`, `projects/*.html`, `fr/projets/*.html`, `work/*.html`, `fr/missions/*.html`, `sitemap.xml`, `llms-full.txt`, `404.html` (the branded not-found page, `noindex`), and the lists between `<!-- notes:… -->` / `<!-- projects:… -->` / `<!-- work:… -->` markers in `llms.txt`. The builder takes `#person`/`#website` from `index.html` and the contact band from `pages/about.html` / `fr/a-propos.html`, so edit those there. Nav labels, the language switch and per-language strings live in its `LANG`, `PROJECT_TEXT` and `WORK_TEXT` tables; project and case-study pages share `detail_page()`.

**Projects** (`/projects/<slug>.html` ↔ `/fr/projets/<slug>.html`, #46): one `.md` per language with the same filename; front matter `title`, `tagline`, `description`, `date`, `repo`, optional `npm`/`live`/`download`, `stack` (· separated), `license`, `status`. Pages get `SoftwareSourceCode` JSON-LD and reciprocal `hreflang`. The home page's project list links to them — add a row in both `index.html` and `fr/index.html` when you add a project. **Retiring a project** (#72): delete its `.md` sources and cards, replace both `.html` files with a `noindex` meta-refresh stub to `/#projects` / `/fr/#projects` (the builder only generates pages that have a `.md`, so stubs are left alone and stay out of the sitemap), and remove its home rows and `profile.json` entry. Retired so far: Termo Track, MacBook MCP Server, ASCII Art Studio. The **Merged upstream** list under the projects shows merged PRs to other projects only; add a PR when it merges, never while it's open. Only facts from the repo's README or Brahim; the same no-invention rule as notes.

**Case studies** (`/work/<slug>.html` ↔ `/fr/missions/<slug>.html`, #45): **anonymised on purpose** (decided 2026-09-18): the pages say "a luxury furniture retailer", "a global home-appliance manufacturer", "a specialty chemicals group"; client names appear only on the home-page cards, which link to the pages. Never put a client name in a case-study title, slug, body, description or JSON-LD. Front matter: `title`, `tagline`, `description`, `date` (publication), `client` (the anonymised descriptor), `period`, `role`, `stack`. The diagram is the home page's `.flow` component written as raw HTML (no blank lines inside it). Content comes only from `profile.json`, the CV or Brahim; add detail when he provides it.

**Share cards** (#60): every generated page has its own 1200×630 card at `assets/img/og/<collection>-<slug>[-fr].png` (eyebrow, the page title, its tagline or description, the ink band). The builder uses a page's card when the file exists and the site card otherwise. So after adding or retitling a page, run in this order: write the `.md` → `python3 tools/make_og_card.py` (needs Pillow and the fonts, see its docstring) → `python3 tools/build_site.py`. Case-study cards use the anonymised titles, never a client name.

## Notes (`/notes/`)

Writing lives in `notes/<slug>.md`: front matter (`title`, `description`, `date`, optional `updated`, `tags`, `project`, `draft: true`) then Markdown. Run `python3 tools/build_site.py` and commit the sources **and** the generated files together; after the deploy, run `tools/indexnow.py`. The builder takes `#person`/`#website` from `index.html` and the contact band from `pages/about.html`, so edit those there. Its converter handles `##`/`###`, paragraphs, `-`/`1.` lists, `>` quotes, fenced code, pipe tables, bold, italic, inline code and links; write raw HTML for anything else.

Notes follow the author's private voice guide, which is kept outside this repo on purpose; don't add style rules here. Two rules are structural and public: the opening paragraph must answer the title on its own (search and AI answer engines quote it), and nothing is invented (no experiences, clients or numbers that aren't sourced; nothing under NDA). Brahim reviews every note before it is merged, and his wording wins.

## Theming

**Light only.** There is no dark mode, no `data-theme`, no `prefers-color-scheme` branch and no toggle — do not add one back. The design system is **Blueprint**, a variant of the Fortunex/Vitalex Banknote system: flat (no shadows, gradients, blur), hard-edged (`border-radius: 0` everywhere), separated by hairline rules rather than boxes. Palette: paper `#FBFAF7`, ink `#131211`, one accent `--cobalt` `#1446C8` (dual-role), `--marker` `#FFD84D` (fill-only, used once for the hero highlighter), `--sky` `#9DB6FF` (links on the ink contact band only). Type: Archivo (display), Hanken Grotesk (reading), IBM Plex Mono (labels), **self-hosted** from `assets/fonts/` (#68): the latin woff2 files Google Fonts serves, declared with `@font-face` at the top of `style.css`, the two variable fonts preloaded in every `<head>`. Never add the Google Fonts `<link>` back; it was the render-blocking request. Only `tools/cv.html` (the offline CV template) still loads Google Fonts. All colours come from CSS custom properties — use `var(--…)`, never hardcode. `docs/DESIGN-SYSTEM.md` is the spec, with measured contrast figures and the verification commands; change it in the same commit as `style.css`.

## Coding Conventions

- 2-space indentation in HTML and CSS
- kebab-case for CSS class names (`project-card`, `value-box`)
- Prefer CSS classes over inline styles
- External links require `rel="noopener noreferrer"` with `target="_blank"`

## SEO Conventions

Each page carries a full SEO head block: `<title>`, meta description, Open Graph (with `og:image:alt`, `og:site_name`, `og:locale`), Twitter Card (`name=` attributes, not `property=`), JSON-LD structured data as **one linked `@graph`** — `Person` (`@id` `https://heybrahim.com/#person`, identical on every page: edit both copies together), `WebSite` (`#website`), the page node (`ProfilePage` on home, `AboutPage` on About; later pages use their own type) with `mainEntity` → `#person`, and a `BreadcrumbList`. New pages reuse the `#person` / `#website` `@id`s instead of inventing new Person blocks; no FAQPage — there is no visible FAQ, canonical URL, and reciprocal hreflang alternates between the EN and FR URLs (`en` / `fr` / `x-default` → EN). When adding or modifying a page, keep all of these consistent. No `meta keywords` (search engines ignore it) and no `Crawl-delay` in `robots.txt` (Bing throttles on it). Refer to `docs/SEO-GUIDE.md` for the keyword strategy.

**IndexNow:** after a deploy that adds or changes pages, run `python3 tools/indexnow.py` (whole sitemap) or `python3 tools/indexnow.py <url>…`. It pings Bing, whose index also feeds ChatGPT search, Copilot and DuckDuckGo. The key file `e163ae94f3a76216d86baae9ec74bcd2.txt` at the repo root proves ownership — keep it.

## Related Guidance & Conventions

This repo also carries `AGENTS.md` and `docs/DESIGN-SYSTEM.md`. `docs/DESIGN-SYSTEM.md` is the authoritative, detailed spec for the **design system** (color tokens, typography, spacing, breakpoints), accessibility and SEO requirements, and the verification harness (contrast, 320px reflow, Lighthouse) — consult it before substantial UI or content work rather than re-deriving these. Open enhancement work and priorities are tracked in `docs/TODO.md`.

## Git & PR Workflow

- Branch naming: `feat/<short-description>` (e.g., `feat/sidebar-highlighting`)
- Commit style: `type: short imperative message` (e.g., `feat: add hero section`, `fix: correct mobile spacing`)
- Always pull before push; prefer rebase over merge when integrating `main`
- PRs require a brief summary + list of changes; UI changes need before/after screenshots
- Do not merge to `main` without opening a PR first
