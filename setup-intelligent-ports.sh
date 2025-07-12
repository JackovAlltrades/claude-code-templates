#!/bin/bash
# Intelligent Port Management Setup Script
# This script sets up the complete intelligent port management system

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧠 Intelligent Port Management Setup${NC}"
echo "===================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"

# Check if running in WSL
IS_WSL=false
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    IS_WSL=true
    echo -e "${YELLOW}📍 Detected WSL environment${NC}"
fi

# Step 1: Check Python
echo -e "\n${YELLOW}1. Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.7+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Step 2: Install Python dependencies
echo -e "\n${YELLOW}2. Installing Python dependencies...${NC}"
pip3 install --user click rich pyyaml > /dev/null 2>&1 || {
    echo -e "${YELLOW}⚠️  Failed to install with --user, trying without...${NC}"
    pip3 install click rich pyyaml
}
echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Step 3: Create necessary directories
echo -e "\n${YELLOW}3. Creating directories...${NC}"
mkdir -p ~/.local/bin
mkdir -p ~/.config/intelligent-port-manager
mkdir -p ~/.config/port-lifecycle
echo -e "${GREEN}✅ Directories created${NC}"

# Step 4: Copy intelligent port scripts
echo -e "\n${YELLOW}4. Installing intelligent port scripts...${NC}"

# Copy main scripts
cp "$SCRIPTS_DIR/intelligent-port-manager.py" ~/.local/bin/
cp "$SCRIPTS_DIR/port-lifecycle-manager.py" ~/.local/bin/
chmod +x ~/.local/bin/intelligent-port-manager.py
chmod +x ~/.local/bin/port-lifecycle-manager.py

# Copy supporting scripts to scripts directory
cp "$SCRIPTS_DIR/port-hooks.sh" ~/.local/bin/
cp "$SCRIPTS_DIR/port-makefile-template.mk" ~/.local/bin/

echo -e "${GREEN}✅ Scripts installed${NC}"

