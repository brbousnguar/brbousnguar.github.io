/*
 * Shared site behavior: language toggle, theme toggle, sidebar
 * navigation (scrollspy + smooth scroll), and back-to-top button.
 * Loaded with `defer` on every page; switchLang/toggleTheme stay
 * global because header buttons use inline onclick attributes.
 * The pre-paint snippet in each page <head> applies the saved theme
 * and language attributes before first paint; this file only syncs
 * UI state and wires up interactions.
 */

function switchLang(lang) {
  document.querySelectorAll('.lang-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.lang-toggle button').forEach(btn => btn.classList.remove('active'));
  const selected = document.getElementById(lang);
  if (selected) selected.classList.add('active');
  const btn = document.querySelector(`.lang-toggle button[onclick*="${lang}"]`);
  if (btn) btn.classList.add('active');

  // Update HTML lang attribute for SEO and accessibility
  document.documentElement.setAttribute('lang', lang);
  document.documentElement.setAttribute('data-lang', lang);

  // Save language preference to localStorage
  localStorage.setItem('language', lang);

  // Update sidebar anchors and re-init navigation (index page only)
  if (document.querySelector('.sidebar-nav a[data-target]')) {
    updateSidebarLang(lang);
    initSmoothScroll();
    initNavigationHighlight();
  }

  // Re-initialize certificate browser for the new language (learning page only)
  if (window.initLearningPage) {
    setTimeout(() => {
      setupEventListeners();
      if (window.renderSkillsFilter) {
        renderSkillsFilter();
      }
      const suffix = lang === 'fr' ? '-fr' : '';
      if (window.filteredCertificates) {
        renderCertificates(suffix);
        updateResultsCount(suffix);
      }
    }, 100);
  }
}

function updateSidebarLang(lang) {
  const suffix = lang === 'fr' ? '-fr' : '';
  document.querySelectorAll('.sidebar-nav a[data-target]').forEach(link => {
    const base = link.getAttribute('data-target');
    link.setAttribute('href', `#${base}${suffix}`);
  });
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeToggle(newTheme);
}

function updateThemeToggle(theme) {
  const lightOption = document.getElementById('light-option');
  const darkOption = document.getElementById('dark-option');
  if (!lightOption || !darkOption) return;

  if (theme === 'light') {
    lightOption.classList.add('active');
    darkOption.classList.remove('active');
  } else {
    darkOption.classList.add('active');
    lightOption.classList.remove('active');
  }
}

function initNavigationHighlight() {
  // Get only sections from the currently active language content
  const activeContent = document.querySelector('.lang-content.active');
  if (!activeContent) return;

  const navLinks = document.querySelectorAll('.sidebar-nav a[href^="#"]');
  if (!navLinks.length) return;

  // Track if user just clicked a link
  window.navigationClickTime = 0;

  window.updateActiveNavLink = function (targetId) {
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === targetId) {
        link.classList.add('active');
      }
    });
  };

  // Remove old scroll listener if exists
  if (window.scrollHighlightHandler) {
    window.removeEventListener('scroll', window.scrollHighlightHandler);
  }

  // Create new scroll handler that always checks current active content
  window.scrollHighlightHandler = function () {
    // Don't update highlighting for 800ms after a click
    if (Date.now() - window.navigationClickTime < 800) {
      return;
    }

    const currentActiveContent = document.querySelector('.lang-content.active');
    if (!currentActiveContent) return;

    const currentSections = currentActiveContent.querySelectorAll('.section[id]');
    const scrollPosition = window.scrollY + 200; // Check what's near top of viewport

    let currentSection = '';

    currentSections.forEach(section => {
      const rect = section.getBoundingClientRect();
      const sectionTop = rect.top + window.scrollY;
      const sectionBottom = sectionTop + rect.height;

      // Check if the scroll position is within this section
      if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
        currentSection = '#' + section.id;
      }
    });

    if (currentSection && window.updateActiveNavLink) {
      updateActiveNavLink(currentSection);
    }
  };

  // Add the new scroll listener with throttling
  let isScrolling = false;
  window.addEventListener('scroll', () => {
    if (!isScrolling) {
      window.requestAnimationFrame(() => {
        if (window.scrollHighlightHandler) {
          window.scrollHighlightHandler();
        }
        isScrolling = false;
      });
    }
    isScrolling = true;
  });

  // Trigger initial highlight check
  if (window.scrollHighlightHandler) {
    setTimeout(() => window.scrollHighlightHandler(), 100);
  }
}

function initBackToTop() {
  // Create back to top button
  const backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.innerHTML = '↑';
  backToTop.setAttribute('aria-label', 'Back to top');
  backToTop.title = 'Back to top';
  document.body.appendChild(backToTop);

  // Show/hide on scroll
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  });

  // Scroll to top on click
  backToTop.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

function initSmoothScroll() {
  // Remove old listeners by cloning and replacing navigation links
  const navLinks = document.querySelectorAll('.sidebar-nav a[href^="#"]');
  navLinks.forEach(link => {
    const newLink = link.cloneNode(true);
    link.parentNode.replaceChild(newLink, link);
  });

  // Add fresh event listeners
  document.querySelectorAll('.sidebar-nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');

      // Update click timestamp to prevent scroll handler from overriding
      window.navigationClickTime = Date.now();

      // Find target in active language content
      const activeContent = document.querySelector('.lang-content.active');
      if (!activeContent) return;

      const target = activeContent.querySelector(targetId);
      if (target) {
        // Calculate offset for sticky header (approx 60px) + extra spacing
        const headerOffset = 80;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });

        // Update active state immediately on click
        if (window.updateActiveNavLink) {
          updateActiveNavLink(targetId);
        }
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  // The pre-paint head snippet already set data-theme / lang / data-lang;
  // restore the language content visibility and sync toggle button states.
  const savedLang = localStorage.getItem('language') || 'en';
  switchLang(savedLang);

  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  updateThemeToggle(currentTheme);

  // Follow system theme changes while the user has no explicit preference
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      const newTheme = e.matches ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', newTheme);
      updateThemeToggle(newTheme);
    }
  });

  initBackToTop();

  if (document.querySelector('.sidebar-nav a[href^="#"]')) {
    initSmoothScroll();
    initNavigationHighlight();
  }

  // Certificate browser (learning page only)
  if (window.initLearningPage) {
    initLearningPage();
  }
});
