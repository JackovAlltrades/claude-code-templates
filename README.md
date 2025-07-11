# 🚀 Claude Templates - Lean Development System

## 📚 Documentation Hub

| Guide | Description |
|-------|------------|
| [**🎯 CHEAT SHEET**](CHEAT_SHEET.md) | Quick reference for all commands |
| [**📖 System Guide**](guides/CLAUDE_SYSTEM_GUIDE.md) | Complete system overview and setup |
| [**🔌 Port Manager Guide**](guides/PORT_MANAGER_GUIDE.md) | Detailed port management documentation |
| [**🤖 MCP Setup Guide**](guides/MCP_SETUP_GUIDE.md) | Model Context Protocol configuration |

## Overview
Reusable templates for rapid, standardized project initialization following lean principles.

## 🚨 IMPORTANT: Port Management Setup

Before starting ANY project, initialize the Universal Port Manager to prevent port conflicts:

```bash
# First time setup (one-time only)
chmod +x ~/.claude-templates/scripts/port-manager.py

# For EVERY new project
cd your-project
python3 ~/.claude-templates/scripts/port-manager.py init .

# This creates .ports.env with assigned ports:
# WEB_PORT=8000
# API_PORT=8100
# DB_PORT=5400
# etc.
```

## Available Templates

### 1. OpenAPI Lean Template (`openapi-lean.yaml`)
A complete OpenAPI 3.1 specification template following REST best practices:
- Resource-based paths (plural nouns)
- Verb-based operation IDs
- Built-in Spectral validation rules
- Standard error responses
- Security schemes (API Key, JWT)
- Terminology documentation via `x-terminology`

**Usage:**
```bash
cp ~/.claude-templates/openapi-lean.yaml api/openapi.yaml
# Edit to customize for your project
```

### 2. Lean API Initializer (`lean-api-init.sh`)
Interactive script to bootstrap a new API project:
- Creates directory structure
- Generates customized OpenAPI spec
- Sets up linting with Spectral
- Adds Makefile targets
- Creates FastAPI boilerplate
- Configures git hooks

**Usage:**
```bash
~/.claude-templates/lean-api-init.sh
```

### 3. Universal Port Manager (`scripts/port-manager.py`)
Centralized port management system that prevents "Address already in use" errors:
- Tracks all ports across all projects
- Auto-assigns ports by service type
- Shows what's using each port
- Integrates with Docker, Make, Node.js, Python

**Usage:**
```bash
# Initialize project ports
python3 ~/.claude-templates/scripts/port-manager.py init .

# Check port status
python3 ~/.claude-templates/scripts/port-manager.py status

# Free a port
python3 ~/.claude-templates/scripts/port-manager.py free 8080
```

### 4. Master Makefile (Coming Soon)
Standard Makefile with:
- Security checks
- API validation
- Test commands
- Documentation generation
- Deployment helpers
- Port management integration

## 🚀 Quick Start

### First Time Setup
```bash
# 1. Clone Claude Templates
cd ~/workspace
git clone <repo> .claude-templates

# 2. Run setup
cd .claude-templates
./setup.sh

# 3. Reload shell
source ~/.bashrc
```

### New Project Setup
```bash
# 1. Create new project
mkdir my-awesome-project && cd my-awesome-project

# 2. Initialize ports (CRITICAL - Do this first!)
port-manager init

# 3. Apply a template (optional)
~/.claude-templates/apply-template.sh saas-platform

# 4. Initialize git
git init

# 5. Set up MCP (optional but recommended)
./scripts/add-mcp-server-shared.sh --init
./scripts/add-mcp-server-shared.sh --common

# 6. Start developing!
port-manager status  # Check ports
./claude "Help me build..."  # Use Claude with MCP
```

## Design Principles

### 1. **Consistency Over Configuration**
- Standard naming conventions (enforced by linting)
- Single source of truth (OpenAPI spec)
- Predictable project structure

### 2. **Lean & Fast**
- Minimal boilerplate
- Quick to start, easy to extend
- Focus on what matters

### 3. **Quality Built-In**
- Automated validation
- Git hooks for mistake prevention
- Documentation as code

### 4. **OpenAPI-First**
- Design API before implementation
- Generate code from spec
- Automatic documentation
- Type safety

## Naming Conventions

### Paths
```yaml
/resources          # Plural nouns
/resources/{id}     # Resource by ID
/resources/{id}/sub-resources  # Nested resources
```

### Operations
```yaml
operationId: listResources    # GET /resources
operationId: createResource   # POST /resources
operationId: getResource      # GET /resources/{id}
operationId: updateResource   # PUT /resources/{id}
operationId: deleteResource   # DELETE /resources/{id}
```

### Schemas
```yaml
Resource              # Singular, PascalCase
CreateResourceRequest # Request suffix
UpdateResourceRequest # Action + Resource + Type
ResourceResponse      # Response suffix
```

## Integration with Claude

When starting a new project with Claude:

1. **Mention the template**: "Use the lean API template"
2. **Provide context**: Project name, description, domain
3. **Claude will**:
   - Apply the template
   - Follow naming conventions
   - Set up validation
   - Generate initial code

## Customization

All templates support environment variables:
- `${PROJECT_NAME}` - Your project name
- `${PROJECT_DESCRIPTION}` - Brief description
- `${DOMAIN}` - Your domain name
- `${PORT}` - API port (default: 8000)

## Future Templates

- [ ] Lean Makefile template
- [ ] Docker Compose template
- [ ] CI/CD pipeline templates (GitHub Actions, GitLab CI)
- [ ] Python project template
- [ ] TypeScript project template
- [ ] Database migration template

## Contributing

To add a new template:
1. Create file in `~/.claude-templates/`
2. Add documentation to this README
3. Include usage examples
4. Test with a sample project

## License

These templates are free to use and modify for any project.