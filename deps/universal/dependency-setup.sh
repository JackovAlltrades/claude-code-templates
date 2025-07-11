#!/bin/bash
# Universal dependency management setup script
# Detects project type and sets up appropriate dependency management

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Universal Dependency Management Setup${NC}"
echo "====================================="

# Detect project type
detect_project_type() {
    if [ -f "package.json" ]; then
        echo "node"
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "python"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Gemfile" ]; then
        echo "ruby"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "java"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)
echo -e "Detected project type: ${GREEN}$PROJECT_TYPE${NC}"

# Create common directories
mkdir -p scripts .github/workflows

# Setup based on project type
case $PROJECT_TYPE in
    "python")
        echo -e "${YELLOW}Setting up Python dependency management...${NC}"
        
        # Copy Python-specific scripts
        cp ~/.claude-templates/deps/python/* ./scripts/ 2>/dev/null || true
        
        # Create requirements-dev.txt if it doesn't exist
        if [ ! -f "requirements-dev.txt" ]; then
            cp ~/.claude-templates/deps/python/requirements-dev.txt . 2>/dev/null || \
            echo "# Development dependencies" > requirements-dev.txt
        fi
        
        # Add Python-specific ignores
        echo -e "\n# Dependency management" >> .gitignore
        echo ".dependency-backups/" >> .gitignore
        echo ".test-update-env/" >> .gitignore
        ;;
        
    "node")
        echo -e "${YELLOW}Setting up Node.js dependency management...${NC}"
        
        # Create Node update checker
        cat > scripts/check-npm-updates.js << 'EOF'
#!/usr/bin/env node
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function checkUpdates() {
    console.log('🔍 Checking for outdated npm packages...\n');
    
    try {
        const { stdout } = await execPromise('npm outdated --json');
        const outdated = JSON.parse(stdout || '{}');
        
        const updates = { high: [], medium: [], low: [] };
        
        for (const [pkg, info] of Object.entries(outdated)) {
            const current = info.current;
            const wanted = info.wanted;
            const latest = info.latest;
            
            const risk = getMajorVersion(latest) > getMajorVersion(current) ? 'high' :
                         getMinorVersion(latest) > getMinorVersion(current) ? 'medium' : 'low';
            
            updates[risk].push({ pkg, current, wanted, latest });
        }
        
        // Display results
        if (updates.high.length) {
            console.log('🔴 HIGH RISK (Major updates):');
            updates.high.forEach(u => console.log(`  ${u.pkg}: ${u.current} → ${u.latest}`));
        }
        
        if (updates.medium.length) {
            console.log('\n🟡 MEDIUM RISK (Minor updates):');
            updates.medium.forEach(u => console.log(`  ${u.pkg}: ${u.current} → ${u.latest}`));
        }
        
        if (updates.low.length) {
            console.log('\n🟢 LOW RISK (Patch updates):');
            updates.low.forEach(u => console.log(`  ${u.pkg}: ${u.current} → ${u.latest}`));
        }
        
    } catch (error) {
        console.log('All packages up to date!');
    }
}

function getMajorVersion(version) {
    return parseInt(version.split('.')[0]);
}

function getMinorVersion(version) {
    return parseInt(version.split('.')[1]);
}

checkUpdates();
EOF
        chmod +x scripts/check-npm-updates.js
        ;;
        
    "go")
        echo -e "${YELLOW}Setting up Go dependency management...${NC}"
        
        cat > scripts/check-go-updates.sh << 'EOF'
#!/bin/bash
echo "🔍 Checking for outdated Go modules..."
go list -u -m all
EOF
        chmod +x scripts/check-go-updates.sh
        ;;
        
    *)
        echo -e "${YELLOW}Project type not detected or not supported yet.${NC}"
        echo "You can still use the universal templates as a starting point."
        ;;
esac

# Create universal GitHub Actions workflow
cat > .github/workflows/dependency-review.yml << 'EOF'
name: Dependency Review

on: [pull_request]

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
          deny-licenses: GPL-3.0, AGPL-3.0
EOF

# Create dependabot config
if [ ! -f ".github/dependabot.yml" ]; then
    cp ~/workspace/.claude-templates/deps/universal/dependabot-template.yml .github/dependabot.yml 2>/dev/null || \
    echo "version: 2" > .github/dependabot.yml
fi

echo -e "\n${GREEN}✅ Dependency management setup complete!${NC}"
echo -e "\nNext steps:"
echo "1. Review and customize the scripts in ./scripts/"
echo "2. Configure .github/dependabot.yml for your needs"
echo "3. Run './scripts/check-*-updates.*' to see outdated dependencies"
echo "4. Commit these changes to version control"