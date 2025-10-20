#!/bin/bash

# OUNASS API - GitHub Push Script
# This script will push all project files to the GitHub repository

echo "================================================"
echo "OUNASS Kubernetes Pod Forecasting API"
echo "GitHub Push Script"
echo "================================================"
echo ""

# Change to project directory
cd /Users/root1/Desktop/Projects/ounass-api || exit 1

echo "✅ Changed to project directory"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi
echo ""

# Add remote if not exists
if ! git remote | grep -q "origin"; then
    echo "Adding GitHub remote..."
    git remote add origin https://github.com/sorted78/ounass-api.git
    echo "✅ Remote added"
else
    echo "✅ Remote already exists"
fi
echo ""

# Fetch latest from GitHub
echo "Fetching latest changes from GitHub..."
git fetch origin main
echo "✅ Fetched latest changes"
echo ""

# Try to merge
echo "Merging with remote main branch..."
git merge origin/main --allow-unrelated-histories || echo "Note: Merge had some conflicts or is not needed"
echo ""

# Show status
echo "Current git status:"
git status
echo ""

# Add all files
echo "Adding all files to git..."
git add .
echo "✅ Files added"
echo ""

# Show what will be committed
echo "Files to be committed:"
git status --short
echo ""

# Ask for confirmation
read -p "Do you want to commit and push these files? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Commit
    echo "Committing files..."
    git commit -m "Add complete source code, documentation, tests, and sample data

- Add all source code files (src/api, src/models, src/services)
- Add comprehensive documentation (README, API_USAGE, GOOGLE_SHEETS_SETUP, DEPLOYMENT, QUICKSTART, PROJECT_SUMMARY)
- Add test suite (tests/test_api.py)
- Add sample data (data/sample_data.csv)
- Add changelog with detailed version history
- Complete project setup with all dependencies and configurations"
    
    echo "✅ Files committed"
    echo ""
    
    # Push to GitHub
    echo "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "================================================"
        echo "✅ SUCCESS! All files pushed to GitHub"
        echo "================================================"
        echo ""
        echo "Repository: https://github.com/sorted78/ounass-api"
        echo ""
        echo "Next steps:"
        echo "1. Visit the repository and verify all files are there"
        echo "2. Set up Google Sheets (see GOOGLE_SHEETS_SETUP.md)"
        echo "3. Configure .env file with your credentials"
        echo "4. Run: pip install -r requirements.txt"
        echo "5. Run: uvicorn src.main:app --reload"
        echo ""
    else
        echo ""
        echo "❌ Push failed. Please check the error message above."
        echo ""
        echo "Common issues:"
        echo "- Authentication: Make sure you're logged into GitHub"
        echo "- Permissions: Ensure you have write access to the repository"
        echo "- Network: Check your internet connection"
        echo ""
    fi
else
    echo ""
    echo "❌ Push cancelled. Files are committed locally but not pushed."
    echo "You can push later with: git push -u origin main"
    echo ""
fi
