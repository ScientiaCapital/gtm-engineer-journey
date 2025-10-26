#!/bin/bash
# Deploy GTM Portfolio to GitHub Pages

echo "🚀 Deploying GTM Engineer Portfolio to GitHub Pages..."

# Ensure we're in the right directory
cd /Users/tmkipper/Desktop/tk_projects/gtm-engineer-journey

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git remote add origin https://github.com/ScientiaCapital/gtm-engineer-journey.git
fi

# Add all files
echo "📝 Staging changes..."
git add .

# Commit
echo "💾 Committing..."
git commit -m "Update GTM portfolio with dealer-scraper-mvp and enhanced GitHub Pages"

# Push to main branch
echo "🌐 Pushing to GitHub..."
git push -u origin main

# Enable GitHub Pages (manual step required)
echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "⚠️  IMPORTANT: Enable GitHub Pages manually:"
echo "1. Go to: https://github.com/ScientiaCapital/gtm-engineer-journey/settings/pages"
echo "2. Source: Deploy from branch"
echo "3. Branch: main"
echo "4. Folder: /docs"
echo "5. Click Save"
echo ""
echo "🌐 Your portfolio will be live at:"
echo "   https://scientiacapital.github.io/gtm-engineer-journey"
echo ""
echo "📊 Live tools showcased:"
echo "   ✅ Dealer Scraper MVP (Tesla data)"
echo "   ✅ Candlestick Screener" 
echo "   ✅ Market Basket Analysis API"
echo "   + 40+ other projects"