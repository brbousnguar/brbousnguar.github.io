#!/usr/bin/env python3
"""
Script to extract LinkedIn Learning certificate information from archived folder
and generate a JSON file for the learning page.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# Domain mapping based on course titles
DOMAIN_KEYWORDS = {
    'programming': ['java', 'python', 'javascript', 'programming', 'spring', 'maven', 'object-oriented', 'refactoring', 'code'],
    'cloud': ['aws', 'azure', 'google cloud', 'cloud', 'gcp', 'ccv2', 'btp'],
    'frontend': ['css', 'html', 'frontend', 'web developers', 'visual studio code', 'web'],
    'devops': ['git', 'docker', 'kubernetes', 'jenkins', 'ci/cd', 'devops', 'infrastructure', 'version control'],
    'ai': ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'gpt', 'openai', 'claude', 'gemini', 'copilot', 'mcp', 'agentic'],
    'agile': ['agile', 'scrum', 'project management', 'kanban'],
    'ecommerce': ['e-commerce', 'ecommerce', 'seo', 'commerce', 'sap commerce'],
    'communication': ['communication', 'meeting', 'presentation', 'business', 'marketing'],
    'tools': ['visual studio code', 'postman', 'confluence', 'microsoft 365', 'excel', 'windows', 'macos'],
    'security': ['security', 'owasp', 'api security'],
    'data': ['data', 'analytics', 'excel', 'chatgpt data'],
    'api': ['api', 'rest', 'swagger', 'openapi', 'postman', 'api testing', 'api documentation']
}

def categorize_domain(title, folder_name):
    """Categorize certificate into domain based on title and folder name."""
    text = (title + ' ' + folder_name).lower()
    
    # Check each domain
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return domain
    
    return 'other'

def extract_year_from_path(path):
    """Extract year from folder path."""
    # Check if path contains year folder
    parts = path.split('/')
    for part in parts:
        if part.isdigit() and len(part) == 4:
            year = int(part)
            if 2020 <= year <= 2030:
                return str(year)
    
    # Try to extract from folder name
    match = re.search(r'(\d{4})', path)
    if match:
        year = int(match.group(1))
        if 2020 <= year <= 2030:
            return str(year)
    
    return '2024'  # Default

def extract_duration(folder_name):
    """Extract duration from folder name."""
    # Look for patterns like "[Beginner-4h 22m]" or "[Intermediate-1h 33m]"
    match = re.search(r'\[.*?-.*?(\d+h?\s*\d*m?)\s*\]', folder_name, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_level(folder_name):
    """Extract level from folder name."""
    levels = ['beginner', 'intermediate', 'advanced', 'general']
    folder_lower = folder_name.lower()
    for level in levels:
        if level in folder_lower:
            return level.capitalize()
    return 'General'

def clean_title(title):
    """Clean certificate title."""
    # Remove "CertificateOfCompletion_" prefix if present
    title = title.replace('CertificateOfCompletion_', '')
    # Remove year suffixes like "-1" or "2022"
    title = re.sub(r'\s*-\s*\d+$', '', title)
    title = re.sub(r'\s*\d{4}$', '', title)
    return title.strip()

def main():
    archived_path = Path('archived')
    certificates = []
    
    if not archived_path.exists():
        print(f"Error: {archived_path} directory not found!")
        return
    
    # Find all certificate PDFs
    cert_files = list(archived_path.rglob('CertificateOfCompletion*.pdf'))
    
    print(f"Found {len(cert_files)} certificate files")
    
    for cert_file in cert_files:
        folder_name = cert_file.parent.name
        cert_name = cert_file.stem.replace('CertificateOfCompletion_', '')
        clean_cert_name = clean_title(cert_name)
        
        # Extract metadata
        domain = categorize_domain(clean_cert_name, folder_name)
        year = extract_year_from_path(str(cert_file))
        duration = extract_duration(folder_name)
        level = extract_level(folder_name)
        
        # Extract skills/keywords
        skills = []
        text_lower = (clean_cert_name + ' ' + folder_name).lower()
        
        # Add domain as primary skill
        if domain != 'other':
            skills.append(domain.replace('_', ' ').title())
        
        # Extract specific technologies
        tech_keywords = ['java', 'python', 'spring', 'git', 'docker', 'kubernetes', 'api', 'ai', 'chatgpt', 
                        'aws', 'azure', 'javascript', 'typescript', 'react', 'node', 'postman', 'maven']
        for keyword in tech_keywords:
            if keyword in text_lower:
                skills.append(keyword.title())
        
        certificate = {
            'id': len(certificates) + 1,
            'title': clean_cert_name,
            'folder': folder_name,
            'path': str(cert_file.relative_to(Path('.'))),
            'domain': domain,
            'year': year,
            'level': level,
            'duration': duration,
            'skills': list(set(skills))[:5],  # Limit to 5 skills
            'provider': 'LinkedIn Learning'
        }
        
        certificates.append(certificate)
    
    # Sort by year (newest first), then by title
    certificates.sort(key=lambda x: (x['year'], x['title']), reverse=True)
    
    # Generate statistics
    stats = {
        'total': len(certificates),
        'domains': len(set(c['domain'] for c in certificates)),
        'years': sorted(set(c['year'] for c in certificates), reverse=True),
        'last_updated': datetime.now().isoformat()
    }
    
    # Create output structure
    output = {
        'metadata': stats,
        'certificates': certificates
    }
    
    # Write JSON file
    output_file = Path('js/learning-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated {output_file} with {len(certificates)} certificates")
    print(f"  Domains: {stats['domains']}")
    print(f"  Years: {', '.join(stats['years'])}")
    
    # Print domain distribution
    domain_counts = {}
    for cert in certificates:
        domain_counts[cert['domain']] = domain_counts.get(cert['domain'], 0) + 1
    
    print("\nDomain distribution:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: {count}")

if __name__ == '__main__':
    main()
