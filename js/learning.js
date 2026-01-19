/**
 * Learning Page JavaScript
 * Handles filtering, searching, and displaying certificates
 */

let allCertificates = [];
let filteredCertificates = [];
let currentView = 'list';
let selectedSkills = new Set(); // Track selected skills for AND filtering

// Initialize the learning page
function initLearningPage() {
  loadCertificates();
  setupEventListeners();
}

// Load certificates from JSON file
async function loadCertificates() {
  try {
    const response = await fetch('js/learning-data.json');
    if (!response.ok) {
      throw new Error('Failed to load certificate data');
    }
    const data = await response.json();
    allCertificates = data.certificates || [];
    filteredCertificates = [...allCertificates];
    
    // Update statistics
    updateStatistics(data.metadata);
    
    // Render certificates first (in case skills filter has issues)
    const lang = document.documentElement.getAttribute('lang') || 'en';
    const suffix = lang === 'fr' ? '-fr' : '';
    renderCertificates(suffix);
    updateResultsCount(suffix);
    
    // Set default view to list
    switchView('list', suffix);
    
    // Render skills filter (after certificates are rendered)
    setTimeout(() => {
      renderSkillsFilter();
    }, 100);
  } catch (error) {
    console.error('Error loading certificates:', error);
    document.getElementById('certificates-grid').innerHTML = 
      '<div class="no-results">Unable to load certificates. Please check the data file.</div>';
  }
}

// Update statistics display
function updateStatistics(metadata) {
  if (metadata) {
    const totalEl = document.getElementById('total-certificates');
    const domainsEl = document.getElementById('total-domains');
    const yearsEl = document.getElementById('active-years');
    
    if (totalEl) totalEl.textContent = metadata.total || allCertificates.length;
    if (domainsEl) domainsEl.textContent = (metadata.domains || new Set(allCertificates.map(c => c.domain)).size) + '+';
    if (yearsEl) yearsEl.textContent = (metadata.years?.length || new Set(allCertificates.map(c => c.year)).size) + '+';
  }
}

// Setup event listeners
function setupEventListeners() {
  const lang = document.documentElement.getAttribute('lang') || 'en';
  const suffix = lang === 'fr' ? '-fr' : '';
  
  // Search input
  const searchInput = document.getElementById('search-input' + suffix);
  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
  }
  
  // Domain filter
  const domainFilter = document.getElementById('domain-filter' + suffix);
  if (domainFilter) {
    domainFilter.addEventListener('change', handleFilter);
  }
  
  // Year filter
  const yearFilter = document.getElementById('year-filter' + suffix);
  if (yearFilter) {
    yearFilter.addEventListener('change', handleFilter);
  }
  
  // Sort filter
  const sortFilter = document.getElementById('sort-filter' + suffix);
  if (sortFilter) {
    sortFilter.addEventListener('change', handleSort);
  }
  
  // Clear filters button
  const clearBtn = document.getElementById('clear-filters' + suffix);
  if (clearBtn) {
    clearBtn.addEventListener('click', clearFilters);
  }
  
  // View toggle buttons
  const gridViewBtn = document.getElementById('grid-view' + suffix);
  const listViewBtn = document.getElementById('list-view' + suffix);
  
  if (gridViewBtn) {
    gridViewBtn.addEventListener('click', () => switchView('grid', suffix));
  }
  if (listViewBtn) {
    listViewBtn.addEventListener('click', () => switchView('list', suffix));
  }
  
  // Re-setup listeners when language changes
  const langObserver = new MutationObserver(() => {
    setupEventListeners();
  });
  langObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['lang']
  });
}

// Handle search
function handleSearch(e) {
  const query = e.target.value.toLowerCase().trim();
  applyFilters();
}

// Handle filter changes
function handleFilter() {
  applyFilters();
}

// Handle sort changes
function handleSort() {
  applyFilters();
}

