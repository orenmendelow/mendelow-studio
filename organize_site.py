#!/usr/bin/env python3
"""
Complete site organization script - creates clean URLs for ALL pages and fixes asset paths
"""
import os
import shutil
import re
import urllib.parse
from pathlib import Path

def create_clean_url_structure():
    """Organize ALL pages into clean URL structure"""
    base_dir = Path("/Users/oren/Documents/MENDELOW LLC/mendelow-studio")
    os.chdir(base_dir)
    
    print("🏗️  Organizing ALL pages into clean URL structure...")
    
    # Get all HTML files except index.html and the main MENDELOW STUDIO.html
    html_files = [f for f in os.listdir(".") if f.endswith(".html") and f not in ["index.html", "MENDELOW STUDIO.html"]]
    
    # Create directories and copy files for each project
    for html_file in html_files:
        # Create clean URL slug from filename
        # Remove " — MENDELOW STUDIO.html" suffix
        clean_name = html_file.replace(" — MENDELOW STUDIO.html", "")
        # Convert to URL-friendly slug
        slug = clean_name.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars except spaces and hyphens
        slug = re.sub(r'[-\s]+', '-', slug)   # Replace spaces and multiple hyphens with single hyphen
        slug = slug.strip('-')                # Remove leading/trailing hyphens
        
        print(f"📄 {html_file} -> /{slug}/")
        
        # Create directory
        page_dir = Path(slug)
        page_dir.mkdir(exist_ok=True)
        
        # Copy HTML file as index.html
        shutil.copy2(html_file, page_dir / "index.html")

def fix_asset_paths():
    """Fix asset paths in all HTML files"""
    print("\n🔧 Fixing asset paths...")
    
    # Fix paths in all index.html files in subdirectories
    for root, dirs, files in os.walk("."):
        if "index.html" in files and root != ".":
            html_path = Path(root) / "index.html"
            print(f"Fixing paths in: {html_path}")
            
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count directory depth to determine how many "../" needed
            depth = len(Path(root).parts) - 1
            prefix = "../" * depth
            
            # Fix asset paths (./filename_files/ -> ../filename_files/)
            content = re.sub(r'\./([^/]+_files/)', f'{prefix}\\1', content)
            
            # Fix internal navigation links
            nav_fixes = {
                'href="https://www.mendelow.studio/"': f'href="{prefix}"',
                'href="https://www.mendelow.studio/design-services"': f'href="{prefix}design-services/"',
                'href="https://www.mendelow.studio/heritage"': f'href="{prefix}heritage/"',
                'href="https://www.mendelow.studio/contact"': f'href="{prefix}contact/"',
                'href="https://www.mendelow.studio/oren"': f'href="{prefix}oren/"',
                'href="/"': f'href="{prefix}"',
                'href="/design-services/"': f'href="{prefix}design-services/"',
                'href="/heritage/"': f'href="{prefix}heritage/"',
                'href="/contact/"': f'href="{prefix}contact/"',
                'href="/oren/"': f'href="{prefix}oren/"',
            }
            
            for old, new in nav_fixes.items():
                content = content.replace(old, new)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)

def fix_main_page_links():
    """Fix links in main pages to point to new clean URLs"""
    print("\n🔗 Fixing navigation links in main pages...")
    
    # List of all project slugs that now exist
    project_dirs = [d for d in os.listdir(".") if os.path.isdir(d) and d not in [".git", "contact", "design-services", "heritage", "oren"]]
    
    # Fix links in main pages
    main_pages = ["index.html", "contact/index.html", "design-services/index.html", "heritage/index.html", "oren/index.html"]
    
    for main_page in main_pages:
        if os.path.exists(main_page):
            with open(main_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix any remaining Squarespace URLs that might be pointing to projects
            # This is a comprehensive approach - we'll look for patterns and fix them
            
            # Example: href="/shop//p/no-mess-cutting-board-oiling-tool" -> href="/no-mess-cutting-board-oiling-tool/"
            content = re.sub(r'href="/shop//p/([^"]+)"', r'href="/\1/"', content)
            
            with open(main_page, 'w', encoding='utf-8') as f:
                f.write(content)

def main():
    print("🚀 COMPLETE SITE ORGANIZATION STARTING...")
    print("=" * 60)
    
    create_clean_url_structure()
    fix_asset_paths() 
    fix_main_page_links()
    
    print("=" * 60)
    print("✅ SITE ORGANIZATION COMPLETE!")
    print("\n📋 What was created:")
    
    # List all directories created
    dirs = [d for d in os.listdir(".") if os.path.isdir(d) and not d.startswith(".")]
    print(f"Created {len(dirs)} project pages with clean URLs:")
    for directory in sorted(dirs)[:10]:  # Show first 10
        print(f"  • /{directory}/")
    if len(dirs) > 10:
        print(f"  ... and {len(dirs) - 10} more!")
    
    print("\n🌐 Your site structure:")
    print("  • https://orenmendelow.github.io/mendelow-studio/ (homepage)")
    print("  • https://orenmendelow.github.io/mendelow-studio/design-services/")
    print("  • https://orenmendelow.github.io/mendelow-studio/heritage/") 
    print("  • https://orenmendelow.github.io/mendelow-studio/contact/")
    print("  • https://orenmendelow.github.io/mendelow-studio/oren/")
    print("  • Plus all your individual project pages!")
    
    print("\n🔄 Next steps:")
    print("1. git add .")
    print("2. git commit -m 'Organize all pages with clean URLs'")
    print("3. git push origin master")
    print("4. Wait 2-3 minutes for GitHub Pages to rebuild")

if __name__ == "__main__":
    main()
