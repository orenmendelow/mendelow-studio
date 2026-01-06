#!/usr/bin/env python3
"""
Script to systematically extract content from old portfolio site
and populate new clean site
"""

import os
import shutil
from pathlib import Path
import re
from bs4 import BeautifulSoup

OLD_SITE = "/Users/oren/Documents/MENDELOW LLC/mendelow-studio"
NEW_SITE = "/Users/oren/Documents/MENDELOW LLC/mendelow-portfolio-clean"

# Project mappings: new site name -> old site directory patterns
PROJECTS = {
    "alto": ["alto", "alto-_-app-design"],
    "patched": ["patched", "pached-_-mobile-app-design"],
    "yurtle": ["yurtle", "yurtle-_-branding-identity"],
    "szzl": ["szzl"],
    "poopalz": ["poopalz"],
    "koala-boards": ["koala-boards", "koala-boards-_-about", "koala-boards-_-board-backpack-bundle"],
    "diamond-farms": ["diamond-farms"],
    "custom-espresso-station": ["custom-espresso-station"],
    "bench-swing": ["bench-swing"],
    "minibike-build": ["minibike-build"],
    "oil-drum-fire-pit": ["oil-drum-fire-pit"],
    "butter-mounts": ["butter-mounts"],
    "vacuum-former": ["homemade-vacuum-former"],
    "portafilter-dock": ["handcrafted-birch-portafilter-dock"],
    "cutting-board-tool": ["no-mess-cutting-board-oiling-tool"],
    "pomander-walk": ["_pomander-walk_-by-oren"],
    "pomander-walk-consultation": ["_pomander-walk_-artist-consultation"],
    "ketubah": ["ketubah"],
    "art-gallery-proposal": ["art-gallery-proposal"],
    "meridian-clock": ["meridian-artisan-clock"],
    "photography": ["photography"],
    "videography": ["videography"],
    "stop-motion": ["stop-motion"],
    "5-panel-hat": ["5-panel-hat"],
    "dad-hat": ["dad-hat"],
    "beanie": ["beanie"],
    "hoodie": ["hoodie"],
    "tee": ["tee"]
}

CATEGORIES = {
    "digital-design": ["alto", "patched", "yurtle", "szzl", "poopalz", "koala-boards", "diamond-farms"],
    "fabrication": ["custom-espresso-station", "bench-swing", "minibike-build", "oil-drum-fire-pit", "butter-mounts", "vacuum-former"],
    "woodwork": ["portafilter-dock", "cutting-board-tool"],
    "art": ["pomander-walk", "pomander-walk-consultation", "ketubah", "art-gallery-proposal", "meridian-clock"],
    "media": ["photography", "videography", "stop-motion"],
    "apparel": ["5-panel-hat", "dad-hat", "beanie", "hoodie", "tee"]
}

def get_category(project):
    """Get category for a project"""
    for category, projects in CATEGORIES.items():
        if project in projects:
            return category
    return "other"

def find_project_directory(project_name):
    """Find the actual directory for a project in old site"""
    patterns = PROJECTS.get(project_name, [])
    for pattern in patterns:
        dir_path = os.path.join(OLD_SITE, pattern)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            return dir_path
    return None

def find_project_files_directory(project_name):
    """Find the _files directory that contains actual assets"""
    # Look for HTML files matching project patterns
    patterns = PROJECTS.get(project_name, [])
    
    # Common file naming patterns for the _files directories
    file_patterns = []
    for p in patterns:
        # Convert pattern to likely HTML file names
        file_patterns.append(f"{p} — MENDELOW STUDIO_files")
        file_patterns.append(f"{p.replace('-', ' ').title()} — MENDELOW STUDIO_files")
        file_patterns.append(f"_{p}_ — MENDELOW STUDIO_files")
    
    for pattern in file_patterns:
        dir_path = os.path.join(OLD_SITE, pattern)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            return dir_path
    
    return None