// Get all skills with counts
function getAllSkillsWithCounts() {
  const skillCounts = new Map();
  
  allCertificates.forEach(cert => {
    if (cert.skills && Array.isArray(cert.skills)) {
      cert.skills.forEach(skill => {
        const skillLower = skill.toLowerCase().trim();
        if (skillLower) {
          skillCounts.set(skillLower, (skillCounts.get(skillLower) || 0) + 1);
        }
      });
    }
  });
  
  // Convert to array and sort by count (descending)
  return Array.from(skillCounts.entries())
    .map(([skill, count]) => ({ skill, count }))
    .sort((a, b) => b.count - a.count);
}

// Render skills filter
function renderSkillsFilter() {
  if (!allCertificates || allCertificates.length === 0) {
    console.warn('No certificates loaded yet, skipping skills filter render');
    return;
  }
  
  const skills = getAllSkillsWithCounts();
  const lang = document.documentElement.getAttribute('lang') || 'en';
  const suffix = lang === 'fr' ? '-fr' : '';
  const skillsListEl = document.getElementById('skills-list' + suffix);
  
  if (!skillsListEl) {
    console.warn('Skills list element not found:', 'skills-list' + suffix);
    return;
  }
  
  skillsListEl.innerHTML = skills.map(({ skill, count }) => {
    const isSelected = selectedSkills.has(skill);
    return `
      <button 
        type="button" 
        class="skill-filter-btn ${isSelected ? 'active' : ''}" 
        data-skill="${escapeHtml(skill)}"
        aria-label="Filter by ${escapeHtml(skill)} (${count} certificates)"
      >
        <span class="skill-name">${escapeHtml(skill)}</span>
        <span class="skill-count">${count}</span>
      </button>
    `;
  }).join('');
  
  // Add click listeners
  skillsListEl.querySelectorAll('.skill-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const skill = btn.getAttribute('data-skill');
      toggleSkillFilter(skill);
    });
  });
}

// Toggle skill filter (AND logic for multiple selections)
function toggleSkillFilter(skill) {
  if (selectedSkills.has(skill)) {
    selectedSkills.delete(skill);
  } else {
    selectedSkills.add(skill);
  }
  
  // Update UI
  renderSkillsFilter();
  
  // Apply filters
  applyFilters();
}

// Apply all filters and search
function applyFilters() {
  const lang = document.documentElement.getAttribute('lang') || 'en';
  const suffix = lang === 'fr' ? '-fr' : '';
  
  const searchQuery = document.getElementById('search-input' + suffix)?.value.toLowerCase().trim() || '';
  const domainFilter = document.getElementById('domain-filter' + suffix)?.value || 'all';
  const yearFilter = document.getElementById('year-filter' + suffix)?.value || 'all';
  const sortFilter = document.getElementById('sort-filter' + suffix)?.value || 'date-desc';
  
  // Filter certificates
  filteredCertificates = allCertificates.filter(cert => {
    // Search filter
    const matchesSearch = !searchQuery || 
      cert.title.toLowerCase().includes(searchQuery) ||
      cert.domain.toLowerCase().includes(searchQuery) ||
      cert.skills?.some(skill => skill.toLowerCase().includes(searchQuery)) ||
      cert.folder?.toLowerCase().includes(searchQuery);
    
    // Domain filter
    const matchesDomain = domainFilter === 'all' || cert.domain === domainFilter;
    
    // Year filter
    const matchesYear = yearFilter === 'all' || cert.year === yearFilter;
    
    // Skills filter (AND logic - certificate must have ALL selected skills)
    const matchesSkills = selectedSkills.size === 0 || 
      (cert.skills && Array.isArray(cert.skills) &&
       Array.from(selectedSkills).every(selectedSkill => 
         cert.skills.some(certSkill => certSkill.toLowerCase().trim() === selectedSkill)
       ));
    
    return matchesSearch && matchesDomain && matchesYear && matchesSkills;
  });
  
  // Sort certificates
  sortCertificates(sortFilter);
  
  // Update active filters display
  updateActiveFilters(domainFilter, yearFilter, searchQuery, suffix);
  
  // Render
  renderCertificates(suffix);
  updateResultsCount(suffix);
}

