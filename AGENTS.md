# Repository Guidelines

## Project Structure & Module Organization
This is a static GitHub Pages portfolio site. Key paths:
- `index.html`, `about.html`: primary pages and content.
- `css/`: site styles (`style.css`, `about.css`).
- `img/`, `icons/`: images, logos, and icons.
- SEO helpers: `sitemap.xml`, `robots.txt`, `seo-helper.html`, `seo-status.html`.
- Assets like `Brahim_Bousnguar_CV.pdf` live at repo root.

## Build, Test, and Development Commands
There is no build step.
- Local preview: `python -m http.server 5173` (then open http://localhost:5173).
- If you edit HTML/CSS, hard refresh to bypass cache (Ctrl+F5).

## Coding Style & Naming Conventions
- HTML/CSS only; keep formatting consistent with existing files (2‑space indent in HTML, 2‑space indent in CSS).
- Use kebab‑case for class names (e.g., `project-card`, `value-box`).
- Prefer CSS classes over repeated inline styles.
- Keep content bilingual (EN/FR) and ensure section IDs exist for both languages (`section-id` and `section-id-fr`).

## Testing Guidelines
No automated tests exist. Validate changes manually:
- Open `index.html` and `about.html` locally.
- Check language toggle, theme toggle, and sidebar anchors.
- Verify links (especially `target="_blank"`) and images load.

## Commit & Pull Request Guidelines
Recent commits use a simple type prefix when present (`feat:`, `style:`, `refactor:`), but some are untyped. Use a short imperative subject, optionally prefixed with a type for consistency, e.g., `feat: add hero section`.
For PRs:
- Include a brief summary and list of changes.
- Add before/after screenshots for UI changes.
- Mention any external links or assets added.

## Security & Configuration Tips
- External links should include `rel="noopener noreferrer"` when using `target="_blank"`.
- Keep `sitemap.xml` and `robots.txt` updated when pages are added.
