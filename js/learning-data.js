/**
 * Learning Data - Certificate Information
 * This file contains sample certificate data structure
 * In production, this should be generated from the archived folder
 */

// Sample data structure - will be replaced by actual data from learning-data.json
window.learningDataSample = {
  metadata: {
    total: 409,
    domains: 12,
    years: ['2026', '2025', '2024', '2023'],
    last_updated: new Date().toISOString()
  },
  certificates: []
};

// If learning-data.json doesn't exist, use sample data
if (typeof fetch !== 'undefined') {
  fetch('js/learning-data.json')
    .then(response => {
      if (!response.ok) {
        console.warn('learning-data.json not found, using sample data');
        return null;
      }
      return response.json();
    })
    .catch(() => {
      console.warn('Error loading learning-data.json, using sample data');
    });
}
