/*
 * Shared site behaviour: the EN/FR switch, and nothing else.
 * The pre-paint snippet in each page <head> sets data-lang on <html>
 * before first paint; CSS shows #en or #fr from that attribute, so this
 * file only flips it, persists the choice, and points in-page nav links
 * at the matching -fr section IDs.
 */

function setLanguage(lang) {
  const root = document.documentElement;
  root.setAttribute('lang', lang);
  root.setAttribute('data-lang', lang);
  try { localStorage.setItem('language', lang); } catch (e) { /* private mode */ }

  const suffix = lang === 'fr' ? '-fr' : '';
  document.querySelectorAll('a[data-target]').forEach(link => {
    const base = link.getAttribute('href').split('#')[0];
    link.setAttribute('href', `${base}#${link.dataset.target}${suffix}`);
  });

  document.querySelectorAll('[data-set-lang]').forEach(btn => {
    btn.setAttribute('aria-pressed', String(btn.dataset.setLang === lang));
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setLanguage(document.documentElement.getAttribute('data-lang') || 'en');
  document.querySelectorAll('[data-set-lang]').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.setLang));
  });
});
