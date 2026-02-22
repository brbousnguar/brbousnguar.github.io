#!/usr/bin/env python3
"""
Script to organize LinkedIn Learning certificates by year based on PDF metadata.
Extracts date, title, skills, and duration from PDFs and organizes them into year folders.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# Try multiple PDF libraries
HAS_PYPDF2 = False
HAS_PDFPLUMBER = False
HAS_PYPDF = False

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    try:
        import pypdf
        HAS_PYPDF = True
    except ImportError:
        try:
            import pdfplumber
            HAS_PDFPLUMBER = True
        except ImportError:
            print("Warning: No PDF library found. Install one with:")
            print("  pip install PyPDF2")
            print("  pip install pdfplumber")
            print("  pip install pypdf")

def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF using available library."""
    text = None
    
    # Try PyPDF2
    if HAS_PYPDF2:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            pass
    
    # Try pypdf
    if not text and HAS_PYPDF:
        try:
            import pypdf
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            pass
    
    # Try pdfplumber
    if not text and HAS_PDFPLUMBER:
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            pass
    
    return None

def extract_date_from_pdf_text(text):
    """Extract completion date from PDF text."""
    if not text:
        return None
    
    # Look for patterns like "May 17, 2025 at 07:24AM UTC" or "Jan 19, 2026"
    patterns = [
        r'(\w+)\s+(\d+),\s+(\d{4})\s+at\s+\d+:\d+[AP]M',
        r'(\w+)\s+(\d+),\s+(\d{4})',
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                if len(match.groups()) == 3:
                    # Try to parse the date
                    date_str = match.group(0)
                    # Try common formats
                    for fmt in ['%B %d, %Y', '%b %d, %Y', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d']:
                        try:
                            dt = datetime.strptime(date_str.split(' at')[0], fmt)
                            return dt.year
                        except:
                            continue
            except:
                continue
    
    return None

def extract_title_from_pdf_text(text):
    """Extract course title from PDF text."""
    if not text:
        return None
    
    # Look for patterns like "Course completed by" followed by title
    # Or look for large text that appears to be the title
    patterns = [
        r'Course completed by.*?\n(.*?)\n',
        r'completed by.*?\n(.*?)\n',
        r'(?:Course|Certificate).*?\n([A-Z][^\n]{10,100})\n',
    ]
    
    lines = text.split('\n')
    # Look for the longest line that seems like a title (not too short, not too long)
    for line in lines:
        line = line.strip()
        if 20 <= len(line) <= 150 and not line.startswith('Certificate') and not line.startswith('LinkedIn'):
            # Check if it looks like a title (has capital letters, not all caps)
            if any(c.isupper() for c in line) and not line.isupper():
                return line
    
    return None

def extract_duration_from_pdf_text(text):
    """Extract course duration from PDF text."""
    if not text:
        return None
    
    # Look for patterns like "1 hour 27 minutes" or "30 minutes" or "1h 27m"
    patterns = [
        r'(\d+)\s+hour[s]?\s+(\d+)\s+minute[s]?',
        r'(\d+)\s+hour[s]?',
        r'(\d+)\s+minute[s]?',
        r'(\d+)h\s*(\d+)m',
        r'(\d+)h',
        r'(\d+)m',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                hours = int(groups[0])
                minutes = int(groups[1])
                return f"{hours}h {minutes}m"
            elif 'hour' in pattern.lower():
                return f"{groups[0]}h"
            elif 'minute' in pattern.lower() or 'm' in pattern:
                return f"{groups[0]}m"
    
    return None

def extract_skills_from_pdf_text(text):
    """Extract skills from PDF text."""
    if not text:
        return []
    
    skills = []
    
    # Look for "Top skills covered" section
    skill_section_match = re.search(r'Top skills covered[:\s]*(.*?)(?:\n\n|\nCertificate|$)', text, re.IGNORECASE | re.DOTALL)
    if skill_section_match:
        skill_text = skill_section_match.group(1)
        # Extract skill names (usually on separate lines or in tags)
        skill_lines = [line.strip() for line in skill_text.split('\n') if line.strip()]
        for line in skill_lines:
            # Remove common prefixes/suffixes
            line = re.sub(r'^(skill|skills?)[:\s]*', '', line, flags=re.IGNORECASE)
            if len(line) > 2 and len(line) < 50:
                skills.append(line)
    
    return skills[:5]  # Limit to 5 skills

def organize_certificates():
    """Main function to organize certificates by year."""
    archived_path = Path('archived')
    
    if not archived_path.exists():
        print(f"Error: {archived_path} directory not found!")
        return
    
    # Create year folders
    year_folders = {}
    cert_files = list(archived_path.rglob('CertificateOfCompletion*.pdf'))
    
    print(f"Found {len(cert_files)} certificate PDFs")
    print("Extracting data and organizing by year...\n")
    
    organized_count = 0
    failed_count = 0
    
    for cert_file in cert_files:
        try:
            # Extract text from PDF
            text = extract_text_from_pdf(cert_file)
            
            # Extract year
            year = extract_date_from_pdf_text(text)
            
            # If year extraction failed, try to get from folder name or default to 2024
            if not year:
                # Check parent folder for year
                parent = cert_file.parent.name
                year_match = re.search(r'(\d{4})', parent)
                if year_match:
                    year = int(year_match.group(1))
                    if 2020 <= year <= 2030:
                        year = str(year)
                    else:
                        year = '2024'
                else:
                    year = '2024'
            else:
                year = str(year)
            
            # Create year folder if it doesn't exist
            year_folder = archived_path / year
            year_folder.mkdir(exist_ok=True)
            
            # Move PDF to year folder
            new_path = year_folder / cert_file.name
            
            # Handle duplicates
            if new_path.exists():
                # Add a number suffix
                base_name = cert_file.stem
                counter = 1
                while new_path.exists():
                    new_path = year_folder / f"{base_name}_{counter}.pdf"
                    counter += 1
            
            shutil.move(str(cert_file), str(new_path))
            organized_count += 1
            
            if organized_count % 50 == 0:
                print(f"Processed {organized_count} certificates...")
                
        except Exception as e:
            print(f"Error processing {cert_file}: {e}")
            failed_count += 1
    
    print(f"\n✓ Organized {organized_count} certificates into year folders")
    if failed_count > 0:
        print(f"⚠ {failed_count} certificates failed to process")
    
    # Clean up empty folders and non-PDF files
    print("\nCleaning up...")
    cleanup_archived_folder(archived_path)

def cleanup_archived_folder(archived_path):
    """Remove non-PDF files and empty folders, keeping only PDFs in year folders."""
    removed_count = 0
    
    # Remove all non-PDF files
    for item in archived_path.rglob('*'):
        if item.is_file() and not item.name.endswith('.pdf'):
            try:
                item.unlink()
                removed_count += 1
            except Exception as e:
                print(f"Could not remove {item}: {e}")
    
    # Remove empty folders (except year folders)
    for folder in sorted(archived_path.rglob('*'), reverse=True):
        if folder.is_dir() and folder != archived_path:
            # Check if it's a year folder (contains only PDFs)
            pdfs = list(folder.glob('*.pdf'))
            other_files = [f for f in folder.iterdir() if f.is_file() and not f.name.endswith('.pdf')]
            subdirs = [d for d in folder.iterdir() if d.is_dir()]
            
            # If it's not a year folder (has subdirs or non-PDF files), clean it
            if subdirs or other_files:
                # Move PDFs to parent year folder if possible
                parent_year = None
                parent_match = re.search(r'(\d{4})', folder.parent.name)
                if parent_match:
                    parent_year = parent_match.group(1)
                
                if parent_year:
                    year_folder = archived_path / parent_year
                    year_folder.mkdir(exist_ok=True)
                    for pdf in pdfs:
                        try:
                            shutil.move(str(pdf), str(year_folder / pdf.name))
                        except:
                            pass
                
                # Remove the folder
                try:
                    if not any(folder.iterdir()):
                        folder.rmdir()
                        removed_count += 1
                except:
                    pass
    
    print(f"✓ Cleaned up {removed_count} non-PDF files and empty folders")

if __name__ == '__main__':
    print("=" * 60)
    print("LinkedIn Learning Certificate Organizer")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Extract dates from PDF certificates")
    print("2. Organize PDFs into year folders (2024, 2025, 2026, etc.)")
    print("3. Remove non-PDF files and empty folders")
    print("\nStarting organization...\n")
    
    organize_certificates()
    
    print("\n" + "=" * 60)
    print("Organization complete!")
    print("=" * 60)
