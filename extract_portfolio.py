"""
Portfolio Project Extractor
Extracts project information from MENDELOW STUDIO HTML files
"""

import os
import re
import json
from bs4 import BeautifulSoup
from pathlib import Path

def extract_project_info(html_file):
    """Extract project information from an HTML file"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    project = {
        'filename': os.path.basename(html_file),
        'title': '',
        'description': '',
        'images': [],
        'text_content': [],
        'videos': []
    }
    
    # Extract title from <title> tag
    title_tag = soup.find('title')
    if title_tag:
        project['title'] = title_tag.text.replace(' — MENDELOW STUDIO', '').strip()
    
    # Extract main content paragraphs
    paragraphs = soup.find_all('p', class_=re.compile(r'sqsrte-large|preFade'))
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text and len(text) > 10:  # Filter out very short text
            project['text_content'].append(text)
    
    # Extract all text from divs that might contain descriptions
    content_divs = soup.find_all('div', class_=re.compile(r'sqs-html-content'))
    for div in content_divs:
        text = div.get_text(strip=True)
        if text and len(text) > 20:
            if text not in project['text_content']:
                project['text_content'].append(text)
    
    # Extract images
    images = soup.find_all('img')
    for img in images:
        src = img.get('data-src') or img.get('src')
        if src and not any(x in src for x in ['logo', 'icon', 'avatar']):
            alt = img.get('alt', '')
            project['images'].append({
                'src': src,
                'alt': alt
            })
    
    # Extract videos
    videos = soup.find_all(['video', 'iframe'])
    for video in videos:
        src = video.get('src') or video.get('data-src')
        if src:
            project['videos'].append(src)
    
    # Get first substantial description
    if project['text_content']:
        project['description'] = project['text_content'][0]
    
    return project

def main():
    """Main extraction function"""
    
    workspace_dir = Path(__file__).parent
    
    # Find all HTML files that match the pattern
    html_files = list(workspace_dir.glob('*— MENDELOW STUDIO.html'))
    
    # Exclude only navigation/category pages (not actual project pages)
    exclude_files = [
        'Oren\'s Portfolio — MENDELOW STUDIO.html',
        'MENDELOW STUDIO.html',
        'Contact — MENDELOW STUDIO.html',
        'Design Services — MENDELOW STUDIO.html',
        'Media — MENDELOW STUDIO.html',
        'Art — MENDELOW STUDIO.html',
        'Digital Design — MENDELOW STUDIO.html',
        'Fabrication — MENDELOW STUDIO.html',
        'Heritage — MENDELOW STUDIO.html',
        'General 1 — MENDELOW STUDIO.html',
        '404.html'
    ]
    
    projects = []
    
    for html_file in html_files:
        filename = html_file.name
        
        # Skip excluded files
        if filename in exclude_files:
            print(f"Skipping: {filename}")
            continue
        
        print(f"Processing: {filename}")
        
        try:
            project_info = extract_project_info(html_file)
            projects.append(project_info)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Sort projects by title
    projects.sort(key=lambda x: x['title'])
    
    # Save to JSON
    output_file = workspace_dir / 'portfolio_projects.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Extracted {len(projects)} projects")
    print(f"✓ Saved to: {output_file}")
    
    # Create a markdown summary
    md_output = workspace_dir / 'PORTFOLIO_SUMMARY.md'
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("# Portfolio Projects Summary\n\n")
        f.write(f"Total Projects: {len(projects)}\n\n")
        f.write("---\n\n")
        
        for project in projects:
            f.write(f"## {project['title']}\n\n")
            
            if project['description']:
                f.write(f"{project['description']}\n\n")
            
            if project['text_content']:
                f.write("**Content:**\n")
                for text in project['text_content'][:3]:  # First 3 text blocks
                    f.write(f"- {text}\n")
                f.write("\n")
            
            f.write(f"**Images:** {len(project['images'])}\n")
            f.write(f"**Videos:** {len(project['videos'])}\n\n")
            f.write("---\n\n")
    
    print(f"✓ Created markdown summary: {md_output}")
    
    # Print project list
    print("\n📁 Projects found:")
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project['title']}")

if __name__ == '__main__':
    main()
