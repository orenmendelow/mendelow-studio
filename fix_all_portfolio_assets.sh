#!/bin/bash

# Fix all portfolio page asset paths systematically
cd "/Users/oren/Documents/MENDELOW LLC/mendelow-studio"

# Array of pages that need fixing with their corresponding asset folder names
declare -A pages=(
    ["media"]="Media — MENDELOW STUDIO_files"
    ["wood-art"]="Wood Art — MENDELOW STUDIO_files"
    ["drawing"]="Drawing — MENDELOW STUDIO_files"
    ["photography"]="Photography — MENDELOW STUDIO_files"
    ["custom-espresso-station"]="Custom Espresso Station — MENDELOW STUDIO_files"
    ["fabrication"]="Fabrication — MENDELOW STUDIO_files"
    ["videography"]="Videography — MENDELOW STUDIO_files"
    ["stop-motion"]="Stop Motion — MENDELOW STUDIO_files"
)

for page in "${!pages[@]}"; do
    asset_folder="${pages[$page]}"
    echo "Fixing $page with asset folder $asset_folder"
    
    cd "$page"
    
    # Fix the main CSS file
    sed -i '' "s|href=\"../site.css\"|href=\"../$asset_folder/site.css\"|g" index.html
    
    # Fix JavaScript files
    sed -i '' "s|src=\"../legacy.js\"|src=\"../$asset_folder/legacy.js\"|g" index.html
    sed -i '' "s|src=\"../modern.js\"|src=\"../$asset_folder/modern.js\"|g" index.html
    
    # Fix other common asset references
    sed -i '' "s|src=\"../extract-css-runtime|src=\"../$asset_folder/extract-css-runtime|g" index.html
    sed -i '' "s|src=\"../extract-css-moment|src=\"../$asset_folder/extract-css-moment|g" index.html
    sed -i '' "s|src=\"../cldr-resource-pack|src=\"../$asset_folder/cldr-resource-pack|g" index.html
    sed -i '' "s|src=\"../common-vendors|src=\"../$asset_folder/common-vendors|g" index.html
    sed -i '' "s|src=\"../common-fd|src=\"../$asset_folder/common-fd|g" index.html
    sed -i '' "s|src=\"../commerce-d3|src=\"../$asset_folder/commerce-d3|g" index.html
    sed -i '' "s|src=\"../user-account-core|src=\"../$asset_folder/user-account-core|g" index.html
    sed -i '' "s|src=\"../performance-c0|src=\"../$asset_folder/performance-c0|g" index.html
    
    # Fix CSS references
    sed -i '' "s|href=\"../commerce-2bd|href=\"../$asset_folder/commerce-2bd|g" index.html
    sed -i '' "s|href=\"../user-account-core|href=\"../$asset_folder/user-account-core|g" index.html
    
    cd ..
    echo "Fixed $page"
done

echo "All portfolio pages fixed!"
