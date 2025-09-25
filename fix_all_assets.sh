#!/bin/bash

# Fix asset paths for all project directories
cd "/Users/oren/Documents/MENDELOW LLC/mendelow-studio"

# Array mapping project directories to their asset directories
declare -A project_assets=(
    ["_pomander-walk_-artist-consultation"]="_Pomander Walk_ Artist Consultation — MENDELOW STUDIO_files"
    ["_pomander-walk_-by-oren"]="_Pomander Walk_ by Oren — MENDELOW STUDIO_files"
    ["5-panel-hat"]="5 panel hat — MENDELOW STUDIO_files"
    ["alto-_-app-design"]="Alto _ App Design — MENDELOW STUDIO_files"
    ["art"]="Art — MENDELOW STUDIO_files"
    ["art-gallery-proposal"]="Art Gallery Proposal — MENDELOW STUDIO_files"
    ["beanie"]="beanie — MENDELOW STUDIO_files"
    ["bench-swing"]="Bench Swing — MENDELOW STUDIO_files"
    ["butter-mounts"]="Butter Mounts — MENDELOW STUDIO_files"
    ["contact"]="Contact — MENDELOW STUDIO_files"
    ["custom-espresso-station"]="Custom Espresso Station — MENDELOW STUDIO_files"
    ["design-services"]="Design Services — MENDELOW STUDIO_files"
    ["digital-design"]="Digital Design — MENDELOW STUDIO_files"
    ["drawing"]="Drawing — MENDELOW STUDIO_files"
    ["fabrication"]="Fabrication — MENDELOW STUDIO_files"
    ["general-1"]="General 1 — MENDELOW STUDIO_files"
    ["handcrafted-birch-portafilter-dock"]="Handcrafted Birch Portafilter Dock — MENDELOW STUDIO_files"
    ["heritage"]="Heritage — MENDELOW STUDIO_files"
    ["homemade-vacuum-former"]="Homemade Vacuum Former — MENDELOW STUDIO_files"
    ["hoodie"]="hoodie — MENDELOW STUDIO_files"
    ["koala-boards"]="KOALA BOARDS — MENDELOW STUDIO_files"
    ["koala-boards-_-about"]="KOALA BOARDS _ About — MENDELOW STUDIO_files"
    ["koala-boards-_-board-backpack-bundle"]="KOALA BOARDS _ board + backpack bundle — MENDELOW STUDIO_files"
    ["media"]="Media — MENDELOW STUDIO_files"
    ["minibike-build"]="Minibike Build — MENDELOW STUDIO_files"
    ["no-mess-cutting-board-oiling-tool"]="No Mess Cutting Board Oiling Tool — MENDELOW STUDIO_files"
    ["oil-drum-fire-pit"]="Oil Drum Fire Pit — MENDELOW STUDIO_files"
    ["oren"]="Oren's Portfolio — MENDELOW STUDIO_files"
    ["orens-portfolio"]="Oren's Portfolio — MENDELOW STUDIO_files"
    ["pached-_-mobile-app-design"]="Pa+ched _ Mobile App Design — MENDELOW STUDIO_files"
    ["photography"]="Photography — MENDELOW STUDIO_files"
    ["poopalz"]="PooPalz — MENDELOW STUDIO_files"
    ["stop-motion"]="Stop Motion — MENDELOW STUDIO_files"
    ["szzl"]="SZZL — MENDELOW STUDIO_files"
    ["tee"]="tee — MENDELOW STUDIO_files"
    ["videography"]="Videography — MENDELOW STUDIO_files"
    ["wood-art"]="Wood Art — MENDELOW STUDIO_files"
    ["yurtle-_-branding-identity"]="Yurtle _ Branding & Identity — MENDELOW STUDIO_files"
    ["dad-hat"]="dad hat — MENDELOW STUDIO_files"
)

# Process each project directory
for project_dir in "${!project_assets[@]}"; do
    asset_dir="${project_assets[$project_dir]}"
    index_file="./$project_dir/index.html"
    
    if [[ -f "$index_file" ]]; then
        echo "Fixing assets in $project_dir -> $asset_dir"
        
        # Fix asset paths - replace any existing asset directory references with the correct one
        sed -i '' "s|src=\"[^\"]*_files/|src=\"../$asset_dir/|g" "$index_file"
        sed -i '' "s|href=\"[^\"]*_files/|href=\"../$asset_dir/|g" "$index_file"
        
        # Also fix specific patterns that might exist
        sed -i '' "s|src=\"[^\"]*MENDELOW STUDIO_files/|src=\"../$asset_dir/|g" "$index_file"
        sed -i '' "s|href=\"[^\"]*MENDELOW STUDIO_files/|href=\"../$asset_dir/|g" "$index_file"
    fi
done

echo "Asset path fixing complete!"
