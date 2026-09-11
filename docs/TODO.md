# Portfolio TODO

Open work only. The 2026-09 Blueprint redesign closed everything that was on the
previous list (hero, case studies, first-view hierarchy, encoding, link safety,
visuals); see `CHANGELOG.md` for what shipped.

Audience: recruiters and hiring managers, plus AI agents reading `llms.txt` /
`profile.json`. Keep the stack (static HTML/CSS/JS, no build) and the Blueprint
rules in `docs/DESIGN-SYSTEM.md`.

## Next
- [ ] P2 / SEO — Create a 1200×630 Open Graph image in the Blueprint style (ink band, BB mark, name and title); `og:image` is still the square `profile.jpeg`
- [ ] P2 / Content — Add a short "Selected metrics" line per case study once real figures are available (API response time, deployment frequency, countries live); do not invent numbers

## Decided against
- Client logo wall and technology icon grid — permission/trademark risk and the templated look; the Credly "Verify" links carry the credibility instead
- Dark mode — the site is light-only by design
