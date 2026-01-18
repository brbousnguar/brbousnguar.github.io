# Quick Reference - Cursor AI Helper

## 🎨 Design System Quick Look

### Colors (CSS Variables)
- Accent: `var(--accent-blue)` = `#d4a04f` (warm gold)
- Text Primary: `var(--text-primary)`
- Text Secondary: `var(--text-secondary)`
- Background: `var(--primary-bg)`

### Fonts
- Family: `Inter` + system fonts fallback
- Base Size: `15px`

### Spacing
- Base: `1rem` = `15px`
- Sections: `2-3rem`

## ✅ Quick Checklists

### New Page Checklist
- [ ] Title tag (60 chars max, includes name + role)
- [ ] Meta description (155-160 chars)
- [ ] Open Graph tags (5 required)
- [ ] Twitter Card tags (5 required)
- [ ] Canonical URL
- [ ] Hreflang tags (en, fr, x-default)
- [ ] Breadcrumb structured data
- [ ] Skip link (`<a href="#main-content" class="skip-link">`)
- [ ] Main content ID (`id="main-content"`)
- [ ] Update sitemap.xml

### New Section Checklist
- [ ] Semantic HTML (`<section>` with `id`)
- [ ] `.section` and `.section-content` classes
- [ ] Proper heading hierarchy (H2, H3)
- [ ] Update sidebar navigation
- [ ] Responsive design tested

### Image Checklist
- [ ] `width` and `height` attributes
- [ ] Descriptive `alt` text
- [ ] `loading="eager"` (above fold) or `loading="lazy"` (below fold)

### Link Checklist
- [ ] External links: `rel="noopener noreferrer"`
- [ ] Internal links: relative paths
- [ ] Email links: `aria-label` included

## 🔍 Common Patterns

### Section HTML
```html
<section class="section" id="section-id">
  <div class="section-content">
    <h2>Title</h2>
    <p>Content</p>
  </div>
</section>
```

### External Link
```html
<a href="https://..." target="_blank" rel="noopener noreferrer">Link Text</a>
```

### Image with Alt
```html
<img src="img/file.jpg" alt="Descriptive alt text" width="100" height="100" loading="eager">
```

### Language Toggle Update
```javascript
document.documentElement.setAttribute('lang', lang);
document.documentElement.setAttribute('data-lang', lang);
```

## 🚫 Don'ts
- ❌ Don't use blue/cold colors (use warm gold/sepia)
- ❌ Don't skip heading levels (H1 → H2 → H3)
- ❌ Don't forget `rel="noopener"` on external links
- ❌ Don't hardcode colors (use CSS variables)
- ❌ Don't forget alt text on images
- ❌ Don't forget to update HTML lang on language switch

## ⚡ Quick Commands

### Test Responsive
- Mobile: 480px width
- Tablet: 768px width
- Desktop: 1024px+ width

### Validate SEO
- Check meta tags count (minimum 10 on each page)
- Verify structured data JSON-LD syntax
- Test language switching updates lang attribute

---

See `.cursorrules` for complete documentation.