# Step 5: Initialize port registry
echo -e "\n${YELLOW}5. Initializing port registry...${NC}"
if [ ! -f ~/.config/intelligent-port-manager/port-registry.json ]; then
    cat > ~/.config/intelligent-port-manager/port-registry.json << EOF
{
  "ports": {},
  "services": {},
  "environments": {},
  "updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
    echo -e "${GREEN}✅ Port registry initialized${NC}"
else
    echo -e "${BLUE}ℹ️  Port registry already exists${NC}"
fi

# Step 6: Add to shell configuration
echo -e "\n${YELLOW}6. Configuring shell integration...${NC}"

# Determine shell config file
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    SHELL_CONFIG="$HOME/.bashrc"  # Default to bashrc
fi

# Check if already configured
if grep -q "Intelligent Port Management" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${BLUE}ℹ️  Shell already configured${NC}"
else
    echo -e "${YELLOW}Adding to $SHELL_CONFIG...${NC}"
    cat >> "$SHELL_CONFIG" << 'EOF'

# Intelligent Port Management System
export PATH="$HOME/.local/bin:$PATH"

# Load port hooks if available
if [ -f ~/.local/bin/port-hooks.sh ]; then
    source ~/.local/bin/port-hooks.sh
    export PORT_HOOKS_ENABLED=true
fi

# Convenient aliases
alias ipm='python3 ~/.local/bin/intelligent-port-manager.py'
alias plm='python3 ~/.local/bin/port-lifecycle-manager.py'
alias port-check='ipm status'
alias port-sync='ipm sync'
alias port-ranges='ipm ranges'

# Function to quickly allocate ports for a new project
quick-ports() {
    local project_name=${1:-$(basename "$PWD")}
    echo "🔍 Allocating ports for $project_name..."
    
    ipm allocate "$project_name-web" --type web --project "$project_name"
    ipm allocate "$project_name-api" --type api --project "$project_name"
    ipm allocate "$project_name-db" --type database --project "$project_name"
    ipm generate-env "$project_name"
    
    echo "✅ Ports allocated! Check .ports.development.env"
}

# Function to show port status with colors
port-dashboard() {
    echo "📊 Port Management Dashboard"
    echo "============================"
    ipm status
    echo ""
    echo "📈 Lifecycle Status"
    echo "==================="
    plm status
}
EOF
    echo -e "${GREEN}✅ Shell configuration updated${NC}"
fi

# Step 7: Fix line endings if on WSL
if [ "$IS_WSL" = true ]; then
    echo -e "\n${YELLOW}7. Fixing line endings for WSL...${NC}"
    dos2unix ~/.local/bin/*.py 2>/dev/null || true
    dos2unix ~/.local/bin/*.sh 2>/dev/null || true
    echo -e "${GREEN}✅ Line endings fixed${NC}"
fi

# Step 8: Create example project setup
echo -e "\n${YELLOW}8. Creating example setup script...${NC}"
cat > ~/.local/bin/setup-project-ports << 'EOF'
#!/bin/bash
# Quick setup script for new projects

PROJECT_NAME=${1:-$(basename "$PWD")}

echo "🚀 Setting up intelligent ports for $PROJECT_NAME"

# Create scripts directory
mkdir -p scripts

# Copy intelligent port manager
cp ~/.local/bin/intelligent-port-manager.py scripts/
cp ~/.local/bin/port-lifecycle-manager.py scripts/
cp ~/.local/bin/port-makefile-template.mk scripts/

# Make executable
chmod +x scripts/*.py

# Allocate ports
python3 scripts/intelligent-port-manager.py allocate "$PROJECT_NAME-web" --type web --project "$PROJECT_NAME"
python3 scripts/intelligent-port-manager.py allocate "$PROJECT_NAME-api" --type api --project "$PROJECT_NAME"
python3 scripts/intelligent-port-manager.py allocate "$PROJECT_NAME-db" --type database --project "$PROJECT_NAME"

# Generate environment file
python3 scripts/intelligent-port-manager.py generate-env "$PROJECT_NAME"

echo "✅ Intelligent port management configured!"
echo "📄 Check .ports.development.env for allocated ports"
EOF

chmod +x ~/.local/bin/setup-project-ports
echo -e "${GREEN}✅ Project setup script created${NC}"

# Step 9: Test installation
echo -e "\n${YELLOW}9. Testing installation...${NC}"

# Test intelligent port manager
if python3 ~/.local/bin/intelligent-port-manager.py --help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Intelligent port manager working${NC}"
else
    echo -e "${RED}❌ Intelligent port manager test failed${NC}"
fi

# Test lifecycle manager
if python3 ~/.local/bin/port-lifecycle-manager.py --help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Port lifecycle manager working${NC}"
else
    echo -e "${RED}❌ Port lifecycle manager test failed${NC}"
fi

# Step 10: Display summary
echo -e "\n${GREEN}🎉 Installation Complete!${NC}"
echo -e "${GREEN}========================${NC}"
echo ""
echo -e "${BLUE}Quick Start Commands:${NC}"
echo -e "  ${YELLOW}ipm allocate my-service --type api${NC}     # Allocate a port"
echo -e "  ${YELLOW}ipm status${NC}                             # Show all allocated ports"
echo -e "  ${YELLOW}ipm ranges${NC}                             # Show standard port ranges"
echo -e "  ${YELLOW}port-dashboard${NC}                         # Show full dashboard"
echo -e "  ${YELLOW}quick-ports${NC}                            # Allocate ports for current project"
echo -e "  ${YELLOW}setup-project-ports${NC}                    # Set up ports for a project"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "1. ${YELLOW}source $SHELL_CONFIG${NC} (or start a new terminal)"
echo -e "2. ${YELLOW}cd to your project${NC}"
echo -e "3. ${YELLOW}setup-project-ports${NC}"
echo ""
echo -e "${GREEN}Happy coding with intelligent port management! 🚀${NC}"

# Create a verification script
cat > ~/.local/bin/verify-intelligent-ports << 'EOF'
#!/bin/bash
echo "🔍 Verifying Intelligent Port Management Installation"
echo "===================================================="
echo ""

# Check if commands are available
echo -n "Checking ipm command... "
if command -v ipm &> /dev/null; then
    echo "✅"
else
    echo "❌"
fi

echo -n "Checking plm command... "
if command -v plm &> /dev/null; then
    echo "✅"
else
    echo "❌"
fi

echo -n "Checking port hooks... "
if [ -f ~/.local/bin/port-hooks.sh ]; then
    echo "✅"
else
    echo "❌"
fi

echo -n "Checking registry... "
if [ -f ~/.config/intelligent-port-manager/port-registry.json ]; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "Testing commands:"
ipm --version 2>/dev/null || echo "ipm: ❌ Not working"
plm --version 2>/dev/null || echo "plm: ❌ Not working"

echo ""
echo "✅ Verification complete!"
EOF

chmod +x ~/.local/bin/verify-intelligent-ports

echo -e "\n${YELLOW}To verify installation later, run:${NC} ${GREEN}verify-intelligent-ports${NC}"