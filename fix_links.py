#!/usr/bin/env python3
"""
Script to fix internal links in the saved Squarespace HTML files.
This converts absolute Squarespace URLs to relative URLs for local hosting.
"""

import os
import re
import glob
from pathlib import Path

def fix_html_file(file_path):
    """Fix the links in a single HTML file."""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # URL mappings from Squarespace URLs to local routes
    url_mappings = {
        'https://www.mendelow.studio/': '/',
        'https://www.mendelow.studio/shop': '/shop',
        'https://www.mendelow.studio/design-services': '/design-services',
        'https://www.mendelow.studio/heritage': '/heritage',
        'https://www.mendelow.studio/contact': '/contact',
        'https://www.mendelow.studio/oren': '/oren',
        'https://www.mendelow.studio/cart': '/cart',
    }
    
    # Replace internal links
    for original_url, new_url in url_mappings.items():
        content = content.replace(f'href="{original_url}"', f'href="{new_url}"')
    
    # Fix canonical URLs to point to your new domain (you'll replace this later)
    content = re.sub(
        r'<link rel="canonical" href="https://www\.mendelow\.studio/[^"]*">',
        '<link rel="canonical" href="/">',
        content
    )
    
    # Fix Open Graph URLs
    content = re.sub(
        r'<meta property="og:url" content="https://www\.mendelow\.studio[^"]*">',
        '<meta property="og:url" content="/">',
        content
    )
    
    # Fix Twitter URLs
    content = re.sub(
        r'<meta name="twitter:url" content="https://www\.mendelow\.studio[^"]*">',
        '<meta name="twitter:url" content="/">',
        content
    )
    
    # Write back if there were changes
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Updated links in {file_path}")
    else:
        print(f"  ℹ️  No changes needed in {file_path}")

def main():
    """Fix all HTML files in the directory."""
    base_dir = '/Users/oren/Documents/MENDELOW LLC/mendelow-studio'
    os.chdir(base_dir)
    
    # Find all HTML files (excluding those in _files directories for now)
    html_files = glob.glob('*.html')
    
    print(f"Found {len(html_files)} HTML files to process")
    print("=" * 50)
    
    for html_file in html_files:
        fix_html_file(html_file)
    
    print("=" * 50)
    print("✅ Link fixing complete!")
    print("\nNext steps:")
    print("1. Run 'python3 serve.py' to start the development server")
    print("2. Open http://localhost:8000 in your browser")
    print("3. Test all navigation links")

if __name__ == "__main__":
    main()