// Sort certificates
function sortCertificates(sortType) {
  switch (sortType) {
    case 'date-desc':
      filteredCertificates.sort((a, b) => {
        if (b.year !== a.year) return b.year.localeCompare(a.year);
        return b.title.localeCompare(a.title);
      });
      break;
    case 'date-asc':
      filteredCertificates.sort((a, b) => {
        if (a.year !== b.year) return a.year.localeCompare(b.year);
        return a.title.localeCompare(b.title);
      });
      break;
    case 'title-asc':
      filteredCertificates.sort((a, b) => a.title.localeCompare(b.title));
      break;
    case 'title-desc':
      filteredCertificates.sort((a, b) => b.title.localeCompare(a.title));
      break;
    case 'domain':
      filteredCertificates.sort((a, b) => {
        if (a.domain !== b.domain) return a.domain.localeCompare(b.domain);
        return a.title.localeCompare(b.title);
      });
      break;
  }
}

// Clear all filters
function clearFilters() {
  const lang = document.documentElement.getAttribute('lang') || 'en';
  const suffix = lang === 'fr' ? '-fr' : '';
  
  document.getElementById('search-input' + suffix).value = '';
  document.getElementById('domain-filter' + suffix).value = 'all';
  document.getElementById('year-filter' + suffix).value = 'all';
  document.getElementById('sort-filter' + suffix).value = 'date-desc';
  
  // Clear selected skills
  selectedSkills.clear();
  renderSkillsFilter();
  
  applyFilters();
}

// Update active filters display
function updateActiveFilters(domain, year, search, suffix = '') {
  const activeFiltersEl = document.getElementById('active-filters' + suffix);
  if (!activeFiltersEl) return;
  
  activeFiltersEl.innerHTML = '';
  
  const lang = document.documentElement.getAttribute('lang') || 'en';
  const isFr = lang === 'fr';
  
  if (domain !== 'all') {
    const label = isFr ? 'Domaine: ' : 'Domain: ';
    const tag = createFilterTag(label + formatDomainName(domain), () => {
      document.getElementById('domain-filter' + suffix).value = 'all';
      applyFilters();
    });
    activeFiltersEl.appendChild(tag);
  }
  
  if (year !== 'all') {
    const label = isFr ? 'Année: ' : 'Year: ';
    const tag = createFilterTag(label + year, () => {
      document.getElementById('year-filter' + suffix).value = 'all';
      applyFilters();
    });
    activeFiltersEl.appendChild(tag);
  }
  
  if (search) {
    const label = isFr ? 'Recherche: ' : 'Search: ';
    const tag = createFilterTag(label + search, () => {
      document.getElementById('search-input' + suffix).value = '';
      applyFilters();
    });
    activeFiltersEl.appendChild(tag);
  }
  
  // Show selected skills
  if (selectedSkills.size > 0) {
    const label = isFr ? 'Compétences: ' : 'Skills: ';
    Array.from(selectedSkills).forEach(skill => {
      const tag = createFilterTag(label + skill, () => {
        selectedSkills.delete(skill);
        renderSkillsFilter();
        applyFilters();
      });
      activeFiltersEl.appendChild(tag);
    });
  }
}

// Create filter tag element
function createFilterTag(text, onClick) {
  const tag = document.createElement('div');
  tag.className = 'filter-tag';
  tag.innerHTML = `
    <span>${text}</span>
    <button type="button" aria-label="Remove filter">×</button>
  `;
  tag.querySelector('button').addEventListener('click', onClick);
  return tag;
}

// Format domain name for display
function formatDomainName(domain) {
  return domain.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
}

// Switch view (grid/list)
function switchView(view, suffix = '') {
  currentView = view;
  const grid = document.getElementById('certificates-grid' + suffix);
  const gridBtn = document.getElementById('grid-view' + suffix);
  const listBtn = document.getElementById('list-view' + suffix);
  
  if (!grid) return;
  
  if (view === 'grid') {
    grid.classList.remove('list-view');
    if (gridBtn) gridBtn.classList.add('active');
    if (listBtn) listBtn.classList.remove('active');
  } else {
    grid.classList.add('list-view');
    if (listBtn) listBtn.classList.add('active');
    if (gridBtn) gridBtn.classList.remove('active');
  }
}

