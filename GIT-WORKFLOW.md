# Git Workflow & Branching Strategy for Claude Templates

## 🌳 Branch Structure

```
main (protected)
├── develop
├── release/v1.x
├── feature/tiered-system
├── feature/language-patterns
├── hotfix/security-fix
└── personal/developer-name
```

### Branch Purposes

| Branch Type | Purpose | Naming | Merge Target | Protected |
|------------|---------|--------|--------------|-----------|
| `main` | Production-ready templates | `main` | - | ✅ Yes |
| `develop` | Integration branch | `develop` | `main` | ✅ Yes |
| `release/*` | Release preparation | `release/v1.2` | `main` | ✅ Yes |
| `feature/*` | New features | `feature/description` | `develop` | ❌ No |
| `hotfix/*` | Urgent fixes | `hotfix/issue` | `main` & `develop` | ❌ No |
| `personal/*` | Developer experiments | `personal/username` | `develop` | ❌ No |

## 🔄 Workflow Patterns

### 1. Feature Development Flow

```bash
# 1. Start from latest develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/rust-safety-patterns

# 3. Make changes iteratively
git add -p  # Interactive staging
git commit -m "feat(rust): add memory safety patterns"

# 4. Keep branch updated
git fetch origin
git rebase origin/develop

# 5. Push and create PR
git push -u origin feature/rust-safety-patterns
```

### 2. Release Flow

```bash
# 1. Create release branch from develop
git checkout -b release/v1.3.0 develop

# 2. Bump version
sed -i 's/version: .*/version: 1.3.0/' claude-system/config.yaml
git commit -m "chore: bump version to 1.3.0"

# 3. Test and fix issues
# ... testing ...
git commit -m "fix: correct Python venv detection"

# 4. Merge to main
git checkout main
git merge --no-ff release/v1.3.0
git tag -a v1.3.0 -m "Release version 1.3.0"

# 5. Back-merge to develop
git checkout develop
git merge --no-ff release/v1.3.0

# 6. Push everything
git push origin main develop v1.3.0
```

### 3. Hotfix Flow

```bash
# 1. Branch from main
git checkout -b hotfix/security-update main

# 2. Fix issue
git commit -m "fix(security): update secret detection pattern"

# 3. Merge to both main and develop
git checkout main
git merge --no-ff hotfix/security-update
git tag -a v1.2.1 -m "Hotfix: security update"

git checkout develop
git merge --no-ff hotfix/security-update

# 4. Clean up
git branch -d hotfix/security-update
git push origin main develop v1.2.1
```

## 📝 Commit Message Standards

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

### Examples
```bash
feat(python): add async/await patterns for Python 3.11+

- Add coroutine best practices
- Include asyncio pitfalls section
- Update virtual environment section

Closes #42

---

fix(docker): correct multi-stage build example

The previous example was missing the --from flag in COPY commands

---

docs(readme): update installation instructions

- Add Windows-specific setup steps
- Include troubleshooting section
- Fix broken links
```

## 🛡️ Branch Protection Rules

### For `main` branch:
```yaml
protection_rules:
  require_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_pr_approvals: true
    require_code_owner_reviews: true
    
  require_status_checks:
    strict: true  # Require branches to be up to date
    contexts:
      - continuous-integration/validate
      - security/snyk
      - test/unit
      
  require_conversation_resolution: true
  require_signed_commits: true
  
  enforce_admins: false  # Allow admins to bypass in emergencies
  
  restrictions:
    users: []
    teams: ["senior-engineers"]
```

### For `develop` branch:
```yaml
protection_rules:
  require_pull_request_reviews:
    required_approving_review_count: 1
    
  require_status_checks:
    contexts:
      - continuous-integration/validate
      - test/unit
```

## 🔍 Code Review Process

### PR Template (`.github/pull_request_template.md`)
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested merger.py with sample configs
- [ ] Validated generated CLAUDE.md
- [ ] Checked backwards compatibility

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass

