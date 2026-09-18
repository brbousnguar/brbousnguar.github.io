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
| `index.html` | The portfolio: hero, facts strip, integration flow, client cases, side projects, experience, stack, credentials, contact |
| `pages/about.html` | Career story, timeline, current focus, what's next |
| `assets/css/style.css` | The only stylesheet (Blueprint design system) |
| `assets/js/main.js` | EN/FR switch — the only runtime script |
| `llms.txt`, `profile.json` | Machine-readable profile for AI agents; linked from the footer |
| `sitemap.xml` | Update when pages are added or removed |
| `robots.txt` | Search crawler directives, with an explicit AI-crawler allowlist |
| `tools/indexnow.py` | Pings IndexNow (Bing, Yandex…) with changed URLs after a deploy |

**Watch out — these are not the files you want to edit:**

- Root `about.html` is a **redirect stub** pointing at `pages/about.html`. Root `learning.html` and `pages/learning.html` are `noindex` redirect stubs to the home page — the LinkedIn Learning browser was removed on 2026-09-11; keep the stubs so old links don't 404.
- `tools/` holds the generators, not linked from the site: `cv.html` (below); `make_favicons.py`, which rebuilds `favicon.ico` and the `assets/img/` icon PNGs from the BB brand mark — bump the `?v=` query on the icon links after regenerating; and `make_og_card.py`, which renders the 1200×630 share cards `assets/img/og-card.png` (EN) and `og-card-fr.png` (FR, used once French has its own URL) from the hero copy — rerun it when the name, title or lede changes, bump the `?v=` on `og:image`/`twitter:image`, and re-scrape in the LinkedIn Post Inspector.
- `docs/Brahim_Bousnguar_CV.pdf` is **generated** from `tools/cv.html` (Blueprint styling, content mirrors `profile.json`) — edit the HTML and re-print it with the headless-Chrome command in its header comment; never edit the PDF by hand. Keep it at two A4 pages.

## Architecture: Bilingual System

Every user-visible section must exist in **both English and French**, and the page ships **both copies in the DOM at once** — the toggle changes which is visible, it does not load content. There are two layers:

1. **Wrapper level:** the entire EN body lives in `<div id="en" class="lang-content">` and the FR body in `<div id="fr" class="lang-content">`. The inline pre-paint script sets `data-lang` on `<html>` from `localStorage` (`language`), and CSS shows `#en` or `#fr` from that attribute — visibility needs no JS. `setLanguage(lang)` in `main.js` flips the attribute and persists it. Short strings outside the wrappers (nav, skip link) use `.t-en` / `.t-fr` spans.
2. **Section level:** matching sections are mirrored by ID suffix — `work` / `work-fr`, `contact` / `contact-fr`, etc. Nav links carry `data-target="<base id>"`; `main.js` rewrites their `href` to the suffixed ID for the active language.

When adding content you must duplicate it into **both** wrapper divs and give the FR copy the `-fr` ID suffix, or the nav will land on an empty section.

## Theming

**Light only.** There is no dark mode, no `data-theme`, no `prefers-color-scheme` branch and no toggle — do not add one back. The design system is **Blueprint**, a variant of the Fortunex/Vitalex Banknote system: flat (no shadows, gradients, blur), hard-edged (`border-radius: 0` everywhere), separated by hairline rules rather than boxes. Palette: paper `#FBFAF7`, ink `#131211`, one accent `--cobalt` `#1446C8` (dual-role), `--marker` `#FFD84D` (fill-only, used once for the hero highlighter), `--sky` `#9DB6FF` (links on the ink contact band only). Type: Archivo (display), Hanken Grotesk (reading), IBM Plex Mono (labels). All colours come from CSS custom properties — use `var(--…)`, never hardcode. `docs/DESIGN-SYSTEM.md` is the spec, with measured contrast figures and the verification commands; change it in the same commit as `style.css`.

## Coding Conventions

- 2-space indentation in HTML and CSS
- kebab-case for CSS class names (`project-card`, `value-box`)
- Prefer CSS classes over inline styles
- External links require `rel="noopener noreferrer"` with `target="_blank"`

## SEO Conventions

Each page carries a full SEO head block: `<title>`, meta description, Open Graph (with `og:image:alt`, `og:site_name`, `og:locale`), Twitter Card (`name=` attributes, not `property=`), JSON-LD structured data as **one linked `@graph`** — `Person` (`@id` `https://heybrahim.com/#person`, identical on every page: edit both copies together), `WebSite` (`#website`), the page node (`ProfilePage` on home, `AboutPage` on About; later pages use their own type) with `mainEntity` → `#person`, and a `BreadcrumbList`. New pages reuse the `#person` / `#website` `@id`s instead of inventing new Person blocks; no FAQPage — there is no visible FAQ, canonical URL, and hreflang alternates (`en` / `fr` / `x-default`). When adding or modifying a page, keep all of these consistent. No `meta keywords` (search engines ignore it) and no `Crawl-delay` in `robots.txt` (Bing throttles on it). Refer to `docs/SEO-GUIDE.md` for the keyword strategy.

**IndexNow:** after a deploy that adds or changes pages, run `python3 tools/indexnow.py` (whole sitemap) or `python3 tools/indexnow.py <url>…`. It pings Bing, whose index also feeds ChatGPT search, Copilot and DuckDuckGo. The key file `e163ae94f3a76216d86baae9ec74bcd2.txt` at the repo root proves ownership — keep it.

## Related Guidance & Conventions

This repo also carries `AGENTS.md` and `docs/DESIGN-SYSTEM.md`. `docs/DESIGN-SYSTEM.md` is the authoritative, detailed spec for the **design system** (color tokens, typography, spacing, breakpoints), accessibility and SEO requirements, and the verification harness (contrast, 320px reflow, Lighthouse) — consult it before substantial UI or content work rather than re-deriving these. Open enhancement work and priorities are tracked in `docs/TODO.md`.

## Git & PR Workflow

- Branch naming: `feat/<short-description>` (e.g., `feat/sidebar-highlighting`)
- Commit style: `type: short imperative message` (e.g., `feat: add hero section`, `fix: correct mobile spacing`)
- Always pull before push; prefer rebase over merge when integrating `main`
- PRs require a brief summary + list of changes; UI changes need before/after screenshots
- Do not merge to `main` without opening a PR first
