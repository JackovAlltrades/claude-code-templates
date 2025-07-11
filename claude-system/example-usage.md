# Tiered CLAUDE System - Example Usage

## Quick Start

### 1. Initialize Company Layer (Senior Dev Team)

```bash
# In company repository
mkdir -p .claude-company/policies
mkdir -p .claude-company/roles

# Create company config
cat > .claude-company/config.yaml << 'EOF'
company: AcmeCorp
version: 1.0.0

# What we inherit from universal
inheritance:
  from: universal
  exclude:
    - "languages/cobol.md"
    - "languages/fortran.md"

# Company-wide policies
policies:
  code_review:
    required: true
    approvers_min: 2
  
  testing:
    coverage_minimum: 80
    types_required: [unit, integration]
  
  security:
    secret_scanning: mandatory
    dependency_audit: weekly

# Role-based customizations  
roles:
  frontend:
    primary_languages: [typescript, javascript, react]
    exclude_sections: ["backend-specific", "database", "rust"]
    
  backend:
    primary_languages: [python, go]
    exclude_sections: ["frontend-specific", "css"]
    
  fullstack:
    include_all: true
    
  devops:
    primary_focus: ["kubernetes", "docker", "ci-cd"]
    include_extra: ["monitoring", "security"]
EOF

# Create company standards
cat > .claude-company/standards.md << 'EOF'
## Company Coding Standards

### Code Review Process
All code must be reviewed by at least 2 developers before merging.
- Use PR templates
- Run automated checks first
- Security review for auth changes

### API Standards
- RESTful design required
- OpenAPI documentation mandatory
- Versioning: /api/v{number}/

### Git Workflow  
- Feature branches from develop
- Squash merge to main
- Semantic versioning for releases
EOF
```

### 2. Initialize Project Layer (Team/Project Lead)

```bash
# In project repository
mkdir -p .claude-project/developer

# Create project config
cat > .claude-project/config.yaml << 'EOF'
project: awesome-api
team: platform
version: 1.0.0

# Project stack
technologies:
  languages: [python, typescript]
  frameworks: [fastapi, react]
  databases: [postgresql, redis]
  
# Service-specific configs
services:
  - name: api-gateway
    language: python
    framework: fastapi
    
  - name: frontend
    language: typescript
    framework: react
    
# Allow developers to customize
developer_overrides:
  enabled: true
  max_override_sections: 5
EOF

# Create project overrides
cat > .claude-project/overrides.md << 'EOF'
## Project-Specific Guidelines

### Local Development
1. Use Docker Compose for all services
2. Python: Always use venv, located at `./venv`
3. Node: Use pnpm (not npm or yarn)

### Project Structure
```
src/
├── api/          # FastAPI backend
├── frontend/     # React frontend  
├── shared/       # Shared types/utils
└── scripts/      # Dev tools
```

### Testing Strategy
- API: pytest with 90% coverage
- Frontend: Jest + React Testing Library
- E2E: Playwright for critical paths
EOF
```

### 3. Developer Customization (Individual Dev)

```bash
# Create personal preferences
cat > .claude-project/developer/jdoe.md << 'EOF'
## Personal Development Preferences

### Editor Setup
- VS Code with Python and ESLint extensions
- Format on save enabled
- Tab size: 2 spaces

### Debugging Preferences  
- Use debugpy for Python
- Chrome DevTools for React
- Always add meaningful log statements

### Personal Shortcuts
- `make dev` - Start all services
- `make test-watch` - Run tests in watch mode
- `make lint-fix` - Auto-fix linting issues
EOF
```

### 4. Generate Final CLAUDE.md

```bash
# Run merger
python ~/.claude-templates/claude-system/merger.py --username jdoe

# Or use the CLI tool
claude-manage merge --user jdoe
```

## Example Output Structure

The final CLAUDE.md would have this structure:

```markdown
# CLAUDE.md - Generated 2024-01-07 10:30:00

*This file is auto-generated from 3-tier template system. Do not edit directly.*

## Project Overview
[From universal + company info + project specifics]

## Language Guidelines

### Python Development
[Universal Python rules]
[Company Python standards]
[Project Python preferences]
[Developer Python shortcuts - if applicable]

### TypeScript Development  
[Universal TS rules]
[Company TS standards]
[Project TS preferences]

## Company Coding Standards
[From company layer - cannot be overridden]

## Project-Specific Guidelines
[From project layer]

## Personal Development Preferences
[From developer layer - only if enabled]
```

## Inheritance Examples

### Example 1: Security Policy (No Override)
```yaml
# Universal says:
- Use environment variables for secrets

# Company enforces:
- Must use HashiCorp Vault
- override_allowed: false

# Project tries:
- Use .env files  # ❌ REJECTED

# Result: Must use HashiCorp Vault
```

### Example 2: Code Style (Override Allowed)
```yaml
# Universal says:
- 4 spaces for Python

# Company says:
- 2 spaces for Python
- override_allowed: true

# Project says:
- 4 spaces for Python (team preference)

# Result: 4 spaces (project override accepted)
```

### Example 3: Testing Requirements (Partial Override)
```yaml
# Universal says:
- Write tests

# Company says:
- Minimum 80% coverage
- override_allowed: true
- max_decrease: 10%

# Project says:
- 75% coverage (legacy code)

# Result: 75% accepted (within allowed decrease)
```

## Update Workflow Example

### When Universal Templates Update:

```bash
# 1. Auto-check runs weekly
$ claude-manage update
🔄 Checking for updates...
📦 New version available: 1.2.0 → 1.3.0
📝 Changed sections:
  - Python: Added Python 3.12 patterns
  - Security: Updated OWASP Top 10 (2024)
  - Docker: New multi-platform build patterns

# 2. Review changes
$ claude-manage diff
+ Python 3.12: Use new f-string syntax
+ Security: Check for JWT algorithm confusion
- Docker: Removed deprecated MAINTAINER

# 3. Merge updates
$ claude-manage merge
✅ Non-breaking changes merged automatically
⚠️  Breaking change in Security section requires review
📝 Created PR #123 for manual review

# 4. After approval
$ git pull
$ cat CLAUDE.md
# ... updated content with new patterns ...
```

## CI/CD Integration

### GitHub Action Example
```yaml
name: Update CLAUDE.md

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  update-claude:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Claude System
        run: |
          pip install -r ~/.claude-templates/requirements.txt
          
      - name: Check for updates
        run: |
          claude-manage update
          
      - name: Merge templates
        run: |
          claude-manage merge
          
      - name: Create PR if changed
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'chore: Update CLAUDE.md templates'
          body: 'Auto-generated update from universal templates'
          branch: update-claude-templates
```

## Best Practices

1. **Company Setup** (One-time by Senior Team)
   - Define non-overridable policies
   - Set up role templates
   - Configure inheritance rules

2. **Project Setup** (Per project by Team Lead)
   - Select applicable technologies
   - Define project-specific patterns
   - Enable/disable developer customization

3. **Developer Usage** (Daily by Individual Devs)
   - Read generated CLAUDE.md
   - Optionally add personal preferences
   - Use `claude-manage validate` before commits

4. **Maintenance** (Ongoing)
   - Review universal updates weekly
   - Update company policies quarterly  
   - Archive old project customizations