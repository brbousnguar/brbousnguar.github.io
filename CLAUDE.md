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
| `about.html` | Extended professional story |
| `learning.html` | Certificates browser — loads dynamically from `js/learning-data.json` |
| `css/style.css` | Global styles shared across all pages |
| `css/about.css` | About page-specific styles |
| `css/learning.css` | Learning page-specific styles |
| `js/learning.js` | Certificate filtering, search, and rendering logic |
| `js/learning-data.json` | Certificate dataset (~400 entries) consumed by `learning.js` |
| `sitemap.xml` | Update when pages are added or removed |
| `robots.txt` | Search crawler directives |

The `js/` directory also contains Python scripts (`extract-*.py`, `organize-*.py`) used to process and reorganize the certificate data — these are one-off utilities, not part of the site runtime.

## Architecture: Bilingual System

Every user-visible section must exist in **both English and French**. The language toggle sets `data-lang` on `<html>` and toggles visibility using CSS. Convention:

- English sections/IDs: `section-id`
- French sections/IDs: `section-id-fr`
- The `lang` attribute value (`en` / `fr`) drives suffix logic in JS: `const suffix = lang === 'fr' ? '-fr' : ''`

When adding content, always duplicate it in the other language or the toggle will show an empty section.

## Coding Conventions

- 2-space indentation in HTML and CSS
- kebab-case for CSS class names (`project-card`, `value-box`)
- Prefer CSS classes over inline styles
- External links require `rel="noopener noreferrer"` with `target="_blank"`

## SEO Conventions

Each page carries a full SEO head block: `<title>`, meta description/keywords, Open Graph, Twitter Card, JSON-LD structured data, canonical URL, and hreflang alternates. When adding or modifying a page, keep all of these consistent. Refer to `SEO-GUIDE.md` for the keyword strategy.

## Git & PR Workflow

- Branch naming: `feat/<short-description>` (e.g., `feat/sidebar-highlighting`)
- Commit style: `type: short imperative message` (e.g., `feat: add hero section`, `fix: correct mobile spacing`)
- Always pull before push; prefer rebase over merge when integrating `main`
- PRs require a brief summary + list of changes; UI changes need before/after screenshots
- Do not merge to `main` without opening a PR first
