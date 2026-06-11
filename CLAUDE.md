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
| `index.html` | Main portfolio page (hero, skills, projects, contact) |
| `pages/about.html` | Extended professional story |
| `pages/learning.html` | Certificates browser — loads dynamically from `assets/data/learning-data.json` |
| `assets/css/style.css` | Global styles shared across all pages |
| `assets/css/about.css` | About page-specific styles |
| `assets/css/learning.css` | Learning page-specific styles |
| `assets/js/learning.js` | Certificate filtering, search, and rendering logic |
| `assets/data/learning-data.json` | Certificate dataset (~400 entries) consumed by `learning.js` |
| `sitemap.xml` | Update when pages are added or removed |
| `robots.txt` | Search crawler directives |

The `assets/js/` directory also contains Python scripts (`extract-*.py`, `organize-*.py`) used to process and reorganize the certificate data — these are one-off utilities, not part of the site runtime.

**Watch out — these are not the files you want to edit:**

- Root `about.html` and `learning.html` are **redirect stubs** (`<meta http-equiv="refresh">`) pointing at `pages/about.html` and `pages/learning.html`. Edit the versions under `pages/`, not the root stubs.
- `archived/` holds the source certificate PDFs (organized by year, several hundred files) that the Python scripts process into `learning-data.json`. It is the data origin, not site output.
- `tools/` contains standalone authoring utilities (SEO helper, favicon generator, GitHub Pages setup guide) — not linked from the site.

## Architecture: Bilingual System

Every user-visible section must exist in **both English and French**, and the page ships **both copies in the DOM at once** — the toggle changes which is visible, it does not load content. There are two layers:

1. **Wrapper level:** the entire EN body lives in `<div id="en" class="lang-content">` and the FR body in `<div id="fr" class="lang-content">`. `setLanguage(lang)` removes `active` from all `.lang-content`, adds it to the chosen one, sets both `lang` and `data-lang` on `<html>`, and persists to `localStorage` (`language`).
2. **Section level:** matching sections are mirrored by ID suffix — `summary` / `summary-fr`, `contact` / `contact-fr`, etc. JS that targets a section (sidebar scrollspy, anchors) derives the suffix from the active language: `const suffix = lang === 'fr' ? '-fr' : ''`.

When adding content you must duplicate it into **both** wrapper divs and give the FR copy the `-fr` ID suffix, or the toggle/sidebar will land on an empty section.

## Theming

Light/dark theme is set via `data-theme` on `<html>` (default light; `data-theme="dark"` for dark). The choice is persisted to `localStorage` (`theme`) and falls back to the OS `prefers-color-scheme` on first visit; an inline pre-paint snippet in each page `<head>` applies it before first render. All colors come from CSS custom properties in `style.css` — use `var(--…)`, never hardcode. The palette is a deliberate **warm graphite + amber** scheme; amber is the only accent hue — do not introduce blue/cold accents. Amber contrast rules: small text in light mode uses `--accent-text`, filled amber surfaces use dark `--accent-contrast` text (never white). See `.cursorrules` for the full token table. Verify both themes after any visual change.

## Coding Conventions

- 2-space indentation in HTML and CSS
- kebab-case for CSS class names (`project-card`, `value-box`)
- Prefer CSS classes over inline styles
- External links require `rel="noopener noreferrer"` with `target="_blank"`

## SEO Conventions

Each page carries a full SEO head block: `<title>`, meta description/keywords, Open Graph, Twitter Card, JSON-LD structured data (BreadcrumbList + Person, plus FAQPage where relevant), canonical URL, and hreflang alternates (`en` / `fr` / `x-default`). When adding or modifying a page, keep all of these consistent. Refer to `docs/SEO-GUIDE.md` for the keyword strategy.

## Related Guidance & Conventions

This repo also carries `AGENTS.md` and `.cursorrules`. `.cursorrules` is the authoritative, detailed spec for the **design system** (color tokens, typography, spacing, breakpoints), accessibility requirements (skip links, ARIA, focus states, WCAG AA contrast), and per-page SEO/structured-data checklists — consult it before substantial UI or content work rather than re-deriving these. Open enhancement work and priorities are tracked in `docs/TODO.md`.

## Git & PR Workflow

- Branch naming: `feat/<short-description>` (e.g., `feat/sidebar-highlighting`)
- Commit style: `type: short imperative message` (e.g., `feat: add hero section`, `fix: correct mobile spacing`)
- Always pull before push; prefer rebase over merge when integrating `main`
- PRs require a brief summary + list of changes; UI changes need before/after screenshots
- Do not merge to `main` without opening a PR first
