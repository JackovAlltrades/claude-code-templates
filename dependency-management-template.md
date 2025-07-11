# Universal Dependency Management Template

## Overview
This template provides a language-agnostic approach to dependency management with security and stability in mind.

## Core Principles
1. **Security First**: Regular security patches without breaking changes
2. **Stability**: Test all updates before applying
3. **Visibility**: Clear reporting of what changes and why
4. **Rollback**: Always maintain ability to revert

## Language-Specific Implementations

### Python Projects
```bash
# Core files needed:
- requirements.txt (production deps)
- requirements-dev.txt (dev deps)
- scripts/check-dependency-updates.py
- scripts/safe-update-deps.sh
- .github/workflows/dependency-update.yml
- .github/dependabot.yml
```

### Node.js Projects
```bash
# Adapt scripts to use:
- npm outdated / npm audit
- package-lock.json for pinning
- npm-check-updates for analysis
```

### Go Projects
```bash
# Adapt scripts to use:
- go list -u -m all
- go mod tidy
- nancy for vulnerability scanning
```

### Ruby Projects
```bash
# Adapt scripts to use:
- bundle outdated
- bundle-audit
- Gemfile.lock for pinning
```

## Universal Scripts Structure

### 1. Dependency Checker Script
```python
#!/usr/bin/env python3
"""
Universal pattern - adapt for your package manager:
1. List outdated packages
2. Categorize by risk (major/minor/patch)
3. Check for security advisories
4. Generate actionable report
"""
```

### 2. Safe Update Script
```bash
#!/bin/bash
# Universal pattern:
# 1. Backup current dependency file
# 2. Create test environment
# 3. Test updates incrementally
# 4. Run test suite
# 5. Apply only passing updates
# 6. Provide rollback instructions
```

### 3. CI/CD Integration
```yaml
# GitHub Actions pattern:
# 1. Schedule weekly checks
# 2. Run security scans
# 3. Test in isolated environment
# 4. Create PR only if tests pass
# 5. Include detailed change report
```

## Quick Setup Commands

### For Python Projects:
```bash
# Copy the templates
cp ~/.claude-templates/deps/python/* ./scripts/
chmod +x ./scripts/*.sh

# Create requirements-dev.txt if missing
echo "# Development dependencies" > requirements-dev.txt

# Add to .gitignore
echo ".dependency-backups/" >> .gitignore
echo ".test-update-env/" >> .gitignore
```

### For Node.js Projects:
```bash
# Install tools
npm install -g npm-check-updates npm-audit-resolver

# Create update script
cp ~/.claude-templates/deps/node/check-updates.js ./scripts/
```

## Integration Checklist
- [ ] Choose appropriate dependency manager files
- [ ] Adapt scripts to package manager commands  
- [ ] Set up CI/CD automation
- [ ] Configure security scanning
- [ ] Document update process in README
- [ ] Train team on safe update procedures

## Security Tools by Language

| Language | Dependency Check | Security Scan | Auto-update Tool |
|----------|-----------------|---------------|------------------|
| Python   | pip-audit       | bandit        | dependabot       |
| Node.js  | npm audit       | snyk          | renovate         |
| Go       | nancy           | gosec         | dependabot       |
| Ruby     | bundle-audit    | brakeman      | dependabot       |
| Java     | OWASP check     | spotbugs      | renovate         |

## Best Practices
1. **Never auto-merge** major version updates
2. **Test in staging** before production
3. **Monitor** for security advisories
4. **Document** any version pins and why
5. **Review** changelogs for breaking changes