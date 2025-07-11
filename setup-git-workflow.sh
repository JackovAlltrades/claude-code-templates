#!/bin/bash
# Setup Git workflow for Claude Templates repository

set -e

echo "🔧 Setting up Git workflow for Claude Templates"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository!${NC}"
    echo "Please run this from the .claude-templates directory"
    exit 1
fi

# Function to create branch if it doesn't exist
create_branch() {
    local branch=$1
    local from_branch=${2:-main}
    
    if ! git show-ref --verify --quiet refs/heads/$branch; then
        echo -e "${GREEN}Creating branch: $branch${NC}"
        git checkout -b $branch $from_branch
        git push -u origin $branch
    else
        echo -e "${YELLOW}Branch already exists: $branch${NC}"
    fi
}

# 1. Create directory structure
echo -e "\n${GREEN}📁 Creating directory structure...${NC}"
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p claude-system/{base/{languages,security},tests}
mkdir -p scripts
mkdir -p tests/sample-project/.claude-{company,project}

# 2. Create .gitignore
echo -e "\n${GREEN}📝 Creating .gitignore...${NC}"
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.pytest_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
.cache/
logs/
backups/
*.log
.env
.env.*

# Testing
tests/sample-project/CLAUDE.md
tests/output/
EOF

# 3. Create requirements.txt
echo -e "\n${GREEN}📦 Creating requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
# Core dependencies
PyYAML>=6.0
gitpython>=3.1.0
click>=8.1.0
pydantic>=2.0.0

# Development dependencies
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
yamllint>=1.33.0

# Security scanning
safety>=2.3.0
bandit>=1.7.0
EOF

# 4. Create PR template
echo -e "\n${GREEN}📋 Creating PR template...${NC}"
cat > .github/pull_request_template.md << 'EOF'
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change)
- [ ] ✨ New feature (non-breaking change)
- [ ] 💔 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Configuration change
- [ ] ♻️ Code refactoring

## Testing
- [ ] Tested merger.py with sample configs
- [ ] Validated generated CLAUDE.md
- [ ] Checked backwards compatibility
- [ ] All tests pass locally

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass

## Impact Analysis
<!-- Answer these questions -->
- Which templates are affected?
- Will this require updates to existing projects?
- Are there any breaking changes?
- Migration steps needed?

## Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## Related Issues
<!-- Link any related issues here -->
Closes #
EOF

# 5. Create issue templates
echo -e "\n${GREEN}🐛 Creating issue templates...${NC}"
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With config '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.11]
- Claude Templates version: [e.g. 1.2.0]

**Additional context**
Add any other context about the problem here.
EOF

cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest an idea for Claude Templates
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've considered.

**Additional context**
Add any other context or screenshots.
EOF

# 6. Create CI workflow
echo -e "\n${GREEN}🚀 Creating CI workflow...${NC}"
cat > .github/workflows/ci.yml << 'EOF'
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Lint with flake8
        run: flake8 claude-system/ --max-line-length=100
        
      - name: Format check with black
        run: black --check claude-system/
        
      - name: Type check with mypy
        run: mypy claude-system/ --ignore-missing-imports
        
      - name: Run tests
        run: pytest tests/ -v --cov=claude-system --cov-report=xml
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        
      - name: Validate YAML configs
        run: yamllint -d relaxed claude-system/**/*.yaml || true
        
      - name: Security scan with bandit
        run: bandit -r claude-system/ -f json -o bandit-report.json || true

  test-merge:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
          
      - name: Test merger script
        run: |
          python claude-system/merger.py --project tests/sample-project --debug
          
      - name: Validate output
        run: |
          test -f tests/sample-project/CLAUDE.md
          grep -q "auto-generated" tests/sample-project/CLAUDE.md
EOF

# 7. Create CHANGELOG.md
echo -e "\n${GREEN}📄 Creating CHANGELOG.md...${NC}"
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to Claude Templates will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Tiered template system (universal, company, project)
- Language-specific mistake-proofing guide
- Git workflow documentation
- Auto-update capability
- Role-based templates

### Changed
- Enhanced Python virtual environment detection
- Improved merge conflict resolution

### Fixed
- Docker multi-stage build examples

## [1.0.0] - 2024-01-07

### Added
- Initial release
- Core templates
- Basic documentation
EOF

# 8. Create git hooks
echo -e "\n${GREEN}🔗 Setting up git hooks...${NC}"
mkdir -p .git/hooks

# Pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook for Claude Templates

# Check Python formatting
if command -v black &> /dev/null; then
    echo "Running black..."
    black --check claude-system/ || {
        echo "❌ Black formatting check failed. Run 'black claude-system/' to fix."
        exit 1
    }
fi

# Check for secrets
echo "Checking for secrets..."
if git diff --staged --name-only | xargs grep -l -E "(password|secret|key|token).*=.*['\"]" 2>/dev/null; then
    echo "❌ Potential hardcoded secrets detected!"
    echo "Please review your changes."
    exit 1
fi

# Validate YAML
if command -v yamllint &> /dev/null; then
    echo "Validating YAML files..."
    git diff --staged --name-only --diff-filter=ACM | grep "\.ya?ml$" | xargs yamllint -d relaxed || {
        echo "⚠️  YAML validation warnings (non-blocking)"
    }
fi

echo "✅ Pre-commit checks passed"
EOF

chmod +x .git/hooks/pre-commit

# Commit-msg hook
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Enforce conventional commits

commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .+'
commit_msg=$(cat "$1")

if ! echo "$commit_msg" | grep -qE "$commit_regex"; then
    echo "❌ Invalid commit message format!"
    echo ""
    echo "Format: <type>(<scope>): <subject>"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, perf, test, chore"
    echo ""
    echo "Example: feat(python): add async patterns"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg

# 9. Create branches
echo -e "\n${GREEN}🌳 Setting up Git branches...${NC}"

# Ensure we're on main
git checkout main 2>/dev/null || git checkout -b main

# Create develop branch
create_branch develop main

# Switch back to main
git checkout main

# 10. Create initial test structure
echo -e "\n${GREEN}🧪 Creating test structure...${NC}"
cat > tests/test_merger.py << 'EOF'
"""Tests for the Claude merger system"""
import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from claude_system.merger import ClaudeMerger, Section

def test_section_creation():
    """Test Section dataclass creation"""
    section = Section(
        title="Test Section",
        content="Test content",
        level=2,
        source="universal"
    )
    assert section.title == "Test Section"
    assert section.checksum != ""

def test_merger_initialization():
    """Test ClaudeMerger initialization"""
    merger = ClaudeMerger("tests/sample-project")
    assert merger is not None
    assert merger.project_path.exists()

# Add more tests...
EOF

# 11. Final setup
echo -e "\n${GREEN}🎉 Git workflow setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review and commit the generated files"
echo "2. Push branches to remote: git push --all"
echo "3. Set up branch protection rules on GitHub"
echo "4. Configure secrets for CI/CD"
echo ""
echo "Recommended commit:"
echo "  git add ."
echo '  git commit -m "chore: implement Git workflow and project structure"'
echo ""
echo "To start developing:"
echo "  git checkout develop"
echo "  git checkout -b feature/your-feature"
EOF

chmod +x setup-git-workflow.sh