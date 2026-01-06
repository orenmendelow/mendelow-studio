#!/usr/bin/env python3
"""
Update project HTML pages in new site with extracted content
"""

import json
import os
import re

NEW_SITE = "/Users/oren/Documents/MENDELOW LLC/mendelow-portfolio-clean"
RESULTS_FILE = os.path.join(NEW_SITE, "extraction_results.json")

def read_html_file(filepath):
    """Read HTML file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_html_file(filepath, content):
    """Write HTML file content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def update_project_description(html_content, description):
    """Update the project description in HTML"""
    if not description:
        return html_content
    
    # Find and replace the placeholder description
    # Look for the description paragraph inside the project-content div
    pattern = r'(<div class="project-content">.*?<p>)(.*?)(</p>)'
    replacement = r'\1' + description + r'\3'
    
    updated = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # If that didn't work, try alternate patterns
    if updated == html_content:
        # Try finding just the first <p> tag in project area
        pattern = r'(<section class="project">.*?<p>)(.*?)(</p>)'
        updated = re.sub(pattern, replacement, html_content, count=1, flags=re.DOTALL)
    
    return updated

def update_project_images(html_content, image_paths, project_name):
    """Update project images in HTML"""
    if not image_paths:
        return html_content
    
    # Generate image gallery HTML
    gallery_html = '\n'
    for img_path in image_paths:
        # Skip logo/icon type images for main gallery
        filename = os.path.basename(img_path).lower()
        if 'combined+shape' in filename or 'background' in filename:
            continue
            
        gallery_html += f'''            <div class="gallery-item">
                <img src="{img_path}" alt="{project_name}" loading="lazy">
            </div>\n'''
    
    # Find and replace the gallery placeholder
    pattern = r'(<div class="project-gallery">)(.*?)(</div>\s*</section>)'
    replacement = r'\1' + gallery_html + '        ' + r'\3'
    
    updated = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    return updated

def update_single_project(project_data):
    """Update a single project HTML file"""
    project_name = project_data['name']
    html_file = os.path.join(NEW_SITE, "projects", f"{project_name}.html")
    
    if not os.path.exists(html_file):
        print(f"  ✗ HTML file not found: {project_name}.html")
        return False
    
    print(f"\nUpdating {project_name}.html...")
    
    # Read current HTML
    html_content = read_html_file(html_file)
    
    # Update description if available
    if project_data.get('description'):
        html_content = update_project_description(html_content, project_data['description'])
        print(f"  ✓ Updated description")
    else:
        print(f"  ⚠ No description available")
    
    # Update images if available
    if project_data.get('image_paths'):
        html_content = update_project_images(
            html_content, 
            project_data['image_paths'],
            project_name
        )
        print(f"  ✓ Updated gallery with {project_data['images_copied']} images")
    else:
        print(f"  ⚠ No images available")
    
    # Write updated HTML
    write_html_file(html_file, html_content)
    print(f"  ✓ Saved {project_name}.html")
    
    return True

def main():
    print("Project Page Updater")
    print("=" * 60)
    
    # Load extraction results
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Results file not found at {RESULTS_FILE}")
        return
    
    with open(RESULTS_FILE, 'r') as f:
        results = json.load(f)
    
    print(f"Loaded {len(results)} project results\n")
    
    # Update each project
    updated_count = 0
    for project_data in results:
        if update_single_project(project_data):
            updated_count += 1
    
    print(f"\n{'='*60}")
    print(f"Updated {updated_count} out of {len(results)} project pages")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
