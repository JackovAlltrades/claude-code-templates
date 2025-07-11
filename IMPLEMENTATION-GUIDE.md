# Claude Templates - Implementation Guide

A complete guide to implementing the 3-tiered Claude template system with proper Git workflow.

## 🎯 Overview

The Claude Templates system provides:
1. **Automatic updates** from universal best practices
2. **Company-wide standards** enforcement
3. **Project-specific customizations**
4. **Developer preferences** (optional)
5. **Git workflow protection** for safe collaboration

## 📋 Prerequisites

- Git 2.30+
- Python 3.9+
- GitHub account (for remote repository)
- Admin access (for branch protection setup)

## 🚀 Initial Setup

### Step 1: Initialize Repository

```bash
# Clone the templates repository
cd ~/.claude-templates

# Run the setup script
chmod +x setup-git-workflow.sh
./setup-git-workflow.sh

# Review generated files
git status

# Commit the initial structure
git add .
git commit -m "chore: implement Git workflow and tiered template system"
```

### Step 2: Configure Remote Repository

```bash
# If not already connected to remote
git remote add origin git@github.com:yourorg/claude-templates.git

# Push all branches
git push -u origin main
git push -u origin develop

# Push tags if any
git push --tags
```

### Step 3: GitHub Configuration

1. **Enable Branch Protection** (Settings → Branches)
   - Protect `main` and `develop`
   - Require PR reviews
   - Require status checks
   - Require up-to-date branches

2. **Set up Secrets** (Settings → Secrets)
   - `SNYK_TOKEN` - For security scanning
   - `CODECOV_TOKEN` - For coverage reports

3. **Configure Actions** (Settings → Actions)
   - Enable GitHub Actions
   - Set up required permissions

## 🏢 Company Setup (Senior Dev Team)

### Step 1: Create Company Standards

```bash
# Create a new branch
git checkout develop
git pull origin develop
git checkout -b feature/company-standards

# Create company directory in your company repo
mkdir -p your-company-repo/.claude-company
cd your-company-repo/.claude-company

# Create company configuration
cat > config.yaml << 'EOF'
company: YourCompany
version: 1.0.0

policies:
  code_review:
    required: true
    min_approvers: 2
    
  security:
    secret_scanning: mandatory
    vulnerability_checks: blocking
    
  testing:
    coverage_minimum: 85
    required_types: [unit, integration, e2e]

roles:
  frontend:
    languages: [typescript, javascript]
    frameworks: [react, vue]
    exclude: ["backend", "database"]
    
  backend:
    languages: [python, go]
    frameworks: [fastapi, gin]
    exclude: ["frontend", "css"]
    
  fullstack:
    include_all: true
    
  devops:
    focus: ["kubernetes", "terraform", "ci-cd"]
    languages: [python, go, bash]
EOF

# Create company standards
cat > standards.md << 'EOF'
## YourCompany Engineering Standards

### Code Quality
- All code must pass linting (score > 9.5/10)
- Type hints required for Python
- Strict TypeScript mode enabled

### Security Requirements
- No hardcoded secrets (enforced by pre-commit)
- Dependencies scanned weekly
- OWASP Top 10 compliance

### Testing Standards
- TDD for new features
- Minimum 85% coverage
- Integration tests for all APIs
EOF

# Commit and push
git add .
git commit -m "feat(company): add company standards and policies"
git push -u origin feature/company-standards

# Create PR
gh pr create --title "Add company standards" --body "Implements company-wide policies and role templates"
```

### Step 2: Set Up Inheritance Chain

```bash
# In the claude-templates repo
cd ~/.claude-templates

# Update system config to recognize company layer
cat >> claude-system/config.yaml << 'EOF'

# Company layer configuration
company:
  enabled: true
  source:
    type: git
    repo: git@github.com:yourcompany/company-standards.git
    path: .claude-company
  
  # Override rules
  override_policy:
    security: forbidden  # Cannot override security policies
    testing: conditional # Can reduce by max 10%
    general: allowed    # Can override other sections
EOF
```

## 💻 Project Setup (Team/Project Lead)

### Step 1: Initialize Project Configuration

