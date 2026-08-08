# Portfolio Website

A professional portfolio website for **Brahim Bousnguar** — Senior E-Commerce Integration Consultant specializing in SAP Commerce Cloud, MuleSoft Anypoint & Salesforce. Built with pure HTML/CSS/JS and hosted on GitHub Pages.

## 🌐 Live Website

Visit the live portfolio at: **[https://brbousnguar.github.io/](https://brbousnguar.github.io/)**

## 📋 About

This repository contains the source code for my personal portfolio website showcasing 9+ years of experience in Java, e-commerce architectures, API-led integration, and AI-augmented development workflows. The site is fully bilingual (English/French), themeable (light/dark), and SEO-optimized with structured data for search engines and AI crawlers.

## 📄 Pages

| Page | Path | Purpose |
|------|------|---------|
| **Home** | `index.html` | Hero with proof stats, bento project grid, skills, learning summary, timeline, and contact |
| **About** | `pages/about.html` | Extended professional story and value propositions |
| **Learning** | `pages/learning.html` | Certificates browser — 644+ LinkedIn Learning certificates filtered and rendered dynamically from `assets/data/learning-data.json` |

> Root `about.html` and `learning.html` are redirect stubs pointing to the `pages/` versions — edit the ones under `pages/`, not the stubs.

## 🗂️ Project Structure

```
index.html              # Main portfolio page
pages/
  about.html            # About page (canonical)
  learning.html         # Certificates browser (canonical)
assets/
  css/                  # style.css (global), about.css, learning.css
  data/                 # learning-data.json (644+ certificate entries)
  js/                   # learning.js, main.js + Python data-processing scripts
  img/                  # Images, logos, favicon, profile
  icons/                # Icon assets
archived/               # Source certificate PDFs organized by year (data origin)
docs/                   # DESIGN-SYSTEM.md, SEO-GUIDE.md, TODO.md
tools/                  # Standalone authoring utilities (SEO helper, favicon generator)
sitemap.xml             # Search engine sitemap
robots.txt              # Crawler directives
llms.txt                # Machine-readable profile for AI agents
profile.json            # Structured profile (JSON Resume format)
.github/workflows/      # Lighthouse CI report on push to main
```

## 🛠️ Technologies Used

- **HTML5** — Semantic markup and structure
- **CSS3** — Custom properties, Grid, Flexbox, glassmorphism, scroll-reveal animations
- **JavaScript** — Bilingual toggle, theme toggle, scrollspy, stat counters, certificate filtering
- **Google Fonts** — Typography (Inter)
- **GitHub Pages** — Static site hosting
- **GitHub Actions** — Lighthouse performance report on every push to `main`

## 🎨 Features

- **Bilingual Support** — English and French language toggle with full content mirrored in both languages; preference persisted to `localStorage`
- **Light/Dark Themes** — Warm graphite + amber palette driven by CSS custom properties; respects OS `prefers-color-scheme` on first visit
- **Responsive Design** — Mobile-first layout with glassmorphism touches and a bento project grid
- **SEO Optimized** — Meta tags, Open Graph, Twitter Cards, JSON-LD structured data (Person, BreadcrumbList, FAQPage), canonical URLs, hreflang alternates, and sitemap
- **AI-Agent Ready** — `llms.txt` and `profile.json` machine-readable profile, plus enhanced AI crawler meta tags
- **Interactive Elements** — Scroll-reveal animations, animated stat counters, smooth transitions (with `prefers-reduced-motion` support)
- **Learning Browser** — Searchable, filterable certificate gallery loaded dynamically from JSON
- **CV Download** — Direct PDF download from `docs/`
- **Contact Integration** — Direct email and social media links

## 🛠️ Local Development

Use the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) VS Code extension for local preview — right-click any HTML file and select *Open with Live Server*. It auto-reloads on save.

Alternatively:

```bash
python -m http.server 5173
# Then open http://localhost:5173
```

Hard refresh (Ctrl+F5) after HTML/CSS changes if not using Live Server.

## 📊 Performance & CI

- **Lightweight** — No build step, no package manager, minimal external dependencies
- **Modern CSS** — CSS Grid and Flexbox for efficient layouts
- **Progressive Enhancement** — Core content works without JavaScript
- **Lighthouse CI** — A GitHub Actions workflow (`.github/workflows/main.yml`) generates a Lighthouse report on every push to `main`

## 📚 Documentation

- [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md) — Color tokens, typography, spacing, breakpoints, accessibility requirements
- [`docs/SEO-GUIDE.md`](docs/SEO-GUIDE.md) — Keyword strategy and per-page SEO checklists
- [`docs/TODO.md`](docs/TODO.md) — Open enhancement work and priorities
- [`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md) — Contribution guidelines and architecture notes

## 🤝 Contact

- **Email**: [b.bousnguar@gmail.com](mailto:b.bousnguar@gmail.com)
- **LinkedIn**: [linkedin.com/in/brahim-bousnguar](https://www.linkedin.com/in/brahim-bousnguar/)
- **GitHub**: [github.com/brbousnguar](https://github.com/brbousnguar)
- **X**: [@bbousnguar](https://x.com/bbousnguar)

---

**Built with ❤️ by Brahim Bousnguar**
