#!/bin/bash

# Switch between GitHub Pages and custom domain
# Usage: ./switch_domain.sh github  or  ./switch_domain.sh custom

if [ "$1" = "github" ]; then
    echo "Switching to GitHub Pages URLs..."
    find . -name '*.html' -exec sed -i '' 's|<base href="/.*">|<base href="/mendelow-studio/">|g' {} \;
    echo "✅ All pages now use GitHub Pages base URL"
elif [ "$1" = "custom" ]; then
    echo "Switching to custom domain URLs..."
    find . -name '*.html' -exec sed -i '' 's|<base href="/.*">|<base href="/">|g' {} \;
    echo "✅ All pages now use custom domain base URL"
else
    echo "Usage: ./switch_domain.sh [github|custom]"
    echo "  github - Switch to GitHub Pages URLs (/mendelow-studio/)"
    echo "  custom - Switch to custom domain URLs (/)"
fi
