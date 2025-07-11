# Claude Templates Integration Guide

> Complete guide for integrating Claude templates and best practices into any project

## Table of Contents
1. [Overview](#overview)
2. [What's Included](#whats-included)
3. [New Project Setup](#new-project-setup)
4. [Existing Project Integration](#existing-project-integration)
5. [File Structure](#file-structure)
6. [Workflow Integration](#workflow-integration)
7. [Truth System](#truth-system)
8. [Quick Reference](#quick-reference)

---

## Overview

The Claude Templates system provides a complete framework for AI-assisted development with:
- **Single Source of Truth** documentation
- **Git workflow** with branching strategies
- **Bun runtime** configuration (our preferred JS tooling)
- **Security-first** practices
- **Lean development** principles

### Templates Location
All templates are stored in: `~/workspace/.claude-templates/`

---

## What's Included

### Core Files
1. **CLAUDE.md** - AI context and project memory
2. **PROJECT_TRUTH.md** - Single source of truth for project status
3. **GIT-WORKFLOW.md** - Git branching and commit standards
4. **.gitignore** - Comprehensive ignore patterns

### Supporting Files
- `claude-base-template.md` - Basic CLAUDE.md template
- `claude-full-template.md` - Comprehensive template with all sections
- `engineer-instructions.md` - Detailed engineering patterns
- `setup-git-workflow.sh` - Git setup automation
- `project-setup.sh` - New project initialization

---

## New Project Setup

### Step 1: Create Project Directory
```bash
mkdir ~/workspace/my-new-project
cd ~/workspace/my-new-project
```

### Step 2: Run Setup Script
```bash
~/workspace/.claude-templates/project-setup.sh my-new-project
```

### Step 3: Initialize Git with Workflow
```bash
git init
git branch -m main
cp ~/workspace/.claude-templates/GIT-WORKFLOW.md .
```

### Step 4: Configure for Bun (if JavaScript project)
```bash
# Update package.json scripts to use bunx
# Change process.env to Bun.env in configs
```

### Step 5: Create PROJECT_TRUTH.md
Use the template structure and customize for your project

---

## Existing Project Integration

### Step 1: Navigate to Project
```bash
cd ~/workspace/existing-project
```

### Step 2: Copy Core Files
```bash
# Copy templates
cp ~/workspace/.claude-templates/GIT-WORKFLOW.md .
cp ~/workspace/.claude-templates/claude-base-template.md ./CLAUDE.md

# Customize CLAUDE.md for your project
# Update technology stack, commands, etc.
```

### Step 3: Create PROJECT_TRUTH.md
Create this file with your project's current status:
- Executive Summary
- Activity Log
- Technical Architecture
- Metrics Dashboard
- Risk Register
- Decision Log

### Step 4: Update .gitignore
Add security and project-specific patterns:
```
# Bun
bun.lockb
.bun/

# Security
*.pem
*.key
*.cert
secrets/
credentials/
```

### Step 5: Configure Git Workflow
```bash
# Create develop branch
git checkout -b develop

# Set up commit message standards
# Follow conventional commits: feat:, fix:, docs:, etc.
```

---

## File Structure

### Required Files
```
project-root/
├── CLAUDE.md              # AI memory and context
├── PROJECT_TRUTH.md       # Single source of truth
├── GIT-WORKFLOW.md        # Git standards
├── .gitignore            # Security-focused ignores
└── README.md             # Public documentation
```

### Optional Enhancements
```
project-root/
├── .github/
│   ├── workflows/        # CI/CD pipelines
│   └── pull_request_template.md
├── docs/
│   └── architecture/     # Technical decisions
└── scripts/
    └── setup.sh          # Project setup automation
```

---

## Workflow Integration

### Daily Development Flow

1. **Start Work**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/description
   ```

2. **During Development**
   - Update PROJECT_TRUTH.md activity log
   - Document decisions in decision log
   - Follow commit standards

3. **Complete Work**
   ```bash
   git add -A
   git commit -m "feat: implement new feature"
   git push -u origin feature/description
   # Create PR to develop
   ```

### Truth Updates
After significant changes:
1. Update PROJECT_TRUTH.md metrics
2. Log decisions with rationale
3. Update risk register if needed
4. Commit with: `docs: update project truth`

---

## Truth System

### PROJECT_TRUTH.md Sections

#### 1. Executive Summary
- Project name and status
- Current phase and health
- Quick stats (velocity, debt, coverage)

#### 2. Activity Log
Most recent first:
- Who made changes
- What was done
- Impact of changes
- Next steps
- Any blockers

#### 3. Technical Architecture
- Current stack
- Key design decisions
- Architecture patterns

#### 4. Metrics Dashboard
- Velocity metrics
- Quality metrics
- Business metrics

#### 5. Risk Register
Track risks with:
- Impact level
- Probability
- Mitigation strategy

#### 6. Decision Log
Document all major decisions:
- Context
- Decision made
- Alternatives considered
- Outcome

### Update Frequency
- **Activity Log**: Every significant change
- **Metrics**: End of each sprint
- **Decisions**: When made
- **Risks**: When identified or status changes

---

## Quick Reference

### Essential Commands

```bash
# New project with templates
~/workspace/.claude-templates/project-setup.sh project-name

# Add to existing project
cp ~/workspace/.claude-templates/claude-base-template.md ./CLAUDE.md
cp ~/workspace/.claude-templates/GIT-WORKFLOW.md .

# Create truth file
touch PROJECT_TRUTH.md
# Add sections from this guide

# Git workflow
git checkout -b feature/name
git commit -m "type: description"
```

### File Templates Checklist

- [ ] CLAUDE.md created and customized
- [ ] PROJECT_TRUTH.md with all sections
- [ ] GIT-WORKFLOW.md copied
- [ ] .gitignore updated for security
- [ ] Git initialized with main/develop branches
- [ ] If JS project: Bun configured
- [ ] Initial commit with setup

### Best Practices

1. **Keep PROJECT_TRUTH.md Updated**
   - It's your single source of truth
   - Update with every significant change

2. **Use Conventional Commits**
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation
   - chore: Maintenance

3. **Security First**
   - Never commit secrets
   - Use comprehensive .gitignore
   - Review before committing

4. **Leverage AI Context**
   - CLAUDE.md helps AI understand your project
   - Include project-specific patterns
   - Document common commands

---

## Integration Examples

### For a React Project
```markdown
# In CLAUDE.md
- **Runtime**: Bun
- **Framework**: React + Vite
- **Testing**: Vitest
- **Package Manager**: Bun

# Commands
bun install
bun run dev
bun test
```

### For a Python Project
```markdown
# In CLAUDE.md
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Testing**: pytest
- **Package Manager**: pip/poetry

# Commands
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### For a Rust Project
```markdown
# In CLAUDE.md
- **Language**: Rust
- **Build Tool**: Cargo
- **Testing**: Built-in
- **Package Manager**: Cargo

# Commands
cargo build
cargo run
cargo test
```

---

## Troubleshooting

### Common Issues

1. **Bun not installed**
   - Install from: https://bun.sh
   - Or fallback to npm/yarn

2. **Git workflow conflicts**
   - Ensure main branch exists
   - Create develop from main
   - Never work directly on main

3. **PROJECT_TRUTH.md format**
   - Use markdown tables for metrics
   - Keep activity log chronological
   - Update dates consistently

---

## Additional Resources

- **Templates**: `~/workspace/.claude-templates/`
- **Examples**: Check other projects using the system
- **Updates**: Templates are version controlled

---

*This guide is part of the Claude Templates system. For updates, check the templates repository.*