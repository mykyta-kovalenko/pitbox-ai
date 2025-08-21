#!/bin/bash
# Watch Python files and run ruff on changes

echo "🔍 Watching Python files for changes..."
echo "Will run ruff check + format on file modifications"
echo "Press Ctrl+C to stop"

# Check if fswatch is available (install with: brew install fswatch)
if ! command -v fswatch &> /dev/null; then
    echo "❌ fswatch not found. Install with: brew install fswatch"
    exit 1
fi

# Watch all Python files in the project
fswatch -r --event Updated --include=".*\.py$" . | while read file
do
    if [[ $file == *.py ]]; then
        echo "📝 File changed: $file"
        echo "🔧 Running ruff check + format..."
        
        uv run ruff check "$file" --fix
        uv run ruff format "$file"
        
        echo "✅ Quality check complete"
        echo "---"
    fi
done