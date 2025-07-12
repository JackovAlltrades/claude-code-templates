# 🚀 Claude Templates System - Quick Reference

## 🎯 Quick Commands

### Port Management (Basic)
```bash
# Check all ports
port-manager status

# Show project ports
port-manager show

# Free a stuck port
port-manager free 8080

# Initialize project ports
port-manager init

# Clean dead registrations
port-manager clean
```

### 🧠 Intelligent Port Management
```bash
# Auto-allocate port by service type
python3 scripts/intelligent-port-manager.py allocate my-api --type api

# Check intelligent status
python3 scripts/intelligent-port-manager.py status

# Sync registry with actual usage
python3 scripts/intelligent-port-manager.py sync

# Show standard port ranges
python3 scripts/intelligent-port-manager.py ranges

# Export for LLM
python3 scripts/intelligent-port-manager.py export-llm

# Enable auto-allocation hooks
source scripts/port-hooks.sh
port-hooks on

# Quick commands with hooks enabled
port-status      # Show allocated ports
port-available   # Show available ranges
port-sync        # Sync registry
port-export      # Export project config
port-llm         # Export for LLM
```

### 🔄 Port Lifecycle Management
```bash
# Initialize service lifecycle
python3 scripts/port-lifecycle-manager.py init my-api api my-project

# Promote through stages
python3 scripts/port-lifecycle-manager.py promote my-api my-project development staging

# Check lifecycle status
python3 scripts/port-lifecycle-manager.py status

# Export deployment configs
python3 scripts/port-lifecycle-manager.py export staging --format docker
```

### Project Setup
```bash
# Setup new project with Claude templates
~/workspace/.claude-templates/setup.sh

# Initialize lean API project
~/workspace/.claude-templates/lean-api-init.sh

# Setup Git workflow
~/workspace/.claude-templates/setup-git-workflow.sh
```

### Claude Aliases
```bash
claude                  # Standard Claude CLI
claude-simple          # Use Sonnet model (faster)
claude-complex         # Use Opus model (smarter)
claude-smart           # Smart model selection
claude-patterns        # View coding patterns
claude-rules           # View warp rules
claude-templates       # Navigate to templates
```

### Lean Commands
```bash
lean truth update      # Update project truth
lean ops quality       # Quality metrics
lean test unit         # Run unit tests
lean deploy prod       # Deploy to production
```

## 📁 Key Locations

| What | Where |
|------|-------|
| Templates | `~/.claude-templates/` |
| Port Manager | `~/.claude-templates/scripts/universal-port-manager.py` |
| Project Ports | `.ports.env` (in each project) |
| Claude Config | `CLAUDE.md` (in each project) |
| Global Claude | `~/.claude/CLAUDE.md` |

## 🔧 Intelligent Port Ranges

### Development Environment
| Service Type | Port Range | Examples |
|-------------|------------|----------|
| Web/Frontend | 3000-3999 | React (3000), Vue (3001) |
| API/Backend | 4000-4999 | REST (4000), GraphQL (4001) |
| PostgreSQL | 5432-5499 | Postgres (5432) |
| MySQL | 3306-3399 | MySQL (3306) |
| MongoDB | 27017-27099 | MongoDB (27017) |
| Redis/Cache | 6379-6399 | Redis (6379) |
| RabbitMQ | 5672-5699 | RabbitMQ (5672) |
| Kafka | 9092-9099 | Kafka (9092) |
| Elasticsearch | 9200-9299 | Elastic (9200) |
| Monitoring | 9090-9099 | Prometheus (9090) |
| Temporal | 7233-7299 | Temporal (7233) |

### Staging Environment
Add 10000 to development ports (e.g., Web: 13000-13999)

### Production Environment
Uses standard ports (80, 443, 5432, etc.)

## 🚨 Common Issues & Fixes

### Port Already in Use
```bash
# Find what's using port
lsof -i :8080

# Free the port
port-manager free 8080
```

### Line Ending Issues (Windows/WSL)
```bash
# Fix script line endings
dos2unix script.sh

# Fix all scripts
find . -name "*.sh" -exec dos2unix {} \;
```

### Permission Denied
```bash
# Make script executable
chmod +x script.sh
```

### Doppler Not Found
```bash
# Install Doppler
curl -Ls https://cli.doppler.com/install.sh | sh

# Setup project
doppler setup --project PROJECT --config dev
```

## 🔐 Environment Management

### Doppler (Recommended)
```bash
# Run with secrets
doppler run -- npm start
doppler run -- make run

# Check secrets
doppler secrets

# Download to .env (dev only!)
doppler secrets download --no-file --format env > .env
```

### Docker Integration
```yaml
# docker-compose.yml
services:
  web:
    ports:
      - "${WEB_PORT:-8000}:8000"
```

### Makefile Integration
```makefile
include .ports.env
export

run:
	python app.py --port $${API_PORT}
```

## 📝 Creating New Project

```bash
# 1. Create project directory
mkdir my-project && cd my-project

# 2. Initialize Git
git init

# 3. Setup Claude templates
~/workspace/.claude-templates/project-setup.sh

# 4. Initialize ports
port-manager init

# 5. Setup Doppler
doppler setup --project my-project --config dev

# 6. Create CLAUDE.md
cp ~/.claude-templates/CLAUDE.md ./CLAUDE.md
# Edit to customize for your project
```

## 🎯 Best Practices

1. **Always check ports before starting services**
2. **Use Doppler for all secrets**
3. **Keep CLAUDE.md updated**
4. **Use .ports.env for all port configs**
5. **Run dos2unix on scripts from Windows**
6. **Use lean commands for consistency**

## 🆘 Help Commands

```bash
# Claude help
claude --help

# Port manager help
port-manager --help

# Lean help
lean --help

# View this cheat sheet
cat ~/.claude-templates/CHEAT_SHEET.md
```

---
*Quick reference for Claude Templates System v1.0*