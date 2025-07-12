#!/bin/bash
# Initialize a new project with Claude Templates best practices
# This ensures proper line endings and port management from the start

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="${1:-.}"
PROJECT_NAME=$(basename "$PROJECT_DIR")

echo -e "${BLUE}🚀 Initializing project: $PROJECT_NAME${NC}"
echo "=================================="

cd "$PROJECT_DIR"

# 1. Copy .gitattributes to ensure proper line endings
echo -e "\n${YELLOW}1. Setting up line ending configuration...${NC}"
if [ ! -f .gitattributes ]; then
    if [ -f ~/.claude-templates/.gitattributes ]; then
        cp ~/.claude-templates/.gitattributes .
        echo -e "${GREEN}✓ Created .gitattributes${NC}"
    else
        echo -e "${RED}⚠ .gitattributes template not found${NC}"
    fi
else
    echo -e "${BLUE}ℹ .gitattributes already exists${NC}"
fi

# 2. Configure local git settings
echo -e "\n${YELLOW}2. Configuring git...${NC}"
if [ -d .git ]; then
    git config core.autocrlf input
    git config core.eol lf
    echo -e "${GREEN}✓ Git configured for LF endings${NC}"
else
    echo -e "${YELLOW}⚠ Not a git repository - skipping git config${NC}"
fi

# 3. Fix any existing line ending issues
echo -e "\n${YELLOW}3. Fixing line endings...${NC}"
if [ -f ~/.claude-templates/scripts/fix-line-endings.sh ]; then
    bash ~/.claude-templates/scripts/fix-line-endings.sh
else
    echo -e "${YELLOW}⚠ Line ending fix script not found${NC}"
fi

# 4. Initialize port management
echo -e "\n${YELLOW}4. Setting up port management...${NC}"
if [ ! -f .ports.env ]; then
    if command -v port-manager &> /dev/null; then
        port-manager init .
        echo -e "${GREEN}✓ Port management initialized${NC}"
    elif [ -f ~/.claude-templates/scripts/port-manager.py ]; then
        python3 ~/.claude-templates/scripts/port-manager.py init .
        echo -e "${GREEN}✓ Port management initialized${NC}"
    else
        echo -e "${RED}⚠ Port manager not found${NC}"
    fi
else
    echo -e "${BLUE}ℹ .ports.env already exists${NC}"
fi

# 5. Copy intelligent port manager if requested
if [ "$2" = "--intelligent" ] || [ "$2" = "-i" ]; then
    echo -e "\n${YELLOW}5. Setting up intelligent port management...${NC}"
    
    mkdir -p scripts
    
    # Copy scripts
    for script in intelligent-port-manager.py port-lifecycle-manager.py port-hooks.sh; do
        if [ -f ~/.claude-templates/scripts/$script ]; then
            cp ~/.claude-templates/scripts/$script scripts/
            chmod +x scripts/$script
            echo -e "${GREEN}✓ Copied $script${NC}"
        fi
    done
    
    # Initialize intelligent ports
    if [ -f scripts/intelligent-port-manager.py ]; then
        python3 scripts/intelligent-port-manager.py allocate "$PROJECT_NAME-web" --type web --project "$PROJECT_NAME"
        python3 scripts/intelligent-port-manager.py allocate "$PROJECT_NAME-api" --type api --project "$PROJECT_NAME"
        python3 scripts/intelligent-port-manager.py generate-env "$PROJECT_NAME"
        echo -e "${GREEN}✓ Intelligent ports configured${NC}"
    fi
fi

# 6. Create/Update CLAUDE.md
echo -e "\n${YELLOW}6. Setting up CLAUDE.md...${NC}"
if [ ! -f CLAUDE.md ]; then
    if [ -f ~/.claude-templates/CLAUDE.md ]; then
        cp ~/.claude-templates/CLAUDE.md .
        # Update project name
        sed -i "s/Project Name/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || \
        sed -i '' "s/Project Name/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || true
        echo -e "${GREEN}✓ Created CLAUDE.md${NC}"
    fi
else
    echo -e "${BLUE}ℹ CLAUDE.md already exists${NC}"
fi

# 7. Create pre-commit hook for line endings
echo -e "\n${YELLOW}7. Setting up git hooks...${NC}"
if [ -d .git ]; then
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook to ensure LF line endings

echo "Pre-commit: Checking line endings..."

# Get all staged files
git diff --cached --name-only --diff-filter=ACM | while read file; do
    if [ -f "$file" ]; then
        # Check if it's a text file
        if file "$file" | grep -q "text"; then
            # Check for CRLF line endings
            if file "$file" | grep -q "CRLF"; then
                echo "Fixing line endings in $file..."
                sed -i 's/\r$//' "$file" 2>/dev/null || sed -i '' 's/\r$//' "$file"
                git add "$file"
            fi
        fi
    fi
done

echo "Pre-commit: Line ending check complete."
EOF
    chmod +x .git/hooks/pre-commit
    echo -e "${GREEN}✓ Created pre-commit hook${NC}"
fi

# 8. Summary
echo -e "\n${GREEN}✅ Project initialization complete!${NC}"
echo -e "\n${BLUE}Project Setup Summary:${NC}"
echo "  • Line endings: LF (Unix)"
echo "  • Git autocrlf: input"
echo "  • Port management: initialized"
if [ -f .git/hooks/pre-commit ]; then
    echo "  • Pre-commit hook: installed"
fi
if [ -f CLAUDE.md ]; then
    echo "  • CLAUDE.md: ready"
fi

# Show port configuration
if [ -f .ports.env ]; then
    echo -e "\n${BLUE}Port Configuration:${NC}"
    cat .ports.env | grep -E "^[A-Z_]+_PORT=" | while read line; do
        echo "  • $line"
    done
fi

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Review and customize CLAUDE.md"
echo "2. Add your project-specific configuration"
if [ "$2" != "--intelligent" ] && [ "$2" != "-i" ]; then
    echo "3. For intelligent port management, run: $0 . --intelligent"
fi

echo -e "\n${GREEN}Happy coding! 🚀${NC}"