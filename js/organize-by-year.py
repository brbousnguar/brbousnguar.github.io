#!/usr/bin/env python3
"""
Organize LinkedIn Learning certificates by year based on PDF dates.
Moves all PDFs to year folders and removes course folders.
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
    print("Warning: pypdf not installed. Install with: pip install pypdf")

def extract_year_from_pdf(pdf_path):
    """Extract year from PDF text."""
    if not HAS_PDF:
        return None
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages[:2]:  # Check first 2 pages
                text += page.extract_text()
            
            # Look for date patterns like "May 17, 2025 at 07:24AM UTC"
            patterns = [
                (r'(\w+)\s+(\d+),\s+(\d{4})\s+at', 3),  # "May 17, 2025 at"
                (r'(\w+)\s+(\d+),\s+(\d{4})', 3),  # "May 17, 2025"
                (r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', 1),  # "2025-05-17"
            ]
            
            for pattern, year_group in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        year = int(match.group(year_group))
                        if 2020 <= year <= 2030:
                            return str(year)
                    except:
                        continue
    except Exception as e:
        pass
    
    return None

def organize_pdfs():
    """Organize all PDFs into year folders."""
    archived_path = Path('archived')
    
    if not archived_path.exists():
        print(f"Error: {archived_path} directory not found!")
        return
    
    # Create year folders
    for year in range(2020, 2031):
        (archived_path / str(year)).mkdir(exist_ok=True)
    
    # Find all PDFs
    all_pdfs = list(archived_path.rglob('CertificateOfCompletion*.pdf'))
    print(f"Found {len(all_pdfs)} certificate PDFs")
    print("Organizing by year from PDF dates...\n")
    
    organized = 0
    failed = 0
    
    for pdf_file in all_pdfs:
        try:
            # Skip if already in a year folder
            if pdf_file.parent.name.isdigit() and len(pdf_file.parent.name) == 4:
                continue
            
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
            organized += 1
            
            if organized % 50 == 0:
                print(f"Processed {organized} PDFs...")
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
            failed += 1
    
    print(f"\n✓ Organized {organized} PDFs into year folders")
    if failed > 0:
        print(f"⚠ {failed} PDFs failed")
    
    # Clean up: remove all non-PDF files and empty folders
    print("\nCleaning up non-PDF files and folders...")
    cleanup_folders(archived_path)

def cleanup_folders(archived_path):
    """Remove all non-PDF files and course folders, keeping only PDFs in year folders."""
    removed_files = 0
    removed_folders = 0
    
    # First pass: remove all non-PDF files
    for item in archived_path.rglob('*'):
        if item.is_file() and not item.name.endswith('.pdf'):
            try:
                item.unlink()
                removed_files += 1
            except Exception as e:
                pass
    
    # Second pass: remove course folders (non-year folders)
    # Process in reverse order (deepest first)
    for folder in sorted(archived_path.rglob('*'), reverse=True):
        if folder.is_dir() and folder != archived_path:
            folder_name = folder.name
            
            # Skip year folders (4-digit numbers)
            if folder_name.isdigit() and len(folder_name) == 4:
                continue
            
            # Check if folder has any PDFs
            pdfs = list(folder.glob('*.pdf'))
            
            if pdfs:
                # Move PDFs to appropriate year folder (or 2024 as default)
                # Try to determine year from folder name or use 2024
                year_match = re.search(r'(\d{4})', folder_name)
                target_year = year_match.group(1) if year_match else '2024'
                year_folder = archived_path / target_year
                year_folder.mkdir(exist_ok=True)
                
                for pdf in pdfs:
                    try:
                        new_path = year_folder / pdf.name
                        if new_path.exists():
                            base_name = pdf.stem
                            counter = 1
                            while new_path.exists():
                                new_path = year_folder / f"{base_name}_{counter}.pdf"
                                counter += 1
                        shutil.move(str(pdf), str(new_path))
                    except Exception as e:
                        pass
            
            # Remove the folder if empty
            try:
                if not any(folder.iterdir()):
                    folder.rmdir()
                    removed_folders += 1
            except Exception as e:
                pass
    
    print(f"✓ Removed {removed_files} non-PDF files")
    print(f"✓ Removed {removed_folders} empty course folders")
    
    # Final check: show year folder contents
    print("\nYear folder summary:")
    for year_folder in sorted(archived_path.glob('20*')):
        if year_folder.is_dir():
            pdf_count = len(list(year_folder.glob('*.pdf')))
            if pdf_count > 0:
                print(f"  {year_folder.name}: {pdf_count} PDFs")

if __name__ == '__main__':
    print("=" * 60)
    print("LinkedIn Learning Certificate Organizer")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Extract dates from PDF certificates")
    print("2. Move all PDFs to year folders (2024, 2025, 2026, etc.)")
    print("3. Remove all non-PDF files and course folders")
    print("\nStarting organization...\n")
    
    organize_pdfs()
    
    print("\n" + "=" * 60)
    print("Organization complete!")
    print("=" * 60)
