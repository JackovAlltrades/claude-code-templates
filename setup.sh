#!/bin/bash
# Claude Templates Setup Script
# Installs and configures the complete lean development system

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Claude Templates Setup${NC}"
echo "======================="

# Check if running in WSL or Linux
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    echo -e "${GREEN}✓ Running in WSL${NC}"
    PLATFORM="wsl"
else
    echo -e "${GREEN}✓ Running in Linux${NC}"
    PLATFORM="linux"
fi

# Create directories
echo -e "\n${YELLOW}Creating template directories...${NC}"
mkdir -p ~/.claude-templates/scripts
mkdir -p ~/.config/port-manager

# Copy templates
echo -e "${YELLOW}Installing templates...${NC}"
TEMPLATE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Core files
cp -v "$TEMPLATE_DIR/README.md" ~/.claude-templates/
cp -v "$TEMPLATE_DIR/CLAUDE.md" ~/.claude-templates/
cp -v "$TEMPLATE_DIR/PORT_MANAGEMENT_TRUTH.md" ~/.claude-templates/
cp -v "$TEMPLATE_DIR/PORT_MANAGER.md" ~/.claude-templates/
cp -v "$TEMPLATE_DIR/CLAUDE_PORT_ADDON.md" ~/.claude-templates/

# Scripts
cp -v "$TEMPLATE_DIR/scripts/port-manager.py" ~/.claude-templates/scripts/
chmod +x ~/.claude-templates/scripts/port-manager.py

# Templates
cp -v "$TEMPLATE_DIR/Makefile.template" ~/.claude-templates/
cp -v "$TEMPLATE_DIR/.gitignore.template" ~/.claude-templates/
cp -v "$TEMPLATE_DIR/openapi-lean.yaml" ~/.claude-templates/ 2>/dev/null || true
cp -v "$TEMPLATE_DIR/lean-api-init.sh" ~/.claude-templates/ 2>/dev/null || true
chmod +x ~/.claude-templates/lean-api-init.sh 2>/dev/null || true

# Install Python dependencies
echo -e "\n${YELLOW}Checking Python dependencies...${NC}"
if ! python3 -c "import click" 2>/dev/null; then
    echo "Installing click..."
    pip3 install --user click
fi

# Create sample project to test
echo -e "\n${YELLOW}Testing port manager...${NC}"
cd /tmp
rm -rf test-port-manager
mkdir test-port-manager
cd test-port-manager

# Initialize ports
python3 ~/.claude-templates/scripts/port-manager.py init . > /dev/null

if [ -f .ports.env ]; then
    echo -e "${GREEN}✓ Port manager working correctly${NC}"
    cat .ports.env
else
    echo -e "${RED}✗ Port manager test failed${NC}"
    exit 1
fi

# Cleanup
cd ..
rm -rf test-port-manager

# Add to shell profile
echo -e "\n${YELLOW}Adding to shell profile...${NC}"
SHELL_PROFILE=""
if [ -f ~/.bashrc ]; then
    SHELL_PROFILE=~/.bashrc
elif [ -f ~/.zshrc ]; then
    SHELL_PROFILE=~/.zshrc
fi

if [ -n "$SHELL_PROFILE" ]; then
    # Check if already added
    if ! grep -q "claude-templates" "$SHELL_PROFILE"; then
        echo "" >> "$SHELL_PROFILE"
        echo "# Claude Templates" >> "$SHELL_PROFILE"
        echo "alias port-manager='python3 ~/.claude-templates/scripts/port-manager.py'" >> "$SHELL_PROFILE"
        echo "alias init-ports='python3 ~/.claude-templates/scripts/port-manager.py init .'" >> "$SHELL_PROFILE"
        echo "alias check-ports='python3 ~/.claude-templates/scripts/port-manager.py status'" >> "$SHELL_PROFILE"
        echo -e "${GREEN}✓ Added aliases to $SHELL_PROFILE${NC}"
    else
        echo -e "${GREEN}✓ Aliases already in $SHELL_PROFILE${NC}"
    fi
fi

# Configure git for proper line endings
echo -e "\n${YELLOW}Configuring git for LF line endings...${NC}"
git config --global core.autocrlf input
git config --global core.eol lf
echo -e "${GREEN}✓ Git configured for LF endings${NC}"

# Fix any existing line ending issues
if [ -f "$TEMPLATE_DIR/scripts/fix-line-endings.sh" ]; then
    echo -e "${YELLOW}Installing line ending fix script...${NC}"
    cp -v "$TEMPLATE_DIR/scripts/fix-line-endings.sh" ~/.claude-templates/scripts/
    chmod +x ~/.claude-templates/scripts/fix-line-endings.sh
    
    # Add alias for easy access
    if [ -n "$SHELL_PROFILE" ] && ! grep -q "fix-line-endings" "$SHELL_PROFILE"; then
        echo "alias fix-line-endings='bash ~/.claude-templates/scripts/fix-line-endings.sh'" >> "$SHELL_PROFILE"
    fi
fi

# Copy .gitattributes template
if [ -f "$TEMPLATE_DIR/.gitattributes" ]; then
    echo -e "${YELLOW}Installing .gitattributes template...${NC}"
    cp -v "$TEMPLATE_DIR/.gitattributes" ~/.claude-templates/
    echo -e "${GREEN}✓ Line ending configuration installed${NC}"
fi

# Summary
echo -e "\n${GREEN}✅ Installation Complete!${NC}"
echo -e "\n${BLUE}Quick Start:${NC}"
echo "1. Go to any project: cd ~/my-project"
echo "2. Initialize ports: init-ports"
echo "3. Check status: check-ports"
echo ""
echo -e "${BLUE}Available Commands:${NC}"
echo "  port-manager status     - Show all ports"
echo "  port-manager init .     - Initialize project"
echo "  port-manager free 8080  - Free a port"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  Main README: ~/.claude-templates/README.md"
echo "  Port Guide: ~/.claude-templates/PORT_MANAGEMENT_TRUTH.md"
echo ""
echo -e "${YELLOW}Reload your shell or run: source $SHELL_PROFILE${NC}"