```bash
# In your project repository
cd ~/projects/awesome-api

# Create project configuration
mkdir -p .claude-project
cd .claude-project

# Create project config
cat > config.yaml << 'EOF'
project: awesome-api
team: platform
version: 1.0.0

# Technology stack
stack:
  primary_language: python
  framework: fastapi
  databases: [postgresql, redis]
  
# Services in this project
services:
  - name: api
    type: backend
    language: python
    
  - name: worker
    type: background
    language: python
    
  - name: frontend
    type: web
    language: typescript

# Developer customization
developer_overrides:
  enabled: true
  approval_required: false
  max_sections: 5
EOF

# Create project-specific overrides
cat > overrides.md << 'EOF'
## Project-Specific Guidelines

### Local Development Setup
1. Use Docker Compose: `docker-compose up -d`
2. Python venv at `./venv`
3. Node modules via pnpm

### API Conventions
- RESTful endpoints under `/api/v1/`
- GraphQL endpoint at `/graphql`
- WebSocket at `/ws`

### Testing Strategy
- Unit tests: pytest with fixtures
- API tests: pytest + httpx
- E2E tests: Playwright
EOF

# Generate initial CLAUDE.md
~/.claude-templates/claude-system/merger.py

# Commit
git add .
git commit -m "chore: add Claude project configuration"
```

### Step 2: Add to CI/CD

```yaml
# .github/workflows/update-claude.yml
name: Update CLAUDE.md

on:
  schedule:
    - cron: '0 0 * * MON'  # Weekly on Monday
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install Claude system
        run: |
          git clone https://github.com/yourorg/claude-templates.git /tmp/claude
          pip install -r /tmp/claude/requirements.txt
          
      - name: Update templates
        run: |
          python /tmp/claude/claude-system/merger.py --project .
          
      - name: Create PR if changed
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'chore: update CLAUDE.md from templates'
          body: 'Automated update from universal templates'
          branch: update-claude-templates
```

## 👤 Developer Setup (Individual)

### Step 1: Personal Preferences

```bash
# In project repository
cd .claude-project/developer

# Create your preferences
cat > $USER.md << 'EOF'
## Personal Development Preferences

### Editor Config
- VS Code with Python extension
- Black formatter on save
- Pylint enabled

### Local Shortcuts
```bash
alias dev="docker-compose up -d && code ."
alias test="pytest -xvs"
alias lint="black . && flake8"
```

### Debugging Setup
- Python: debugpy on port 5678
- Node: --inspect on port 9229
EOF

# Regenerate CLAUDE.md with your preferences
~/.claude-templates/claude-system/merger.py --username $USER
```

## 🔄 Daily Workflow

### For Template Maintainers

```bash
# 1. Always start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/add-rust-patterns

# 3. Make changes
vim claude-system/base/languages/rust.md

# 4. Test changes
pytest tests/

# 5. Commit with conventional message
git add .
git commit -m "feat(rust): add error handling patterns"

# 6. Push and create PR
git push -u origin feature/add-rust-patterns
gh pr create

# 7. After review and merge
git checkout develop
git pull origin develop
git branch -d feature/add-rust-patterns
```

### For Project Teams

```bash
# Check for updates
claude-manage update

# Review changes
claude-manage diff

# Apply updates
claude-manage merge

# Commit if changed
git add CLAUDE.md
git commit -m "chore: update CLAUDE.md from templates"
```

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Check system status
claude-manage status

# Validate current setup
claude-manage validate

# Show inheritance chain
claude-manage show-inheritance

# Check for conflicts
claude-manage check-conflicts
```

### Regular Maintenance

1. **Weekly**: Review and merge template updates
2. **Monthly**: Update company policies if needed
3. **Quarterly**: Review role definitions
4. **Yearly**: Major version review

## 🚨 Troubleshooting

### Common Issues

#### 1. Merge Conflicts
```bash
# Show conflict details
claude-manage show-conflicts

# Resolve with override
claude-manage resolve --strategy=override

# Or resolve with merge
claude-manage resolve --strategy=merge
```

#### 2. Permission Denied
```bash
# Check policy violations
claude-manage check-policy

# Request exception
claude-manage request-exception --section="Testing" --reason="Legacy code"
```

#### 3. Update Failures
```bash
# Check update logs
cat ~/.claude-templates/logs/update.log

# Force update
claude-manage update --force

# Rollback if needed
claude-manage rollback
```

## 🎓 Best Practices

1. **Version Control**
   - Tag releases properly
   - Use semantic versioning
   - Keep changelog updated

2. **Testing**
   - Test template changes before merging
   - Validate in sample projects
   - Check backwards compatibility

3. **Communication**
   - Announce breaking changes
   - Provide migration guides
   - Gather feedback regularly

4. **Security**
   - Never override security policies
   - Review company policies regularly
   - Audit developer customizations

## 📚 Additional Resources

- [Git Workflow Guide](./GIT-WORKFLOW.md)
- [Tiered System Design](./tiered-claude-system.md)
- [Language Patterns](./language-mistake-proofing.md)
- [Example Usage](./claude-system/example-usage.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch from `develop`
3. Make changes following conventions
4. Add tests for new features
5. Submit PR with detailed description

---

Remember: The goal is to **automate best practices** while **preserving flexibility** where needed!