## Impact Analysis
- Which templates are affected?
- Will this require updates to existing projects?
- Are there any breaking changes?
```

### Review Guidelines
1. **Check for breaking changes** - Will this affect existing users?
2. **Validate patterns** - Are the patterns correct and tested?
3. **Security review** - No hardcoded secrets or vulnerable patterns
4. **Documentation** - Is it clear how to use new features?
5. **Test coverage** - Are there tests for new functionality?

## 🚀 CI/CD Pipeline

### `.github/workflows/ci.yml`
```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install black flake8 mypy pytest
          
      - name: Lint with flake8
        run: flake8 claude-system/
        
      - name: Format check with black
        run: black --check claude-system/
        
      - name: Type check with mypy
        run: mypy claude-system/
        
      - name: Run tests
        run: pytest tests/
        
      - name: Validate YAML configs
        run: |
          pip install yamllint
          yamllint -d relaxed claude-system/**/*.yaml
          
      - name: Check markdown
        uses: DavidAnson/markdownlint-cli2-action@v11
        
      - name: Security scan
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  test-merge:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v3
      
      - name: Test merger script
        run: |
          python claude-system/merger.py --project tests/sample-project
          
      - name: Validate output
        run: |
          test -f tests/sample-project/CLAUDE.md
          grep -q "auto-generated" tests/sample-project/CLAUDE.md

  release:
    if: github.ref == 'refs/heads/main'
    needs: [validate, test-merge]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create release
        uses: semantic-release/semantic-release@v19
```

## 📋 Release Process

### 1. Version Numbering (Semantic Versioning)
```
MAJOR.MINOR.PATCH

1.0.0 - Initial release
1.1.0 - Added language patterns (backward compatible)
2.0.0 - Tiered system (breaking change)
```

### 2. Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in config.yaml
- [ ] Migration guide for breaking changes
- [ ] Announcement prepared

### 3. Release Notes Template
```markdown
# Release v1.3.0

## 🎉 Highlights
- Tiered inheritance system
- Role-based templates
- Auto-update capability

## 🚀 New Features
- feat(system): implement 3-tier merge system (#45)
- feat(languages): add Rust safety patterns (#48)

## 🐛 Bug Fixes
- fix(python): correct venv detection logic (#52)

## 📚 Documentation
- docs(guide): add tiered system usage guide (#50)

## 💔 Breaking Changes
None in this release

## 🔄 Migration Guide
N/A

## 📊 Stats
- 23 commits
- 5 contributors
- 15 files changed
```

## 🔐 Security Workflow

### Security Issue Handling
1. **Never commit fixes directly to main**
2. Use `hotfix/security-*` branches
3. Request security review from senior team
4. Update SECURITY.md with disclosure

### `.github/SECURITY.md`
```markdown
# Security Policy

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Email: security@claude-templates.dev

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

Response time: within 48 hours
```

## 🔄 Sync with Upstream

For personal forks:

```bash
# 1. Add upstream remote
git remote add upstream https://github.com/anthropics/claude-templates.git

# 2. Fetch upstream
git fetch upstream

# 3. Merge or rebase
git checkout main
git merge upstream/main

# Or rebase your changes
git checkout feature/my-feature
git rebase upstream/develop

# 4. Push to your fork
git push origin main
```

## 📊 Git Hooks

### `.git/hooks/pre-commit`
```bash
#!/bin/bash
# Validate Python files
python -m black --check claude-system/
python -m flake8 claude-system/

# Check for secrets
git diff --staged --name-only | xargs -I {} sh -c 'git show :"{}" | grep -E "(password|secret|key|token)" && echo "Potential secret in {}" && exit 1'

# Validate YAML
yamllint -d relaxed claude-system/**/*.yaml
```

### `.git/hooks/commit-msg`
```bash
#!/bin/bash
# Enforce conventional commits
commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .+'
if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Format: <type>(<scope>): <subject>"
    exit 1
fi
```

## 🎯 Best Practices

1. **Never work directly on main or develop**
2. **Keep PRs small and focused** - One feature per PR
3. **Rebase feature branches** - Keep history clean
4. **Write descriptive commit messages** - Future you will thank you
5. **Tag releases properly** - Use annotated tags
6. **Document breaking changes** - Include migration guides
7. **Review your own PR first** - Catch obvious issues
8. **Keep branches up to date** - Rebase or merge regularly