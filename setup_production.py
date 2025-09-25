#!/usr/bin/env python3
"""
Setup script for preparing the Mendelow Studio website for production hosting.
"""

import os
import shutil
import glob
from pathlib import Path

def create_production_structure():
    """Create a clean production-ready directory structure."""
    base_dir = Path('/Users/oren/Documents/MENDELOW LLC/mendelow-studio')
    prod_dir = base_dir / 'www'
    
    # Create production directory
    if prod_dir.exists():
        shutil.rmtree(prod_dir)
    prod_dir.mkdir()
    
    print(f"Creating production structure in: {prod_dir}")
    
    # Copy and rename main files
    file_mappings = {
        'MENDELOW STUDIO.html': 'index.html',
        'Design Services — MENDELOW STUDIO.html': 'design-services.html',
        'Heritage — MENDELOW STUDIO.html': 'heritage.html',
        'Contact — MENDELOW STUDIO.html': 'contact.html',
        "Oren's Portfolio — MENDELOW STUDIO.html": 'oren.html',
    }
    
    # Check which files actually exist and copy them
    for original_name, new_name in file_mappings.items():
        original_path = base_dir / original_name
        if original_path.exists():
            shutil.copy2(original_path, prod_dir / new_name)
            print(f"  ✅ Copied {original_name} → {new_name}")
        else:
            print(f"  ⚠️  File not found: {original_name}")
    
    # Create assets directory and copy all _files
    assets_dir = prod_dir / 'assets'
    assets_dir.mkdir()
    
    # Copy all _files directories to assets
    for files_dir in glob.glob(str(base_dir / '*_files')):
        dir_name = Path(files_dir).name
        target_dir = assets_dir / dir_name
        shutil.copytree(files_dir, target_dir)
        print(f"  📁 Copied {dir_name} to assets/")
    
    # Create .htaccess for Apache servers (if needed)
    htaccess_content = """# Mendelow Studio .htaccess
RewriteEngine On

# Handle clean URLs
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^([^.]+)$ $1.html [L]

# Set cache headers for static assets
<FilesMatch "\\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 year"
</FilesMatch>

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
"""
    
    with open(prod_dir / '.htaccess', 'w') as f:
        f.write(htaccess_content)
    print("  📄 Created .htaccess file")
    
    # Create a simple PHP index for hosting providers that need it
    php_index = """<?php
// Simple redirect to handle directory access
if (file_exists('index.html')) {
    header('Location: index.html');
    exit;
}
?>"""
    
    with open(prod_dir / 'index.php', 'w') as f:
        f.write(php_index)
    print("  🐘 Created index.php redirect")
    
    return prod_dir

def update_production_links(prod_dir):
    """Update links in the production files to work with the new structure."""
    print("\nUpdating links for production...")
    
    for html_file in glob.glob(str(prod_dir / '*.html')):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update asset paths to point to the assets directory
        content = content.replace('./MENDELOW STUDIO_files/', './assets/MENDELOW STUDIO_files/')
        content = content.replace('./Design Services — MENDELOW STUDIO_files/', './assets/Design Services — MENDELOW STUDIO_files/')
        content = content.replace('./Heritage — MENDELOW STUDIO_files/', './assets/Heritage — MENDELOW STUDIO_files/')
        content = content.replace('./Contact — MENDELOW STUDIO_files/', './assets/Contact — MENDELOW STUDIO_files/')
        content = content.replace("./Oren's Portfolio — MENDELOW STUDIO_files/", "./assets/Oren's Portfolio — MENDELOW STUDIO_files/")
        
        # Update internal navigation links
        link_mappings = {
            'href="/shop"': 'href="/shop.html"',  # If you have this page
            'href="/design-services"': 'href="/design-services.html"',
            'href="/heritage"': 'href="/heritage.html"',
            'href="/contact"': 'href="/contact.html"',
            'href="/oren"': 'href="/oren.html"',
        }
        
        for old_link, new_link in link_mappings.items():
            content = content.replace(old_link, new_link)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Updated {Path(html_file).name}")

def main():
    print("🏗️  Setting up Mendelow Studio for production hosting")
    print("=" * 60)
    
    prod_dir = create_production_structure()
    update_production_links(prod_dir)
    
    print("=" * 60)
    print("✅ Production setup complete!")
    print(f"\n📁 Production files are ready in: {prod_dir}")
    print("\n🚀 Hosting options:")
    print("1. Upload the 'www' folder contents to your web hosting provider")
    print("2. Use services like Netlify, Vercel, or GitHub Pages")
    print("3. Set up your own VPS with Apache/Nginx")
    print("\n💡 Next steps:")
    print("1. Test the production files locally with a web server")
    print("2. Update any remaining absolute URLs to your new domain")
    print("3. Set up SSL certificate for your domain")

if __name__ == "__main__":
    main()
