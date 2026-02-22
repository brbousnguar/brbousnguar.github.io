#!/usr/bin/env python3
"""
Final organization: Extract dates from PDFs, move to year folders, remove course folders.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

try:
    import pypdf
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("Error: pypdf not installed. Install with: pip install pypdf")
    exit(1)

def extract_year_from_pdf(pdf_path):
    """Extract year from PDF text."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages[:2]:
                text += page.extract_text()
            
            # Look for "May 17, 2025 at 07:24AM UTC" pattern
            pattern = r'(\w+)\s+(\d+),\s+(\d{4})\s+at'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                year = int(match.group(3))
                if 2020 <= year <= 2030:
                    return str(year)
    except Exception as e:
        pass
    
    return None

def main():
    archived_path = Path('archived')
    
    # Create year folders
    for year in range(2020, 2031):
        (archived_path / str(year)).mkdir(exist_ok=True)
    
    # Find all PDFs (including those in course folders)
    all_pdfs = list(archived_path.rglob('CertificateOfCompletion*.pdf'))
    print(f"Found {len(all_pdfs)} certificate PDFs")
    print("Extracting dates and organizing...\n")
    
    moved = 0
    already_organized = 0
    
    for pdf_file in all_pdfs:
        # Skip if already in a year folder
        if pdf_file.parent.name.isdigit() and len(pdf_file.parent.name) == 4:
            already_organized += 1
            continue
        
        try:
            # Extract year from PDF
            year = extract_year_from_pdf(pdf_file)
            
            # Fallback: check folder name
            if not year:
                parent = pdf_file.parent.name
                year_match = re.search(r'(\d{4})', parent)
                if year_match:
                    year = year_match.group(1)
                else:
                    year = '2024'  # Default
            
            # Move to year folder
            year_folder = archived_path / year
            new_path = year_folder / pdf_file.name
            
            # Handle duplicates
            if new_path.exists():
                base_name = pdf_file.stem
                counter = 1
                while new_path.exists():
                    new_path = year_folder / f"{base_name}_{counter}.pdf"
                    counter += 1
            
            shutil.move(str(pdf_file), str(new_path))
            moved += 1
            
            if moved % 50 == 0:
                print(f"Moved {moved} PDFs...")
                
        except Exception as e:
            print(f"Error: {pdf_file}: {e}")
    
    print(f"\n✓ Moved {moved} PDFs to year folders")
    print(f"✓ {already_organized} PDFs already in year folders")
    
    # Clean up: remove all non-PDF files
    print("\nRemoving non-PDF files...")
    removed_files = 0
    for item in archived_path.rglob('*'):
        if item.is_file() and not item.name.endswith('.pdf'):
            try:
                item.unlink()
                removed_files += 1
            except:
                pass
    
    print(f"✓ Removed {removed_files} non-PDF files")
    
    # Remove course folders (non-year folders)
    print("\nRemoving course folders...")
    removed_folders = 0
    for folder in sorted(archived_path.rglob('*'), reverse=True):
        if folder.is_dir() and folder != archived_path:
            folder_name = folder.name
            
            # Skip year folders
            if folder_name.isdigit() and len(folder_name) == 4:
                continue
            
            # Remove the folder if empty or only has non-PDF files
            try:
                if not any(folder.glob('*.pdf')):
                    # Move any remaining PDFs first
                    pdfs = list(folder.glob('**/*.pdf'))
                    for pdf in pdfs:
                        # Try to determine year
                        year = extract_year_from_pdf(pdf) or '2024'
                        year_folder = archived_path / year
                        year_folder.mkdir(exist_ok=True)
                        try:
                            shutil.move(str(pdf), str(year_folder / pdf.name))
                        except:
                            pass
                    
                    # Remove folder
                    if not any(folder.iterdir()):
                        folder.rmdir()
                        removed_folders += 1
                    else:
                        # Force remove if it has non-PDF files
                        for item in folder.rglob('*'):
                            if item.is_file():
                                try:
                                    item.unlink()
                                except:
                                    pass
                        try:
                            folder.rmdir()
                            removed_folders += 1
                        except:
                            pass
            except Exception as e:
                pass
    
    print(f"✓ Removed {removed_folders} course folders")
    
    # Summary
    print("\n" + "=" * 60)
    print("Final Summary:")
    print("=" * 60)
    for year_folder in sorted(archived_path.glob('20*')):
        if year_folder.is_dir():
            pdf_count = len(list(year_folder.glob('*.pdf')))
            if pdf_count > 0:
                print(f"  {year_folder.name}: {pdf_count} PDFs")

if __name__ == '__main__':
    print("=" * 60)
    print("Final Certificate Organization")
    print("=" * 60)
    print("\nThis will:")
    print("1. Extract dates from PDFs")
    print("2. Move all PDFs to year folders")
    print("3. Remove all course folders and non-PDF files")
    print("\nStarting...\n")
    
    main()
    
    print("\n" + "=" * 60)
    print("Organization complete!")
    print("=" * 60)
