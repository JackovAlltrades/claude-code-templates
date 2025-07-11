# 🎯 Claude Templates System - Complete Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Core Components](#core-components)
3. [Installation & Setup](#installation--setup)
4. [Project Templates](#project-templates)
5. [CLAUDE.md Memory System](#claudemd-memory-system)
6. [Port Management](#port-management)
7. [MCP Integration](#mcp-integration)
8. [Lean Six Sigma Integration](#lean-six-sigma-integration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## System Overview

The Claude Templates System is a comprehensive development framework designed to standardize project setup, enhance LLM collaboration, and implement Lean Six Sigma principles across all projects.

### 🎯 Core Philosophy
- **Single Source of Truth**: One authoritative location for each piece of information
- **LLM-First Development**: Optimized for AI collaboration
- **Lean Principles**: Eliminate waste, maximize value
- **Consistency**: Same patterns across all projects
- **Automation**: Scripts and tools for repetitive tasks

### 🏗️ System Architecture
```
~/.claude-templates/
├── setup.sh                    # Main installation script
├── CHEAT_SHEET.md             # Quick reference
├── guides/                    # Detailed documentation
│   ├── CLAUDE_SYSTEM_GUIDE.md # This file
│   ├── PORT_MANAGER_GUIDE.md  # Port management
│   └── MCP_SETUP_GUIDE.md     # MCP integration
├── scripts/                   # Utility scripts
│   ├── universal-port-manager.py
│   ├── port-manager.py
│   └── add-mcp-server-shared.sh
├── templates/                 # Project templates
│   ├── saas-platform/
│   ├── api-service/
│   └── web-app/
└── mcp/                      # MCP configurations
    └── shared/               # Shared MCP resources
```

## Core Components

### 1. **CLAUDE.md Memory System**
The heart of LLM collaboration - a persistent memory file that maintains context across sessions.

**Key Features:**
- Project overview and context
- Code philosophy and principles
- Common commands and patterns
- Recent changes and decisions
- Team conventions
- Troubleshooting guides

### 2. **Universal Port Manager**
Centralized port management across all projects to prevent conflicts.

**Key Features:**
- Automatic port assignment
- Conflict detection
- Process management
- Docker integration
- Status visualization

### 3. **Project Templates**
Pre-configured starting points for different project types.

**Available Templates:**
- `saas-platform`: Full-stack SaaS applications
- `api-service`: Microservice APIs
- `web-app`: Frontend applications
- `cli-tool`: Command-line utilities
- `data-pipeline`: Data processing workflows

### 4. **MCP Integration**
Model Context Protocol servers for enhanced AI capabilities.

**MCP Servers:**
- `mem0`: Persistent memory across sessions
- `filesystem`: Enhanced file operations
- `context7`: Project context management

### 5. **Lean Command System**
Standardized commands across all projects.

**Core Commands:**
```bash
lean truth update    # Update project metrics
lean test all       # Run all tests
lean deploy prod    # Deploy to production
lean ops health     # Check system health
```

## Installation & Setup

### Prerequisites
- WSL or Linux environment
- Python 3.7+
- Git
- Node.js (optional)
- Docker (optional)

### Quick Setup
```bash
# 1. Clone claude-templates
cd ~/workspace
git clone <your-repo> .claude-templates

# 2. Run setup
cd .claude-templates
./setup.sh

# 3. Source bashrc
source ~/.bashrc

# 4. Verify installation
port-manager --help
lean --help
```

### Manual Setup
```bash
# 1. Add to bashrc
cat >> ~/.bashrc << 'EOF'
# Claude Templates System
export CLAUDE_TEMPLATES_HOME="$HOME/workspace/.claude-templates"
export PATH="$CLAUDE_TEMPLATES_HOME/scripts:$PATH"

# Aliases
alias port-manager="python3 $CLAUDE_TEMPLATES_HOME/scripts/universal-port-manager.py"
alias lean="$CLAUDE_TEMPLATES_HOME/scripts/lean-cli.sh"
EOF

# 2. Install dependencies
pip install click rich python-dotenv

# 3. Create directories
mkdir -p ~/.config/claude-templates
mkdir -p ~/.config/port-manager
```

## Project Templates

### Using Templates
```bash
# 1. Create new project
mkdir my-new-project
cd my-new-project

# 2. Apply template
~/.claude-templates/scripts/apply-template.sh saas-platform

# 3. Initialize
port-manager init
lean init
```

### Template Structure
Each template includes:
- `CLAUDE.md`: Pre-configured memory file
- `PROJECT_TRUTH.md`: Metrics tracking
- `.ports.env`: Port configuration
- `Makefile`: Common commands
- `docker-compose.yml`: Development environment
- `.github/workflows/`: CI/CD pipelines

### Customizing Templates
```bash
# 1. Copy existing template
cp -r ~/.claude-templates/templates/saas-platform ~/.claude-templates/templates/my-template

# 2. Modify files
vim ~/.claude-templates/templates/my-template/CLAUDE.md

# 3. Use new template
~/.claude-templates/scripts/apply-template.sh my-template
```

## CLAUDE.md Memory System

### Structure
```markdown
# Project Name - LLM Memory System

## Project Overview
Brief description, tech stack, key features

## Code Philosophy
Core principles, design patterns

## Warp Rules (Fast Development)
Speed-focused guidelines

## Project Commands & Patterns
Common commands, project-specific patterns

## Critical Project Decisions
Architecture decisions, technology choices

## Code Organization
Directory structure, key files

## Common Tasks
For new features, bug fixes, etc.

## Configuration Management
Environment variables, secrets

## Testing & Quality
Test strategy, quality standards

## Error Patterns & Solutions
Common errors and fixes

## Team Conventions
Naming, git workflow, code review

## Integration Points
External services, APIs, webhooks

## Performance Considerations
Optimization guidelines, monitoring

## Security Practices
Security checklist, sensitive data

## Recent Implementations
Latest changes and updates

## Memory Extensions
Short-term and long-term memory
```

### Best Practices
1. **Update Regularly**: After significant changes
2. **Be Specific**: Include exact commands and paths
3. **Document Decisions**: Explain the "why"
4. **Include Examples**: Show, don't just tell
5. **Track TODOs**: Maintain current state

### LLM Instructions
Add these to the top of CLAUDE.md:
```markdown
**Purpose**: Single source of truth for LLMs working on [Project Name]
**Last Updated**: YYYY-MM-DD
**Project Template**: saas-platform

When working on this project:
1. Always read this file first
2. Check PROJECT_TRUTH.md for metrics
3. Follow established patterns
4. Update this file after changes
```

## Port Management

### Basic Workflow
```bash
# 1. Initialize project
port-manager init

# 2. Check status
port-manager status

# 3. Before running services
port-manager scan || exit 1

# 4. Free ports if needed
port-manager free 8000

# 5. Clean up
port-manager clean
```

### Integration Examples

**Docker Compose:**
```yaml
services:
  web:
    ports:
      - "${WEB_PORT:-8000}:8000"
    env_file:
      - .ports.env
```

**Makefile:**
```makefile
include .ports.env
export

run: check-ports
	docker-compose up

check-ports:
	@port-manager scan
```

**Node.js:**
```javascript
// Load ports
require('dotenv').config({ path: '.ports.env' });
const port = process.env.WEB_PORT || 8000;
```

## MCP Integration

### Setup MCP Servers
```bash
# 1. Initial setup
./scripts/add-mcp-server-shared.sh --init

# 2. Add common servers
./scripts/add-mcp-server-shared.sh --common

# 3. Configure project
cat > .mcp/config.json << EOF
{
  "servers": {
    "mem0": {
      "command": "python",
      "args": ["~/.mcp-shared/servers/mem0-server.py"],
      "env": {
        "OPENAI_API_KEY": "\${OPENAI_API_KEY}"
      }
    }
  }
}
EOF
```

### Using with Claude
```bash
# Use Claude with MCP
./claude "Help me understand this codebase"

# MCP will provide:
# - Persistent memory (mem0)
# - Enhanced file operations
# - Project context
```

### MCP Best Practices
1. **API Keys**: Use Doppler or environment variables
2. **Storage**: Keep project-specific in `.mcp/storage/`
3. **Shared Resources**: Use `~/.mcp-shared/` for common servers
4. **Configuration**: Version control `.mcp/config.json`

## Lean Six Sigma Integration

### SIPOC Framework
```yaml
# In CLAUDE.md
Suppliers:
  - User inputs
  - External APIs
  - Databases

Inputs:
  - Requirements
  - Data
  - Configuration

Process:
  - Validate
  - Transform
  - Persist

Outputs:
  - Results
  - Reports
  - Notifications

Customers:
  - End users
  - Admins
  - Systems
```

### Lean Commands
```bash
# Update metrics
lean truth update project

# Quality check
lean ops quality measure

# Value stream mapping
lean analyze value-stream

# Waste elimination
lean optimize remove-waste
```

### Continuous Improvement
1. **Measure**: Track key metrics in PROJECT_TRUTH.md
2. **Analyze**: Regular retrospectives
3. **Improve**: Implement changes
4. **Control**: Monitor results
5. **Standardize**: Update templates

## Best Practices

### 1. **Project Setup Checklist**
- [ ] Initialize with template
- [ ] Configure ports
- [ ] Set up CLAUDE.md
- [ ] Configure MCP
- [ ] Add to version control
- [ ] Document in README

### 2. **Daily Workflow**
```bash
# Morning
port-manager status
lean truth check
git pull

# During development
# Update CLAUDE.md after decisions
# Use lean commands
# Check ports before running

# End of day
lean truth update
port-manager clean
git commit
```

### 3. **LLM Collaboration**
- Always provide CLAUDE.md context
- Use specific project terms
- Reference exact file paths
- Include error messages
- Update memory after sessions

### 4. **Port Management**
- Initialize every project
- Use .ports.env everywhere
- Check before starting services
- Clean up regularly
- Document custom ports

### 5. **Template Maintenance**
- Regular updates
- Test changes
- Version templates
- Document modifications
- Share improvements

## Troubleshooting

### Common Issues

#### 1. **Port Conflicts**
```bash
# Error: Port already in use
port-manager scan
port-manager free 8000
# Or change port in .ports.env
```

#### 2. **MCP Connection Failed**
```bash
# Check configuration
cat .mcp/config.json

# Verify servers running
ps aux | grep mcp

# Check logs
tail -f ~/.mcp/logs/mem0.log
```

#### 3. **Template Not Found**
```bash
# List available templates
ls ~/.claude-templates/templates/

# Check template path
echo $CLAUDE_TEMPLATES_HOME
```

#### 4. **Lean Command Not Found**
```bash
# Add to PATH
export PATH="$HOME/workspace/.claude-templates/scripts:$PATH"

# Or use full path
~/.claude-templates/scripts/lean-cli.sh
```

#### 5. **Line Ending Issues (WSL)**
```bash
# Fix script line endings
dos2unix ~/.claude-templates/scripts/*
```

### Debug Mode
```bash
# Enable debug output
export CLAUDE_DEBUG=1
export PORT_MANAGER_DEBUG=1

# Run commands
port-manager status
lean truth check
```

### Getting Help
1. Check CHEAT_SHEET.md for quick reference
2. Read specific guides in `guides/`
3. Check script help: `command --help`
4. Review example projects
5. Ask Claude with context from CLAUDE.md

## Advanced Topics

### Custom Scripts
```bash
# Add to ~/.claude-templates/scripts/
cat > ~/.claude-templates/scripts/my-tool.sh << 'EOF'
#!/bin/bash
# Custom tool description
echo "Running custom tool..."
EOF

chmod +x ~/.claude-templates/scripts/my-tool.sh
```

### Project Hooks
```bash
# .claude-hooks/pre-commit
#!/bin/bash
lean test unit
port-manager scan
```

### Multi-Environment
```bash
# Development
ln -s .env.dev .env
ln -s .ports.dev.env .ports.env

# Production
ln -s .env.prod .env
ln -s .ports.prod.env .ports.env
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Setup Claude Templates
  run: |
    git clone ${{ secrets.CLAUDE_TEMPLATES_REPO }} .claude-templates
    .claude-templates/scripts/ci-setup.sh
    
- name: Run Lean Tests
  run: lean test all
```

---

*Claude Templates System v2.0 - Your AI-Powered Development Assistant 🚀*

*"Single Source of Truth, Infinite Possibilities"*