// Render certificates
function renderCertificates(suffix = '') {
  const container = document.getElementById('certificates-grid' + suffix);
  if (!container) {
    console.error('Certificate container not found:', 'certificates-grid' + suffix);
    return;
  }
  
  const lang = document.documentElement.getAttribute('lang') || 'en';
  const isFr = lang === 'fr';
  
  if (!filteredCertificates || filteredCertificates.length === 0) {
    const message = isFr ? 'Aucun certificat trouvé correspondant à vos filtres.' : 'No certificates found matching your filters.';
    container.innerHTML = `<div class="no-results">${message}</div>`;
    return;
  }
  
  container.innerHTML = filteredCertificates.map(cert => createCertificateCard(cert, isFr)).join('');
}

// Format date from YYYY-MM-DD to dd-mm-yyyy
function formatDate(dateString) {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString + 'T00:00:00'); // Add time to avoid timezone issues
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
  } catch (e) {
    // Fallback: try to parse YYYY-MM-DD format directly
    const parts = dateString.split('-');
    if (parts.length === 3) {
      return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }
    return dateString;
  }
}

// Create certificate card HTML
function createCertificateCard(cert, isFr = false) {
  const domainName = formatDomainName(cert.domain);
  
  // Remove duplicates, exclude domain name from skills
  // Show all skills (no limit) - they will wrap to multiple lines if needed
  const uniqueSkills = cert.skills?.filter(skill => {
    const skillLower = skill.toLowerCase();
    const domainLower = cert.domain.toLowerCase();
    return skillLower !== domainLower && skillLower !== domainName.toLowerCase();
  }) || [];
  
  const skillsHtml = uniqueSkills.map(skill => 
    `<span class="skill-badge-learning">${skill}</span>`
  ).join('');
  
  // Format date as dd-mm-yyyy
  const formattedDate = cert.date ? formatDate(cert.date) : (cert.year || '');
  
  const viewText = isFr ? 'Voir le Certificat' : 'View Certificate';
  
  // Only show skills from the certificate, not the domain badge
  // Domain is already shown in filters, so we don't need to duplicate it here
  const allSkillsHtml = skillsHtml;
  
  return `
    <div class="certificate-card-learning" data-domain="${cert.domain}" data-year="${cert.year}">
      <div class="certificate-header-learning">
        <h3 class="certificate-title-learning">${escapeHtml(cert.title)}</h3>
      </div>
      <div class="certificate-meta-learning">
        ${formattedDate ? `<span>${formattedDate}</span>` : ''}
        ${cert.duration ? `<span>${cert.duration}</span>` : ''}
      </div>
      ${allSkillsHtml ? `<div class="certificate-skills-learning">${allSkillsHtml}</div>` : '<div class="certificate-skills-learning"></div>'}
      <div class="certificate-actions">
        <a href="${cert.path}" target="_blank" rel="noopener noreferrer" class="certificate-link-learning">
          ${viewText}
        </a>
      </div>
    </div>
  `;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Update results count
function updateResultsCount(suffix = '') {
  const countEl = document.getElementById('results-count' + suffix);
  if (countEl) {
    const lang = document.documentElement.getAttribute('lang') || 'en';
    const isFr = lang === 'fr';
    const count = filteredCertificates.length;
    const total = allCertificates.length;
    
    if (count === total) {
      const text = isFr ? `Affichage de <strong>${total}</strong> certificats` : `Showing <strong>${total}</strong> certificates`;
      countEl.innerHTML = text;
    } else {
      const text = isFr 
        ? `Affichage de <strong>${count}</strong> sur <strong>${total}</strong> certificats`
        : `Showing <strong>${count}</strong> of <strong>${total}</strong> certificates`;
      countEl.innerHTML = text;
    }
  }
}

// Make functions available globally
window.initLearningPage = initLearningPage;
window.renderSkillsFilter = renderSkillsFilter;
window.filteredCertificates = filteredCertificates;
