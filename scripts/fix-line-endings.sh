#!/bin/bash
# Comprehensive line ending fix script
# Fixes CRLF -> LF for all text files in the project

echo "🔧 Fixing line endings for all text files..."

# Define file extensions to check
TEXT_EXTENSIONS=(
    "*.py"
    "*.sh"
    "*.md"
    "*.yml"
    "*.yaml"
    "*.json"
    "*.txt"
    "*.mk"
    "*.sql"
    "*.js"
    "*.ts"
    "*.jsx"
    "*.tsx"
    "*.css"
    "*.scss"
    "*.html"
    "*.xml"
    "*.go"
    "*.rs"
    "*.toml"
    "*.env"
    "*.gitignore"
    "Makefile"
    "Dockerfile"
    ".dockerignore"
)

# Counter for fixed files
FIXED_COUNT=0

# Function to fix line endings in a file
fix_file() {
    local file=$1
    if [ -f "$file" ]; then
        # Check if file has CRLF endings
        if file "$file" 2>/dev/null | grep -q "CRLF" || od -c "$file" 2>/dev/null | grep -q '\r'; then
            echo "  Fixing: $file"
            # Convert CRLF to LF
            sed -i 's/\r$//' "$file" 2>/dev/null || sed -i '' 's/\r$//' "$file" 2>/dev/null
            ((FIXED_COUNT++))
        fi
    fi
}

# Process each file type
for pattern in "${TEXT_EXTENSIONS[@]}"; do
    # Use find to get all matching files, excluding common binary directories
    find . -type f -name "$pattern" \
        -not -path "*/\.git/*" \
        -not -path "*/node_modules/*" \
        -not -path "*/venv/*" \
        -not -path "*/__pycache__/*" \
        -not -path "*/\.venv/*" \
        -not -path "*/dist/*" \
        -not -path "*/build/*" \
        -not -path "*/target/*" \
        -not -path "*/vendor/*" \
        -not -path "*/\.mcp-venv/*" \
        -print0 | while IFS= read -r -d '' file; do
        fix_file "$file"
    done
done

# Also fix files without extensions that might be text files
find . -type f \
    -not -path "*/\.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/venv/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/\.venv/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    -not -path "*/target/*" \
    -not -path "*/vendor/*" \
    -not -path "*/\.mcp-venv/*" \
    ! -name "*.*" \
    -print0 | while IFS= read -r -d '' file; do
    # Check if it's a text file
    if file "$file" 2>/dev/null | grep -q "text"; then
        fix_file "$file"
    fi
done

echo "✅ Fixed line endings in $FIXED_COUNT files"

# Update git config to handle line endings properly
echo "🔧 Updating git configuration..."
git config core.autocrlf input
git config core.eol lf

echo "✅ Git configured to use LF line endings"