def find_project_images(project_name):
    """Find all images in a project's _files directory"""
    images = []
    
    # Look in the _files directory which contains actual assets
    files_dir = find_project_files_directory(project_name)
    
    if files_dir and os.path.exists(files_dir):
        for file in os.listdir(files_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                file_path = os.path.join(files_dir, file)
                if os.path.isfile(file_path):
                    images.append(file_path)
    
    return images

def copy_images_to_new_site(images, project_name, category):
    """Copy images to new site organized by category"""
    if not images:
        return []
    
    target_dir = os.path.join(NEW_SITE, "images", category, project_name)
    os.makedirs(target_dir, exist_ok=True)
    
    copied_files = []
    for img_path in images:
        filename = os.path.basename(img_path)
        target_path = os.path.join(target_dir, filename)
        
        try:
            shutil.copy2(img_path, target_path)
            # Return relative path for HTML
            rel_path = f"../images/{category}/{project_name}/{filename}"
            copied_files.append(rel_path)
            print(f"  ✓ Copied: {filename}")
        except Exception as e:
            print(f"  ✗ Error copying {filename}: {e}")
    
    return copied_files

def extract_description_from_html(html_file):
    """Extract project description from old HTML file"""
    if not os.path.exists(html_file):
        return ""
    
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Try to find meta description
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
        if desc_match and desc_match.group(1):
            return desc_match.group(1)
        
        # Try to extract paragraphs from the content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for content paragraphs (skip nav, header, footer)
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            # Skip empty, very short, or navigation text
            if text and len(text) > 50 and not any(x in text.lower() for x in ['menu', 'copyright', 'follow', 'subscribe']):
                return text
        
        return ""
    except Exception as e:
        print(f"  ✗ Error reading HTML: {e}")
        return ""

def process_project(project_name):
    """Process a single project"""
    print(f"\n{'='*60}")
    print(f"Processing: {project_name.upper()}")
    print(f"{'='*60}")
    
    category = get_category(project_name)
    project_dir = find_project_directory(project_name)
    
    if not project_dir:
        print(f"  ⚠ Could not find directory for {project_name}")
        return {
            "name": project_name,
            "category": category,
            "found": False,
            "images_copied": 0,
            "description": ""
        }
    
    print(f"  Found directory: {project_dir}")
    
    # Find images
    images = find_project_images(project_name)
    files_dir = find_project_files_directory(project_name)
    if files_dir:
        print(f"  Found assets directory: {files_dir}")
    print(f"  Found {len(images)} images")
    
    # Copy images
    copied_images = copy_images_to_new_site(images, project_name, category)
    print(f"  Copied {len(copied_images)} images to new site")
    
    # Try to find HTML file for description
    html_patterns = [
        f"{p} — MENDELOW STUDIO.html" for p in PROJECTS.get(project_name, [])
    ]
    html_patterns.extend([
        f"{p.replace('-', ' ').title()} — MENDELOW STUDIO.html" for p in PROJECTS.get(project_name, [])
    ])
    
    description = ""
    for pattern in html_patterns:
        html_file = os.path.join(OLD_SITE, pattern)
        if os.path.exists(html_file):
            print(f"  Found HTML file: {pattern}")
            description = extract_description_from_html(html_file)
            if description:
                print(f"  ✓ Extracted description: {description[:100]}...")
                break
    
    if not description:
        print(f"  ⚠ No description found")
    
    return {
        "name": project_name,
        "category": category,
        "found": True,
        "directory": project_dir,
        "images_found": len(images),
        "images_copied": len(copied_images),
        "image_paths": copied_images,
        "description": description
    }

def generate_summary_report(results):
    """Generate a summary report"""
    print(f"\n\n{'='*60}")
    print("SUMMARY REPORT")
    print(f"{'='*60}\n")
    
    total_projects = len(results)
    found_projects = sum(1 for r in results if r.get('found', False))
    total_images = sum(r.get('images_copied', 0) for r in results)
    projects_with_desc = sum(1 for r in results if r.get('description', ''))
    
    print(f"Projects processed: {total_projects}")
    print(f"Projects found: {found_projects}")
    print(f"Total images copied: {total_images}")
    print(f"Projects with descriptions: {projects_with_desc}")
    
    print(f"\n\nDETAILED RESULTS BY CATEGORY:")
    print(f"{'='*60}\n")
    
    for category, projects in CATEGORIES.items():
        print(f"\n{category.upper().replace('-', ' ')}:")
        print("-" * 40)
        
        for project in projects:
            result = next((r for r in results if r['name'] == project), None)
            if result:
                status = "✓" if result.get('found') else "✗"
                images = result.get('images_copied', 0)
                desc_status = "✓" if result.get('description') else "✗"
                print(f"  {status} {project:30s} | Images: {images:3d} | Desc: {desc_status}")

def main():
    print(f"\nPortfolio Content Extractor")
    print(f"Old site: {OLD_SITE}")
    print(f"New site: {NEW_SITE}")
    
    results = []
    
    # Process all projects
    for category, projects in CATEGORIES.items():
        for project in projects:
            result = process_project(project)
            results.append(result)
    
    # Generate summary
    generate_summary_report(results)
    
    # Save results to JSON for later use
    import json
    results_file = os.path.join(NEW_SITE, "extraction_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\n✓ Results saved to: {results_file}")

if __name__ == "__main__":
    main()
