# brbousnguar.github.io

**Portfolio of Brahim Bousnguar — Senior E-Commerce Integration Consultant (SAP Commerce Cloud, MuleSoft Anypoint, Salesforce).**
A static, bilingual (EN/FR) GitHub Pages site with no build step, served from `main` at **[brbousnguar.github.io](https://heybrahim.com/)**.

---

## What it does

Presents 9+ years of enterprise e-commerce and integration work to recruiters, clients and AI agents, in two short pages.

- **Home (`index.html`)** — hero, facts strip, an integration-flow diagram (SAP Commerce Cloud → MuleSoft → Salesforce/ERP), three client case studies (Problem / Built / Result), side projects and open-source contributions, experience, stack, SAP certifications, and a contact block.
- **About (`pages/about.html`)** — career story, timeline, current focus and what comes next.
- **Bilingual** — English and French both ship in the DOM; an EN/FR switch in the header flips between them and the choice persists in `localStorage`.
- **Machine-readable** — `llms.txt`, `profile.json` (JSON Resume style) and Person JSON-LD for search engines and AI agents; `robots.txt` explicitly allows the major AI crawlers.
- **CV download** — `docs/Brahim_Bousnguar_CV.pdf`.

## Requirements

- Any static file server for local preview (Python 3 or the VS Code Live Server extension)
- Google Chrome, only for the verification harness

## Run

```bash
python3 -m http.server 5173
# open http://localhost:5173
```

Or right-click `index.html` → *Open with Live Server* in VS Code for auto-reload. Pushing to `main` deploys through GitHub Pages.

## Design system

**Blueprint** — a light-only variant of the Banknote system used by the Fortunex and Vitalex webapps. The full spec, with measured contrast figures, lives in [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md) and changes in the same commit as `assets/css/style.css`.

| Rule | In practice |
|---|---|
| Light only | No dark mode, no theme toggle, `color-scheme: light` |
| Flat | No shadows, gradients, blur or glass |
| Hard-edged | `border-radius: 0` everywhere |
| Rule-separated | Rows divided by hairlines, not boxes around every item |
| Palette | Paper `#FBFAF7`, ink `#131211`, cobalt `#1446C8`; marker yellow `#FFD84D` is fill-only |
| Type | Archivo (display), Hanken Grotesk (reading), IBM Plex Mono (labels) |

## Verification

Run from the repo root before shipping a visual change:

```bash
PORT=8798 ~/Server/.claude/skills/brb-flat-poster-theme/scripts/verify.sh . index.html pages/about.html
```

It checks alpha-composited contrast and true 320px reflow. Then run Lighthouse (mobile) against the local server. Current state: 0 contrast failures, page width 320 in EN and FR, Accessibility / Best Practices / SEO 100 on both pages.

## Tech stack

| Layer | Technology |
|---|---|
| Markup | HTML5, JSON-LD (Person, BreadcrumbList) |
| Styles | One hand-written stylesheet, CSS custom properties |
| Script | Vanilla JS (`assets/js/main.js`, EN/FR switch only) |
| Fonts | Google Fonts: Archivo, Hanken Grotesk, IBM Plex Mono |
| Hosting | GitHub Pages from `main` |

## Repository layout

```text
.
├── index.html                  # the portfolio (EN + FR bodies)
├── pages/
│   ├── about.html              # career story (canonical)
│   └── learning.html           # noindex redirect stub → home
├── about.html, learning.html   # redirect stubs (about → pages/, learning → home)
├── assets/
│   ├── css/style.css           # the only stylesheet
│   ├── js/main.js              # EN/FR switch
│   └── img/                    # portrait, favicon set
├── docs/                       # CV PDF, DESIGN-SYSTEM.md, SEO-GUIDE.md, TODO.md
├── changelog/unreleased/       # one changelog fragment per PR
├── CHANGELOG.md                # collated changelog
├── llms.txt, profile.json      # machine-readable profile
├── sitemap.xml, robots.txt
├── favicon.ico                 # 16/32/48 BB mark
└── tools/
    ├── cv.html                 # print source of the CV PDF (regeneration command inside)
    └── make_favicons.py        # regenerates the favicon set from the BB mark
```

## Notes

- Every visible section exists twice — in `#en` and in `#fr`, with a `-fr` ID suffix. Add content to both or the nav lands on an empty section.
- The LinkedIn Learning certificate browser was removed; `learning.html` URLs redirect to the home page so old links don't 404.
- `.github/workflows/main.yml` runs a Lighthouse report against the live site on every push to `main`.
- `docs/Brahim_Bousnguar_CV.pdf` and the favicons are generated files — edit `tools/cv.html` / `tools/make_favicons.py` and regenerate, never edit the outputs by hand.
- Contribution conventions: [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md).

## Contact

- Email: [b.bousnguar@gmail.com](mailto:b.bousnguar@gmail.com)
- LinkedIn: [linkedin.com/in/brahim-bousnguar](https://www.linkedin.com/in/brahim-bousnguar/)
- GitHub: [github.com/brbousnguar](https://github.com/brbousnguar)
