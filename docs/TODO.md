# Portfolio Enhancements TODO

Goal: Improve first impression, scanability, and credibility while keeping the current content strengths.

Audience: Recruiters (technical screening + hiring managers)
Tone/Persona: Tech Lead (clear, outcome-driven, systems-focused)
Scope: Content + structure + visual hierarchy. Keep the current stack (HTML/CSS/JS), no build tooling.

## Quick Wins (start here)
- [x] P0 / Scope: UX+Content — Fix text encoding so emojis and French accents render correctly (save files as UTF-8)
- [x] P0 / Scope: Security — Add `rel="noopener noreferrer"` to all external links with `target="_blank"`
- [x] P1 / Scope: UX — Update sidebar anchors to include `#projects`, `#faq`, `#contact`
- [x] P1 / Scope: UX — Add missing section IDs in FR blocks so sidebar works for both languages
- [x] P1 / Scope: Maintainability — Replace inline styles on repeated blocks with CSS classes (projects cards, value props)
- [ ] P2 / Scope: Visual — Decide on font usage: remove Poppins or apply it to headings consistently

## Acceptance Criteria
P0
- [x] All pages render French accents correctly and emojis display properly on refresh and hard reload
- [x] External links with `target="_blank"` include `rel="noopener noreferrer"`

P1
- [x] Sidebar links cover all major sections (including Projects, FAQ, Contact)
- [x] Clicking a sidebar link scrolls to the correct section in both EN and FR views
- [x] Reused visual blocks (projects, value prop) are styled via CSS classes instead of inline styles

## High-Impact Enhancements (next)
- [ ] P1 / Scope: Content+Layout — Add a hero section: 1-line positioning + 2–3 proof bullets + 2 CTAs (Contact / Download CV)
- [ ] P1 / Scope: Content+Layout — Convert “Featured Integration Projects” into 3 card tiles with outcomes surfaced
- [ ] P2 / Scope: Content — Add a credibility strip (client names/logos or text badges)
- [ ] P1 / Scope: Content — Reformat each project to Problem / Role / Solution / Impact for faster scan
- [ ] P2 / Scope: Layout — Improve first-view hierarchy (reduce CV density above the fold)

## Later / Nice-to-have
- [ ] P2 / Scope: Visual — Add lightweight visuals (architecture diagram or simple schematic per project)
- [ ] P2 / Scope: Content — Add a “Selected Metrics” block for key wins (API response time, deployment time, etc.)
- [ ] P3 / Scope: Content — Add downloadable one-page PDF case study summaries

## Notes from Review
- Strong SEO foundation (meta tags, JSON-LD, canonical)
- Clear specialization and domain depth
- Main improvement: shift from CV layout to portfolio layout on the homepage
