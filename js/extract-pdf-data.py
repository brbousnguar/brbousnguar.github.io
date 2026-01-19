#!/usr/bin/env python3
"""
Extract certificate data from PDF files and update learning-data.json
This script reads PDF files to extract: date, title, skills, duration
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# Try to import PDF libraries
try:
    import pypdf
    PDF_LIB = 'pypdf'
except ImportError:
    try:
        import PyPDF2 as pypdf
        PDF_LIB = 'PyPDF2'
    except ImportError:
        try:
            import pdfplumber
            PDF_LIB = 'pdfplumber'
        except ImportError:
            PDF_LIB = None
            print("Warning: No PDF library found. Install with: pip install pypdf")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using available library."""
    if not PDF_LIB:
        return None
    
    try:
        if PDF_LIB == 'pdfplumber':
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        else:
            # pypdf or PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
    except Exception as e:
        print(f"Error reading {pdf_path.name}: {e}")
        return None

def extract_date_from_text(text):
    """Extract completion date from PDF text."""
    if not text:
        return None, None
    
    # Patterns for dates like "May 17, 2025 at 07:24AM UTC"
    patterns = [
        (r'(\w+)\s+(\d+),\s+(\d{4})\s+at\s+(\d+):(\d+)[AP]M', '%B %d, %Y'),
        (r'(\w+)\s+(\d+),\s+(\d{4})', '%B %d, %Y'),
        (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', '%m/%d/%Y'),
        (r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', '%Y-%m-%d'),
    ]
    
    for pattern, date_format in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                date_str = match.group(0).split(' at')[0].strip()
                # Try parsing
                for fmt in ['%B %d, %Y', '%b %d, %Y', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        return str(dt.year), dt.strftime('%Y-%m-%d')
                    except:
                        continue
            except:
                continue
    
    return None, None

def extract_title_from_text(text):
    """Extract course title from PDF text. Handles multi-line titles."""
    if not text:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Title lines come BEFORE "Course completed by"
    # They may span multiple lines
    title_lines = []
    
    excluded_keywords = ['certificate', 'id:', 'head of', 'provider', 'top skills covered']
    month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    
    for i, line in enumerate(lines):
        # Skip LinkedIn Learning header
        if 'linkedin learning' in line.lower() and len(line) < 30:
            continue
        
        # Stop if we hit "Course completed" - title comes before this
        if 'course completed' in line.lower() or 'completed by' in line.lower():
            break
        
        # Check if this looks like a date/time line (has month name, year, and time)
        is_date_time_line = False
        has_month = any(month in line.lower() for month in month_names)
        has_year = bool(re.search(r'\d{4}', line))
        has_time = bool(re.search(r'\d{1,2}:\d{2}[AP]M', line, re.IGNORECASE)) or 'utc' in line.lower()
        
        # If it has month + year + time, it's definitely a date/time line
        if has_month and has_year and has_time:
            is_date_time_line = True
        
        # Also check for duration pattern that's clearly metadata (not part of title)
        # Pattern: number + "hour(s)" or "minute(s)" + optional bullet, appearing after date
        # But "10 minutes" in a title like "10 minutes, un livre" should be kept
        is_duration_metadata = False
        if re.search(r'\d+\s+(hour|minute)[s]?\s*•', line, re.IGNORECASE):
            is_duration_metadata = True
        
        if is_date_time_line or is_duration_metadata:
            continue
        
        # Check if this is excluded metadata
        is_excluded = False
        
        # Check keywords (but "skill" might appear in titles, so be careful)
        if any(kw in line.lower() for kw in excluded_keywords):
            is_excluded = True
        
        # Don't exclude lines that look like title content
        # If not excluded and looks like title content
        if not is_excluded and len(line) >= 3:
            # Must have some letters
            if any(c.isalpha() for c in line):
                # Check if it's not clearly a time pattern
                if not re.search(r'\d{1,2}:\d{2}[AP]M', line) and 'utc' not in line.lower():
                    title_lines.append(line)
    
    # Join title lines
    if title_lines:
        full_title = ' '.join(title_lines)
        # Clean up extra spaces
        full_title = re.sub(r'\s+', ' ', full_title).strip()
        # Reasonable length check
        if 5 <= len(full_title) <= 300:
            return full_title
    
    return None

def extract_duration_from_text(text):
    """Extract course duration from PDF text."""
    if not text:
        return None
    
    # Patterns: "1 hour 27 minutes", "30 minutes", "1h 27m", etc.
    patterns = [
        (r'(\d+)\s+hour[s]?\s+(\d+)\s+minute[s]?', lambda m: f"{m.group(1)}h {m.group(2)}m"),
        (r'(\d+)\s+hour[s]?', lambda m: f"{m.group(1)}h"),
        (r'(\d+)\s+minute[s]?', lambda m: f"{m.group(1)}m"),
        (r'(\d+)h\s*(\d+)m', lambda m: f"{m.group(1)}h {m.group(2)}m"),
        (r'(\d+)h', lambda m: f"{m.group(1)}h"),
        (r'(\d+)m', lambda m: f"{m.group(1)}m"),
    ]
    
    for pattern, formatter in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return formatter(match)
    
    return None

def format_skill_name(skill):
    """Format a skill name to proper title case."""
    if not skill:
        return None
    
    # Clean up
    skill = skill.strip('•,.:;()[]').strip()
    
    # Handle special cases
    # Preserve acronyms like "AI", "API", "SQL", etc.
    skill_upper = skill.upper()
    common_acronyms = ['AI', 'API', 'SQL', 'XML', 'JSON', 'HTML', 'CSS', 'JS', 'REST', 'SOAP', 'HTTP', 'HTTPS', 'URL', 'UI', 'UX', 'CI', 'CD', 'QA', 'ID']
    
    # Check if entire skill is an acronym
    if skill_upper in common_acronyms:
        return skill_upper
    
    # Split into words and format
    words = skill.split()
    formatted_words = []
    
    # Words that should be lowercase in the middle of phrases (unless first word)
    lowercase_words = {'for', 'and', 'or', 'the', 'of', 'in', 'on', 'at', 'to', 'a', 'an', 'as', 'by', 'with'}
    
    for i, word in enumerate(words):
        word_clean = word.strip('•,.:;()[]').strip()
        if not word_clean:
            continue
        
        word_lower = word_clean.lower()
        
        # If it's an acronym (all caps, 2-5 chars), keep it uppercase
        if word_clean.isupper() and 2 <= len(word_clean) <= 5:
            formatted_words.append(word_clean)
        # If it's mixed case (like "JavaScript"), preserve it
        elif word_clean[0].isupper() and any(c.islower() for c in word_clean[1:]):
            formatted_words.append(word_clean)
        # If it's a lowercase word in the middle of phrase (not first word)
        elif i > 0 and word_lower in lowercase_words:
            formatted_words.append(word_lower)
        # Otherwise, capitalize first letter
        else:
            formatted_words.append(word_clean.capitalize())
    
    return ' '.join(formatted_words)

def extract_skills_from_text(text):
    """Extract skills from PDF text.
    
    LinkedIn Learning PDFs format skills like:
    "Top skills covered"
    "Microsoft Copilot"
    "Security Operations"
    "Generative AI"
    
    Each skill is on its own line. We should treat each line as a complete skill phrase.
    Skills section ends when we hit metadata like "Certificate ID" or signature lines.
    """
    if not text:
        return []
    
    skills = []
    
    # Find "Top skills covered" section
    # Look for the header and capture lines until we hit stop patterns
    skill_section_pattern = r'Top\s+skills\s+covered[:\s]*\n((?:[^\n]+\n?)+?)(?=\n\s*\n|\nCertificate\s+ID|\n[A-Z][a-z]+\s+[A-Z][a-z]+\s+Head|\n[A-Z][A-Z\s]{15,}|$)'
    skill_match = re.search(skill_section_pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    
    if not skill_match:
        # Try alternative pattern - skills might be on same line
        alt_pattern = r'Top\s+skills\s+covered[:\s]+([^\n]+)'
        alt_match = re.search(alt_pattern, text, re.IGNORECASE)
        if alt_match:
            skill_text = alt_match.group(1).strip()
            # Split by common separators if on same line
            for skill in re.split(r'[•,\-;]', skill_text):
                skill_clean = skill.strip()
                if skill_clean and len(skill_clean) >= 2:
                    formatted = format_skill_name(skill_clean)
                    if formatted:
                        skills.append(formatted)
        return skills[:5]
    
    skill_text = skill_match.group(1).strip()
    
    # Split by newlines - each line is potentially a skill
    lines = skill_text.split('\n')
    
    # Patterns that indicate we should stop processing (metadata lines)
    stop_patterns = [
        r'Certificate\s+ID',
        r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s+Head',  # Signature lines like "Shea Hanson Head"
        r'^[A-Z][a-z]+\s+Of\s+',  # Title fragments like "Head Of Learning"
        r'^[A-Z][a-z]+\s+Strategy$',  # "Content Strategy"
        r'^\d+[a-z]+\s+\d+[a-z]+$',  # Duration like "48m" or "1h 55m"
        r'^\d{1,2}[-/]\d{1,2}[-/]\d{4}',  # Dates
        r'^[A-Z][a-z]+\s+\d+,\s+\d{4}',  # Dates like "Jan 18, 2026"
    ]
    
    # Words/phrases to skip (metadata, not actual skills)
    skip_phrases = {
        'certificate id', 'head of', 'learning content', 'content strategy',
        'shea hanson', 'provider', 'linkedin learning', 'course completed',
        'completed by', 'top skills covered', 'institute inc', 'institute',
        'activity #', 'activity', 'inc', 'ltd', 'llc', 'corp', 'corporation',
        'pdus', 'pdu', 'contact hours', 'contacthours'
    }
    
    # Patterns that indicate metadata (not skills)
    metadata_patterns = [
        r'^[A-Z][a-z]+\s+Inc\.?$',  # "Institute Inc"
        r'^[A-Z][a-z]+\s+Inc$',  # "Institute Inc"
        r'Activity\s*#',  # "Activity #"
        r'^#\s*\d+',  # "# 12345"
        r'^\d+[a-z0-9]+$',  # Alphanumeric IDs like "4101x2z28f"
        r'^[a-z]+\d+[a-z0-9]+$',  # Mixed alphanumeric IDs
        r'^\d+[a-z]+\d+',  # Number-letter-number patterns
        r'PDUs?/ContactHours?',  # "PDUs/ContactHours 1.00"
        r'Contact\s+Hours?',  # "Contact Hours"
        r'PDUs?',  # "PDU" or "PDUs"
    ]
    
    for line in lines:
        # Clean the line
        line_clean = line.strip()
        
        # Remove bullet points and common punctuation from start
        line_clean = re.sub(r'^[•\-\*\.\s]+', '', line_clean)
        line_clean = line_clean.strip('•,.:;()[]').strip()
        
        # Skip empty lines or very short lines
        if not line_clean or len(line_clean) < 2:
            continue
        
        line_lower = line_clean.lower()
        
        # Check stop patterns - if we hit metadata, stop processing
        should_stop = False
        for pattern in stop_patterns:
            if re.search(pattern, line_clean, re.IGNORECASE):
                should_stop = True
                break
        
        if should_stop:
            break
        
        # Skip if line contains skip phrases
        skip_line = False
        for phrase in skip_phrases:
            if phrase in line_lower:
                skip_line = True
                break
        
        if skip_line:
            continue
        
        # Check for metadata patterns
        is_metadata = False
        for pattern in metadata_patterns:
            if re.search(pattern, line_clean, re.IGNORECASE):
                is_metadata = True
                break
        
        if is_metadata:
            continue
        
        # Skip if line looks like a date or duration
        if re.match(r'^\d+[hm]\s*$|^\d+h\s+\d+m\s*$', line_lower):
            continue
        
        # Skip if line is just numbers or special characters
        if not any(c.isalpha() for c in line_clean):
            continue
        
        # Skip if line looks like an ID (mostly alphanumeric with numbers)
        # Pattern: has numbers and letters but looks like an ID (not a skill name)
        if re.match(r'^[a-z0-9]{8,}$', line_lower) and any(c.isdigit() for c in line_clean):
            # Check if it's mostly numbers/letters without spaces (likely an ID)
            if len(line_clean.split()) == 1 and len(line_clean) >= 8:
                # Allow if it's a known acronym or short skill name
                if line_clean.lower() not in ['javascript', 'typescript', 'postgresql', 'mongodb']:
                    continue
        
        # Check if line contains multiple skills (common pattern: skills concatenated)
        # Skills are typically 1-4 words, so if we have more than 3 words, we might have multiple skills
        words = line_clean.split()
        
        # Known skill patterns to help split concatenated skills
        # These are common multi-word skills that should be kept together
        # Order matters: longer patterns first to match correctly
        known_skill_patterns = [
            r'Artificial\s+Intelligence\s+for\s+Business',
            r'AI\s+for\s+Business\s+Analysis',
            r'AI\s+for\s+Business',
            r'Artificial\s+Intelligence\s+for\s+Business\s+Analysis',
            r'Media\s+Literacy',
            r'Media\s+Psychology',
            r'Software\s+Testing',
            r'Programming\s+Foundations',
            r'Software\s+Quality\s+Assurance',
            r'Quality\s+Assurance',
            r'Microsoft\s+Copilot',
            r'Security\s+Operations',
            r'Security\s+Incident\s+Response',
            r'Generative\s+AI',
            r'Artificial\s+Intelligence',
            r'Visual\s+Studio\s+Code',
            r'Visual\s+Studio',
            r'Personal\s+Development',
            r'Critical\s+Thinking',
            r'Digital\s+Transformation',
            r'Cloud\s+Computing',
            r'Interpersonal\s+Communication',
            r'SQL\s+Database',
            r'Design\s+AI',
            r'Data\s+Analysis',
            r'Business\s+Analysis',
        ]
        
        # Strategy: Treat each line as potentially containing multiple skills
        # First, try to match known patterns (longest first)
        # Then process remaining text more carefully
        
        found_patterns = []
        remaining_text = line_clean
        pattern_positions = []
        
        # Find all known patterns and their positions
        for pattern in known_skill_patterns:
            matches = list(re.finditer(pattern, remaining_text, re.IGNORECASE))
            for match in matches:
                pattern_positions.append((match.start(), match.end(), match.group(0)))
        
        # Sort by position and remove overlaps (keep longest matches)
        pattern_positions.sort(key=lambda x: (x[0], -(x[1] - x[0])))
        non_overlapping = []
        for start, end, text in pattern_positions:
            # Check if this overlaps with any already added pattern
            overlaps = False
            for prev_start, prev_end, _ in non_overlapping:
                if not (end <= prev_start or start >= prev_end):
                    overlaps = True
                    break
            if not overlaps:
                non_overlapping.append((start, end, text))
        
        # Extract matched patterns
        for start, end, pattern_text in non_overlapping:
            found_patterns.append(pattern_text)
            # Mark as processed by replacing with spaces
            remaining_text = remaining_text[:start] + ' ' * (end - start) + remaining_text[end:]
        
        # Add found patterns as skills
        for pattern_text in found_patterns:
            skill_name = format_skill_name(pattern_text.strip())
            if skill_name:
                skills.append(skill_name)
        
        # If we found patterns and remaining text is empty/whitespace, we're done with this line
        # This prevents adding concatenated versions like "Media Literacy Media Psychology"
        remaining_words = [w for w in remaining_text.split() if w.strip() and len(w.strip()) > 1]
        
        # If we matched all patterns and there's no meaningful remaining text, skip further processing
        if found_patterns and not remaining_words:
            continue
        
        if remaining_words:
            # If we have remaining words, try to group them intelligently
            # Common patterns: "X for Y", "X Y", single words
            i = 0
            while i < len(remaining_words):
                # Try "X for Y" pattern (3 words)
                if i + 2 < len(remaining_words) and remaining_words[i+1].lower() == 'for':
                    potential_skill = ' '.join(remaining_words[i:i+3])
                    skill_name = format_skill_name(potential_skill)
                    if skill_name:
                        skills.append(skill_name)
                        i += 3
                        continue
                
                # Try 2-word combinations
                if i + 1 < len(remaining_words):
                    potential_skill = ' '.join(remaining_words[i:i+2])
                    # Skip if it's "for X" (incomplete phrase)
                    if remaining_words[i].lower() != 'for':
                        skill_name = format_skill_name(potential_skill)
                        if skill_name:
                            skills.append(skill_name)
                            i += 2
                            continue
                
                # Single word (skip common words)
                word = remaining_words[i].lower()
                if word not in ['for', 'and', 'or', 'the', 'of', 'in', 'on', 'at', 'to']:
                    skill_name = format_skill_name(remaining_words[i])
                    if skill_name:
                        skills.append(skill_name)
                i += 1
        # If line has many words but no patterns matched, treat as single skill
        elif len(words) > 4:
            # Try to find known patterns first
            found_patterns = []
            remaining_text = line_clean
            
            for pattern in known_skill_patterns:
                matches = re.finditer(pattern, remaining_text, re.IGNORECASE)
                for match in matches:
                    found_patterns.append(match.group(0))
                    # Remove matched pattern from remaining text
                    remaining_text = remaining_text.replace(match.group(0), ' ', 1)
            
            # Add found patterns as skills
            for pattern_text in found_patterns:
                skill_name = format_skill_name(pattern_text.strip())
                if skill_name:
                    skills.append(skill_name)
            
            # Process remaining text (might contain more skills)
            remaining_words = remaining_text.split()
            if remaining_words:
                # Group remaining words into potential skills (2-3 words each)
                i = 0
                while i < len(remaining_words):
                    # Try 2-word combinations first (common skill length)
                    if i + 1 < len(remaining_words):
                        potential_skill = ' '.join(remaining_words[i:i+2])
                        skill_name = format_skill_name(potential_skill)
                        if skill_name and len(skill_name.split()) <= 3:
                            skills.append(skill_name)
                            i += 2
                            continue
                    # Single word skill
                    skill_name = format_skill_name(remaining_words[i])
                    if skill_name:
                        skills.append(skill_name)
                    i += 1
        else:
            # Single skill line - format and add
            skill_name = format_skill_name(line_clean)
            
            # Only add if it's a valid skill (has letters, reasonable length)
            if skill_name and 2 <= len(skill_name) <= 80 and any(c.isalpha() for c in skill_name):
                # Additional validation: skill shouldn't be just common words
                skill_words = skill_name.lower().split()
                if len(skill_words) == 1 and skill_words[0] in ['the', 'of', 'and', 'or', 'for', 'with', 'from']:
                    continue
                skills.append(skill_name)
    
    # Remove duplicates and concatenated duplicates (case-insensitive) while preserving order
    seen = set()
    unique_skills = []
    
    for skill in skills:
        skill_lower = skill.lower().strip()
        if not skill_lower or len(skill_lower) < 2:
            continue
        
        # Check if this skill is an exact duplicate
        if skill_lower in seen:
            continue
        
        # Check if this skill contains other skills (concatenated duplicates)
        # e.g., "Media Literacy Media Psychology" contains both "Media Literacy" and "Media Psychology"
        is_concatenated = False
        for existing_skill in seen:
            if existing_skill in skill_lower and existing_skill != skill_lower:
                # This skill contains an existing skill, so it's likely concatenated
                is_concatenated = True
                break
        
        # Also check if this skill is contained in other skills we've already added
        # If so, skip it (the longer concatenated version will be handled above)
        if not is_concatenated:
            for existing_skill in seen:
                if skill_lower in existing_skill and skill_lower != existing_skill:
                    # This skill is part of a longer skill we already added, skip it
                    is_concatenated = True
                    break
        
        if not is_concatenated:
            seen.add(skill_lower)
            unique_skills.append(skill.strip())
    
    return unique_skills[:5]  # Limit to 5 skills

def main():
    archived_path = Path('archived')
    certificates = []
    
    if not archived_path.exists():
        print(f"Error: {archived_path} directory not found!")
        return
    
    # Find all PDFs in year folders
    pdf_files = []
    for year_folder in sorted(archived_path.glob('20*')):
        if year_folder.is_dir():
            pdf_files.extend(year_folder.glob('*.pdf'))
    
    # Also check root archived folder for any remaining PDFs
    pdf_files.extend(archived_path.glob('**/*.pdf'))
    
    # Remove duplicates
    pdf_files = list(set(pdf_files))
    
    print(f"Found {len(pdf_files)} certificate PDFs")
    print("Extracting data from PDFs...\n")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        if i % 50 == 0:
            print(f"Processing {i}/{len(pdf_files)}...")
        
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        
        # Extract data
        year, full_date = extract_date_from_text(text)
        title = extract_title_from_text(text)
        duration = extract_duration_from_text(text)
        skills = extract_skills_from_text(text)
        
        # If year not found, try to get from folder
        if not year:
            parent = pdf_file.parent.name
            year_match = re.search(r'(\d{4})', parent)
            if year_match:
                year = year_match.group(1)
            else:
                year = '2024'  # Default
        
        # If title not found, use filename (clean it up)
        if not title:
            title = pdf_file.stem.replace('CertificateOfCompletion_', '').replace('_', ' ').replace('-', ' ')
            # Clean up common suffixes
            title = re.sub(r'\s*-\s*\d+$', '', title)
            title = re.sub(r'\s*\d{4}$', '', title)
        
        # Determine domain from title and skills
        domain = categorize_domain(title, skills)
        
        certificate = {
            'id': len(certificates) + 1,
            'title': title,
            'path': str(pdf_file.relative_to(Path('.'))),
            'domain': domain,
            'year': year,
            'date': full_date,
            'duration': duration,
            'skills': skills,
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

def categorize_domain(title, skills):
    """Categorize certificate into domain."""
    DOMAIN_KEYWORDS = {
        'programming': ['java', 'python', 'javascript', 'programming', 'spring', 'maven', 'object-oriented', 'refactoring', 'code', 'git'],
        'cloud': ['aws', 'azure', 'google cloud', 'cloud', 'gcp', 'ccv2', 'btp'],
        'frontend': ['css', 'html', 'frontend', 'web developers', 'visual studio code', 'web'],
        'devops': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'devops', 'infrastructure', 'version control', 'ubuntu', 'linux'],
        'ai': ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'gpt', 'openai', 'claude', 'gemini', 'copilot', 'mcp', 'agentic', 'deepfake', 'dalle'],
        'agile': ['agile', 'scrum', 'project management', 'kanban'],
        'ecommerce': ['e-commerce', 'ecommerce', 'seo', 'commerce', 'sap commerce'],
        'communication': ['communication', 'meeting', 'presentation', 'business', 'marketing'],
        'tools': ['visual studio code', 'postman', 'confluence', 'microsoft 365', 'excel', 'windows', 'macos'],
        'security': ['security', 'owasp', 'api security'],
        'data': ['data', 'analytics', 'excel', 'chatgpt data', 'dynamodb'],
        'api': ['api', 'rest', 'swagger', 'openapi', 'postman', 'api testing', 'api documentation']
    }
    
    text = (title + ' ' + ' '.join(skills)).lower()
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return domain
    
    return 'other'

if __name__ == '__main__':
    if not PDF_LIB:
        print("ERROR: Please install a PDF library first:")
        print("  pip install pypdf")
        print("  OR")
        print("  pip install pdfplumber")
        exit(1)
    
    print(f"Using PDF library: {PDF_LIB}")
    main()
