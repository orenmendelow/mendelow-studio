#!/usr/bin/env python3
"""
Setup script specifically for GitHub Pages deployment.
Creates the proper structure and configuration for GitHub Pages hosting.
"""

import os
import shutil
import glob
import json
from pathlib import Path

def create_github_pages_structure():
    """Create a GitHub Pages ready directory structure."""
    base_dir = Path('/Users/oren/Documents/MENDELOW LLC/mendelow-studio')
    
    print(f"Setting up GitHub Pages structure in: {base_dir}")
    
    # File mappings for clean URLs
    file_mappings = {
        'MENDELOW STUDIO.html': 'index.html',
        'Design Services — MENDELOW STUDIO.html': 'design-services.html',
        'Heritage — MENDELOW STUDIO.html': 'heritage.html', 
        'Contact — MENDELOW STUDIO.html': 'contact.html',
        "Oren's Portfolio — MENDELOW STUDIO.html": 'oren.html',
    }
    
    # Rename main files for GitHub Pages
    for original_name, new_name in file_mappings.items():
        original_path = base_dir / original_name
        new_path = base_dir / new_name
        
        if original_path.exists() and not new_path.exists():
            shutil.copy2(original_path, new_path)
            print(f"  ✅ Created {new_name}")
        elif new_path.exists():
            print(f"  ℹ️  {new_name} already exists")
        else:
            print(f"  ⚠️  Source file not found: {original_name}")
    
    # Create _config.yml for Jekyll (GitHub Pages)
    jekyll_config = """# GitHub Pages Jekyll Configuration
title: "MENDELOW STUDIO"
description: "Design, fabrication, and creative services"
url: "https://orenmendelow.github.io"
baseurl: "/mendelow-studio"

# Disable Jekyll processing for static files
include:
  - "_*"

# Keep asset files
keep_files:
  - "assets"

# Exclude files from processing
exclude:
  - "*.py"
  - "README.md"
  - "*.md"
  - "serve.py"
  - "fix_links.py"
  - "setup_production.py"
  - "setup_github_pages.py"

# Plugins
plugins:
  - jekyll-relative-links

# Settings
markdown: kramdown
highlighter: rouge
"""
    
    config_path = base_dir / '_config.yml'
    with open(config_path, 'w') as f:
        f.write(jekyll_config)
    print("  📄 Created _config.yml for Jekyll")
    
    # Create .nojekyll file to bypass Jekyll processing if needed
    nojekyll_path = base_dir / '.nojekyll'
    nojekyll_path.touch()
    print("  📄 Created .nojekyll file")
    
    # Create GitHub Actions workflow for deployment
    github_dir = base_dir / '.github' / 'workflows'
    github_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    
    workflow_path = github_dir / 'deploy.yml'
    with open(workflow_path, 'w') as f:
        f.write(workflow_content)
    print("  ⚙️  Created GitHub Actions workflow")
    
    return base_dir

def update_links_for_github_pages(base_dir):
    """Update links specifically for GitHub Pages with repository name in URL."""
    print("\nUpdating links for GitHub Pages...")
    
    # GitHub Pages URL structure: https://username.github.io/repository-name/
    base_url = "/mendelow-studio"
    
    html_files = [
        'index.html',
        'design-services.html', 
        'heritage.html',
        'contact.html',
        'oren.html'
    ]
    
    for html_file in html_files:
        file_path = base_dir / html_file
        if not file_path.exists():
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update internal navigation links for GitHub Pages
        link_mappings = {
            'href="/"': f'href="{base_url}/"',
            'href="/design-services"': f'href="{base_url}/design-services"',
            'href="/heritage"': f'href="{base_url}/heritage"',
            'href="/contact"': f'href="{base_url}/contact"',
            'href="/oren"': f'href="{base_url}/oren"',
            'href="/shop"': f'href="{base_url}/shop"',
            'href="/cart"': f'href="{base_url}/cart"',
        }
        
        for old_link, new_link in link_mappings.items():
            content = content.replace(old_link, new_link)
        
        # Update asset paths to be relative (GitHub Pages handles this well)
        # Keep the existing relative paths as they are
        
        # Update meta tags for the new domain
        content = content.replace(
            'https://www.mendelow.studio',
            'https://orenmendelow.github.io/mendelow-studio'
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Updated {html_file}")
        else:
            print(f"  ℹ️  No changes needed in {html_file}")

def create_github_readme():
    """Create a GitHub-specific README."""
    readme_content = """# Mendelow Studio

A creative design studio website featuring portfolio work, services, and heritage pieces.

## 🌐 Live Site

Visit the live website: [https://orenmendelow.github.io/mendelow-studio/](https://orenmendelow.github.io/mendelow-studio/)

## 📁 Project Structure

This is a static website converted from Squarespace, optimized for GitHub Pages hosting.

- `index.html` - Home page
- `design-services.html` - Design & Software Services
- `heritage.html` - Heritage collection
- `contact.html` - Contact information
- `oren.html` - Portfolio
- `*_files/` - Asset directories (CSS, JS, images)

## 🚀 Local Development

To run locally:

```bash
python3 serve.py
```

Then visit http://localhost:8000

## 🔧 Technologies

- Static HTML/CSS/JavaScript
- GitHub Pages hosting
- Jekyll for deployment
- Responsive design

## 📝 License

All rights reserved.
"""
    
    base_dir = Path('/Users/oren/Documents/MENDELOW LLC/mendelow-studio')
    readme_path = base_dir / 'README.md'
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print("  📝 Created GitHub README.md")

def main():
    print("🐙 Setting up Mendelow Studio for GitHub Pages")
    print("=" * 60)
    
    base_dir = create_github_pages_structure()
    update_links_for_github_pages(base_dir)
    create_github_readme()
    
    print("=" * 60)
    print("✅ GitHub Pages setup complete!")
    print("\n📋 Next steps:")
    print("1. Commit and push all files to your GitHub repository")
    print("2. Go to your repository settings on GitHub")
    print("3. Navigate to 'Pages' section")
    print("4. Select 'Deploy from a branch' as source")
    print("5. Choose 'main' (or 'master') branch")
    print("6. Your site will be available at:")
    print("   https://orenmendelow.github.io/mendelow-studio/")
    print("\n💡 Pro tips:")
    print("- GitHub Pages may take a few minutes to update")
    print("- You can use a custom domain by adding a CNAME file")
    print("- All pushes to main/master branch will auto-deploy")

if __name__ == "__main__":
    main()
