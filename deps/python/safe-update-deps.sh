#!/bin/bash
# Safe dependency update script with rollback capability

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Universal Scaffolder Safe Dependency Updater${NC}"
echo "============================================="

# Create backup of current requirements
BACKUP_DIR=".dependency-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

echo -e "${YELLOW}Creating backup of current dependencies...${NC}"
cp requirements.txt "$BACKUP_DIR/requirements_${TIMESTAMP}.txt"
cp requirements-dev.txt "$BACKUP_DIR/requirements-dev_${TIMESTAMP}.txt" 2>/dev/null || true

# Create virtual environment for testing
TEST_ENV=".test-update-env"
echo -e "${YELLOW}Creating test environment...${NC}"
python -m venv $TEST_ENV
source $TEST_ENV/bin/activate

# Install current dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt 2>/dev/null || true

# Function to test updates
test_update() {
    local package=$1
    local version=$2
    
    echo -e "${YELLOW}Testing update: $package to $version${NC}"
    
    # Try to install the update
    if pip install "$package==$version"; then
        # Run basic import test
        if python -c "import $package" 2>/dev/null; then
            echo -e "${GREEN}✓ Import test passed${NC}"
            
            # Run unit tests
            if pytest tests/unit/ -v --maxfail=1 -x; then
                echo -e "${GREEN}✓ Unit tests passed${NC}"
                return 0
            else
                echo -e "${RED}✗ Unit tests failed${NC}"
                return 1
            fi
        else
            echo -e "${RED}✗ Import test failed${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Installation failed${NC}"
        return 1
    fi
}

# Get list of outdated packages
echo -e "${YELLOW}Checking for outdated packages...${NC}"
python scripts/check-dependency-updates.py

# Ask for confirmation
echo -e "\n${YELLOW}Do you want to proceed with safe updates? (y/n)${NC}"
read -r response

if [[ "$response" != "y" ]]; then
    echo "Update cancelled"
    deactivate
    rm -rf $TEST_ENV
    exit 0
fi

# Update low-risk packages first
echo -e "\n${GREEN}Updating low-risk packages...${NC}"
pip list --outdated --format=json | python -c "
import json, sys
data = json.load(sys.stdin)
for pkg in data:
    current = pkg['version']
    latest = pkg['latest_version']
    if current.split('.')[0] == latest.split('.')[0]:  # Same major version
        print(f\"{pkg['name']}=={latest}\")
" | while read pkg_spec; do
    package=$(echo $pkg_spec | cut -d'=' -f1)
    version=$(echo $pkg_spec | cut -d'=' -f3)
    
    if test_update "$package" "$version"; then
        echo "$pkg_spec" >> successful_updates.txt
    else
        echo "$pkg_spec" >> failed_updates.txt
    fi
done

# Generate update summary
echo -e "\n${GREEN}Update Summary${NC}"
echo "================="

if [ -f successful_updates.txt ]; then
    echo -e "${GREEN}Successfully updated:${NC}"
    cat successful_updates.txt
    
    # Apply successful updates to main environment
    deactivate
    echo -e "\n${YELLOW}Applying updates to main environment...${NC}"
    cat successful_updates.txt | xargs pip install
fi

if [ -f failed_updates.txt ]; then
    echo -e "\n${RED}Failed updates (manual review needed):${NC}"
    cat failed_updates.txt
fi

# Cleanup
rm -rf $TEST_ENV
rm -f successful_updates.txt failed_updates.txt

echo -e "\n${GREEN}Update process completed!${NC}"
echo -e "Backup saved to: $BACKUP_DIR/requirements_${TIMESTAMP}.txt"
echo -e "\nTo rollback if needed:"
echo -e "  cp $BACKUP_DIR/requirements_${TIMESTAMP}.txt requirements.txt"
echo -e "  pip install -r requirements.txt --force-reinstall"