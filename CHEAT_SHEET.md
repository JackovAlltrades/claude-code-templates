# 🚀 Claude Templates System - Quick Reference

## 🎯 Quick Commands

### Port Management
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

## 🔧 Port Ranges

| Service Type | Port Range | Example |
|-------------|------------|---------|
| Web/Frontend | 8000-8099 | 8000, 8001 |
| API/Backend | 8100-8199 | 8100, 8101 |
| Databases | 5400-5499 | 5432 (Postgres) |
| Cache/Redis | 6300-6399 | 6379 (Redis) |
| Message Queue | 4200-4299 | 4222 (NATS) |
| Monitoring | 9000-9099 | 9000 (Metrics) |
| Documentation | 3000-3099 | 3000 (Docs) |
| Workflow | 7200-7299 | 7233 (Temporal) |
| Testing | 4400-4499 | 4444 (Selenium) |

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