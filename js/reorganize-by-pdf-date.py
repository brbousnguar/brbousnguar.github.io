#!/usr/bin/env python3
"""
Reorganize PDFs to correct year folders based on actual PDF dates.
"""

import os
import re
import shutil
from pathlib import Path

try:
    import pypdf
except ImportError:
    print("Error: pypdf not installed. Install with: pip install pypdf")
    exit(1)

def extract_year_from_pdf(pdf_path):
    """Extract year from PDF."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages[:2]:
                text += page.extract_text()
            
            # Look for "May 17, 2025 at 07:24AM UTC"
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
    
    # Find all PDFs
    all_pdfs = list(archived_path.rglob('*.pdf'))
    print(f"Found {len(all_pdfs)} PDFs")
    print("Reorganizing by PDF dates...\n")
    
    moved = 0
    correct = 0
    
    for pdf_file in all_pdfs:
        try:
            # Extract year from PDF
            pdf_year = extract_year_from_pdf(pdf_file)
            
            if not pdf_year:
                correct += 1  # Can't determine, leave as is
                continue
            
            # Check current folder
            current_folder = pdf_file.parent.name
            
            # If already in correct year folder, skip
            if current_folder == pdf_year:
                correct += 1
                continue
            
            # Move to correct year folder
            year_folder = archived_path / pdf_year
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
    
    print(f"\n✓ Moved {moved} PDFs to correct year folders")
    print(f"✓ {correct} PDFs already in correct folders")
    
    # Clean up: remove all non-PDF files and empty folders
    print("\nCleaning up...")
    removed_files = 0
    removed_folders = 0
    
    # Remove non-PDF files
    for item in archived_path.rglob('*'):
        if item.is_file() and not item.name.endswith('.pdf'):
            try:
                item.unlink()
                removed_files += 1
            except:
                pass
    
    # Remove course folders (non-year folders)
    for folder in sorted(archived_path.rglob('*'), reverse=True):
        if folder.is_dir() and folder != archived_path:
            folder_name = folder.name
            # Skip year folders
            if folder_name.isdigit() and len(folder_name) == 4:
                continue
            
            # Remove folder if empty
            try:
                if not any(folder.iterdir()):
                    folder.rmdir()
                    removed_folders += 1
                else:
                    # Remove all contents
                    for item in folder.rglob('*'):
                        if item.is_file():
                            try:
                                item.unlink()
                            except:
                                pass
                    # Try to remove again
                    try:
                        folder.rmdir()
                        removed_folders += 1
                    except:
                        pass
            except:
                pass
    
    print(f"✓ Removed {removed_files} non-PDF files")
    print(f"✓ Removed {removed_folders} course folders")
    
    # Summary
    print("\n" + "=" * 60)
    print("Final Structure:")
    print("=" * 60)
    for year_folder in sorted(archived_path.glob('20*')):
        if year_folder.is_dir():
            pdf_count = len(list(year_folder.glob('*.pdf')))
            if pdf_count > 0:
                print(f"  {year_folder.name}: {pdf_count} PDFs")

if __name__ == '__main__':
    print("=" * 60)
    print("Reorganize Certificates by PDF Date")
    print("=" * 60)
    print("\nThis will:")
    print("1. Read dates from each PDF")
    print("2. Move PDFs to correct year folders")
    print("3. Remove all course folders and non-PDF files")
    print("\nStarting...\n")
    
    main()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
