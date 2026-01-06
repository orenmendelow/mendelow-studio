"""
Categorize portfolio projects into logical groups
"""

import json
from pathlib import Path

def categorize_projects():
    """Categorize all projects"""
    
    workspace_dir = Path(__file__).parent
    json_file = workspace_dir / 'portfolio_projects.json'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    
    # Define categories
    categories = {
        'Product Design & Fabrication': [
            'Pomander Walk',
            'KOALA BOARDS',
            'Butter Mounts',
            'No Mess Cutting Board Oiling Tool',
            'Handcrafted Birch Portafilter Dock',
            'Bench Swing',
            'Custom Espresso Station',
            'Oil Drum Fire Pit',
            'Minibike Build',
            'Homemade Vacuum Former'
        ],
        'Digital Design & Apps': [
            'Alto',
            'Pa+ched',
            'Yurtle'
        ],
        'Branding & Marketing': [
            'SZZL',
            'PooPalz'
        ],
        'Visual Media': [
            'Photography',
            'Videography',
            'Stop Motion'
        ],
        'Art & Illustration': [
            'Wood Art',
            'Drawing',
            'Art Gallery Proposal'
        ],
        'Merchandise': [
            '5 panel hat',
            'dad hat',
            'beanie',
            'hoodie',
            'tee'
        ]
    }
    
    # Categorize projects
    categorized = {}
    uncategorized = []
    
    for project in projects:
        title = project['title']
        found = False
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(project)
                    found = True
                    break
            if found:
                break
        
        if not found:
            uncategorized.append(project)
    
    # Create categorized markdown
    md_output = workspace_dir / 'PORTFOLIO_CATEGORIZED.md'
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("# Portfolio Projects by Category\n\n")
        f.write(f"**Total Projects:** {len(projects)}\n\n")
        
        for category in categories.keys():
            if category in categorized:
                f.write(f"## {category}\n\n")
                f.write(f"*{len(categorized[category])} projects*\n\n")
                
                for project in categorized[category]:
                    f.write(f"### {project['title']}\n\n")
                    if project['description']:
                        f.write(f"{project['description']}\n\n")
                    f.write(f"- **Images:** {len(project['images'])}\n")
                    f.write(f"- **Videos:** {len(project['videos'])}\n")
                    f.write(f"- **File:** `{project['filename']}`\n\n")
        
        if uncategorized:
            f.write(f"## Uncategorized\n\n")
            for project in uncategorized:
                f.write(f"- {project['title']}\n")
    
    # Create stats summary
    stats_output = workspace_dir / 'PORTFOLIO_STATS.md'
    with open(stats_output, 'w', encoding='utf-8') as f:
        f.write("# Portfolio Statistics\n\n")
        
        total_images = sum(len(p['images']) for p in projects)
        total_videos = sum(len(p['videos']) for p in projects)
        total_text_blocks = sum(len(p['text_content']) for p in projects)
        
        f.write(f"## Overview\n\n")
        f.write(f"- **Total Projects:** {len(projects)}\n")
        f.write(f"- **Total Images:** {total_images}\n")
        f.write(f"- **Total Videos:** {total_videos}\n")
        f.write(f"- **Total Text Blocks:** {total_text_blocks}\n\n")
        
        f.write(f"## By Category\n\n")
        for category, keywords in categories.items():
            if category in categorized:
                count = len(categorized[category])
                images = sum(len(p['images']) for p in categorized[category])
                videos = sum(len(p['videos']) for p in categorized[category])
                f.write(f"### {category}\n")
                f.write(f"- Projects: {count}\n")
                f.write(f"- Images: {images}\n")
                f.write(f"- Videos: {videos}\n\n")
        
        f.write(f"## Top Projects by Image Count\n\n")
        sorted_by_images = sorted(projects, key=lambda x: len(x['images']), reverse=True)
        for i, project in enumerate(sorted_by_images[:10], 1):
            f.write(f"{i}. **{project['title']}** - {len(project['images'])} images\n")
        
        f.write(f"\n## Projects with Videos\n\n")
        video_projects = [p for p in projects if len(p['videos']) > 0]
        for project in video_projects:
            f.write(f"- **{project['title']}** - {len(project['videos'])} video(s)\n")
    
    print(f"✓ Created categorized summary: {md_output}")
    print(f"✓ Created statistics: {stats_output}")
    
    print(f"\n📊 Summary:")
    print(f"Total projects: {len(projects)}")
    print(f"Total images: {total_images}")
    print(f"Total videos: {total_videos}")
    print(f"\nCategories:")
    for category, keywords in categories.items():
        if category in categorized:
            print(f"  {category}: {len(categorized[category])} projects")

if __name__ == '__main__':
    categorize_projects()
