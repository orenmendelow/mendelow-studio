#!/bin/bash
# GitHub Pages Deployment Script
# This script helps you deploy your Mendelow Studio website to GitHub Pages

echo "🐙 GitHub Pages Deployment Helper"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Check if remote is set
if ! git remote get-url origin &>/dev/null; then
    echo ""
    echo "🔗 You need to set up your GitHub repository remote."
    echo "   1. Go to https://github.com/new"
    echo "   2. Create a repository named 'mendelow-studio'"
    echo "   3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL (https://github.com/username/mendelow-studio.git): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote origin set to: $repo_url"
    else
        echo "❌ No repository URL provided. Please run this script again."
        exit 1
    fi
fi

# Add all files
echo ""
echo "📦 Adding files to git..."
git add .

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]

# macOS
.DS_Store

# Temporary files
*.tmp
*.bak

# Local development
node_modules/
EOF
    git add .gitignore
fi

# Commit
echo "💾 Committing changes..."
git commit -m "Initial commit: Mendelow Studio website for GitHub Pages"

# Get current branch name
current_branch=$(git branch --show-current)
if [ -z "$current_branch" ]; then
    current_branch="main"
    git checkout -b main
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git push -u origin "$current_branch"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository: https://github.com/orenmendelow/mendelow-studio"
echo "2. Click on 'Settings' tab"
echo "3. Scroll down to 'Pages' section on the left sidebar"
echo "4. Under 'Source', select 'Deploy from a branch'"
echo "5. Choose '$current_branch' branch and '/ (root)' folder"
echo "6. Click 'Save'"
echo ""
echo "🌐 Your website will be available at:"
echo "   https://orenmendelow.github.io/mendelow-studio/"
echo ""
echo "⏱️  Note: It may take 5-10 minutes for the site to be live after setup."
