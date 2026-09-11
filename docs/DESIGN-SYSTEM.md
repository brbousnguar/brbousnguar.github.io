# Blueprint — design system

The design system for brbousnguar.github.io. **This file and `assets/css/style.css`
change in the same commit.** A spec that drifts is worse than none.

Blueprint is a light-only variant of the Banknote system used by the Fortunex and
Vitalex webapps (`~/Server/webapps/fortunex/DESIGN.md`): same form language, same
type split, a palette tuned for a professional profile instead of a finance app.

## Why it exists

The previous theme had drifted into the generated-portfolio look: an amber accent
on warm grey, a light/dark toggle with sun/moon emoji, rounded cards with soft
shadows everywhere, icon-in-tile stat cards with count-up animations, scroll-reveal
on every block, a sidebar of twelve links, glass surfaces, a visible FAQ written for
crawlers, and a 644-certificate LinkedIn Learning browser. Every piece was
competent. Together they read as a template, and they buried the actual work.

Blueprint removes all of it. What is left is type, rules and one colour.

## Palette

Measured with `~/Server/.claude/skills/brb-flat-poster-theme/scripts/check-palette.py`
against paper `#FBFAF7` and ink `#131211` (ink on paper **17.93:1**).

| Token | Hex | Role | As text on paper | White on it | Class |
|---|---|---|---|---|---|
| `--ink` | `#131211` | text, rules, the contact band | 17.93 | — | text + fill |
| `--ink-2` | `#3A3833` | secondary text | 11.1 | — | text |
| `--muted` | `#5E5B55` | meta, labels | 6.48 (5.88 on `--paper-2`) | — | text |
| `--cobalt` | `#1446C8` | links, primary button, numbers, the core flow node | 7.34 (6.67 on `--paper-2`) | 7.66 | **DUAL-ROLE** |
| `--on-cobalt` | `#FFFFFF` | text and rules on the cobalt fill | — | — | on-fill |
| `--marker` | `#FFD84D` | the highlighter stroke | 1.33 | 1.38 | **FILL-ONLY** |
| `--sky` | `#9DB6FF` | links inside the ink band | 9.42 on ink | — | **TEXT-ON-INK ONLY** |
| `--paper` | `#FBFAF7` | page ground | — | — | ground |
| `--paper-2` | `#F1EFE9` | alternate section band | — | — | ground |
| `--rule` | `#D9D6CE` | hairlines | — | — | non-text |

Rules that have already cost bugs elsewhere:

- **`--marker` never sets type.** It exists for exactly one element: `.hl`, the
  highlighter behind one phrase in the hero. Ink on it is 13.53:1.
- **Cobalt fails on ink** (2.44:1). Inside `.contact` links use `--sky`, headings and
  body use `--paper`. Focus rings switch to `--sky` there too.
- **No dark mode.** `color-scheme: light` is declared; there is no `data-theme`, no
  `prefers-color-scheme` branch, no toggle. Do not add one back.

## Form language

1. **Flat.** No shadows, gradients, blur or glass. Depth comes from type scale and
   colour weight.
2. **Hard-edged.** `border-radius: 0` everywhere, including the portrait. There is no
   named exception.
3. **Separated by rule and colour change**, not by a box around every item. Rows
   (cases, projects, experience, stack, credentials) are divided by hairlines; only
   the three flow nodes carry a full border.
4. **Unequal.** The Roche Bobois case is larger than the other two; the middle flow
   node is wider and filled; the contact block is the only ink surface. A grid of
   identical cards is the failure mode this replaced.
5. **Still.** No scroll-reveal, no counters, no back-to-top button. Hover is an
   instant ink inversion (`.btn`, `.index a`, `.site-nav a`).

## Type

Three roles, never blurred. Same families as Fortunex and Vitalex; Inter is
deliberately gone.

| Role | Family | Used for |
|---|---|---|
| Display | Archivo 600–800, `-0.02` to `-0.045em` | name, headings, numbers, buttons, project names |
| Reading | Hanken Grotesk 400–600, 17px | body copy, lists |
| Technical | IBM Plex Mono 400–500 | eyebrows, dates, tags, stack labels, footer |

Sentence case for display. All-caps only for mono eyebrows and labels. Every
display heading carries `overflow-wrap: break-word`.

## Imagery

One photo (the 336×336 portrait, shown at 168px so it stays sharp on 2× screens).
Everything explanatory is built from HTML and CSS — the integration flow in
"What I do" replaces the old value-proposition paragraph.

## Concision

The page states each fact once. Experience keeps three bullets per role; the case
studies keep one sentence each for Problem / Built / Result. Never shorten by
changing a date, title, client, certification name or metric — those are the
product.

## Bilingual

Both languages ship in the DOM. The inline pre-paint script sets `data-lang` on
`<html>`; CSS shows `#en` or `#fr` from that attribute, so there is no flash and no
JS dependency for visibility. Short inline strings (nav, skip link) use
`.t-en` / `.t-fr` spans. Section IDs in the French body carry a `-fr` suffix;
`main.js` rewrites every `a[data-target]` to point at the right one.

## Component list

Anything not here does not exist; adding a component means adding it here.

Header (brand mark, nav, EN/FR switch) · eyebrow · hero (name, lede with `.hl`,
note, actions, portrait) · facts strip · section head · integration flow ·
case row · project index row · upstream line · experience row · stack list ·
credentials list · contact band (headline, email, one-line summary) + footer · about page intro · prose row ·
timeline.

## Verification

Run before shipping any change to this file or `style.css`, with the site served
from its root:

```bash
PORT=8798 ~/Server/.claude/skills/brb-flat-poster-theme/scripts/verify.sh . index.html pages/about.html
```

- **Contrast**, alpha-composited: **0 failures** on both pages.
- **Reflow at true 320px**, in **both languages**: page `scrollWidth` 320. The only
  reported overflow is the nav links inside `.site-nav`, which is its own horizontal
  scroller below 390px — expected. At ≤480px the `Stack` link (`.nav-optional`) hides
  so the other five fit a 390px phone without scrolling.
- **Lighthouse mobile** (chrome-devtools MCP, loopback): Accessibility, Best
  Practices and SEO **100** on both pages.
- Switch to FR and confirm every nav anchor lands on a non-empty `-fr` section.

## SEO and accessibility requirements

Every page keeps: `<title>`, meta description and keywords, Open Graph, Twitter
Card, canonical, `hreflang` en / fr / x-default, JSON-LD (`Person` +
`BreadcrumbList`), a skip link, one `<h1>`, and visible focus rings. There is no
`FAQPage` markup — it requires visible Q&A, which the site no longer has.
AI-readability lives in `llms.txt`, `profile.json`, the Person JSON-LD and the
AI-crawler allowlist in `robots.txt`; the footer links the first two.

External links carry `target="_blank" rel="noopener noreferrer"`. Use tokens, never
hex literals, outside `:root`.

## File organisation

```
index.html                 # the portfolio
pages/about.html           # career story
about.html, learning.html  # redirect stubs (learning → home, noindex)
pages/learning.html        # redirect stub → home, noindex
assets/css/style.css       # the only stylesheet
assets/js/main.js          # EN/FR switch
assets/img/                # portrait, favicon
docs/                      # CV PDF, this file, SEO-GUIDE.md, TODO.md
llms.txt, profile.json     # machine-readable profile
sitemap.xml, robots.txt
```

---

**Last updated**: 2026-09-11
