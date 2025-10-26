#!/bin/bash
# Move dealer-scraper-mvp to GTM Engineer Journey

echo "🚀 Migrating dealer-scraper-mvp to GTM Engineer Journey..."

# Source and destination paths
SOURCE="/Users/tmkipper/Desktop/dealer-scraper-mvp"
DEST="/Users/tmkipper/Desktop/tk_projects/gtm-engineer-journey/projects/dealer-scraper-mvp"

# Check if source exists
if [ ! -d "$SOURCE" ]; then
    echo "❌ Source directory not found: $SOURCE"
    echo "Please ensure dealer-scraper-mvp exists on your Desktop"
    exit 1
fi

# Copy files
echo "📦 Copying files..."
cp -r "$SOURCE"/* "$DEST/" 2>/dev/null || {
    echo "⚠️  Some files couldn't be copied. You may need to manually copy from:"
    echo "   $SOURCE"
    echo "   to: $DEST"
}

# Create README if it doesn't exist
if [ ! -f "$DEST/README.md" ]; then
    echo "📝 Creating README..."
    cat > "$DEST/README.md" << 'EOF'
# Dealer Scraper MVP

Production web scraping tool for OEM dealer networks.

## Features
- Tesla installer data extraction (live)
- CSV export capabilities
- Rate limiting & error handling
- Duplicate detection
- Progress tracking

## Quick Start
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scraper.py
```

## Output
Results are saved to `data/dealers_YYYY-MM-DD.csv`

## Status
✅ Production - Processing Tesla installers
EOF
fi

echo "✅ Migration complete!"
echo ""
echo "Next steps:"
echo "1. cd /Users/tmkipper/Desktop/tk_projects/gtm-engineer-journey"
echo "2. git add projects/dealer-scraper-mvp"
echo "3. git commit -m 'Add dealer-scraper-mvp to GTM portfolio'"
echo "4. git push origin main"