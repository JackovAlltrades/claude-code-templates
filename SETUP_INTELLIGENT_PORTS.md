# 🚀 Setting Up Intelligent Port Management System

This guide will help you set up the automatic intelligent port management system that:
- Automatically allocates ports based on service type
- Prevents port conflicts across all projects
- Tracks port lifecycle from development to production
- Integrates seamlessly with your workflow

## Prerequisites

- Python 3.7+
- Linux/WSL/macOS environment
- Basic understanding of ports and services

## Quick Setup (5 minutes)

### 1. Clone Claude Templates

```bash
# If you haven't already
cd ~/workspace
git clone https://github.com/YOUR_USERNAME/claude-templates.git .claude-templates
```

### 2. Run the Intelligent Setup Script

```bash
cd ~/.claude-templates
./setup-intelligent-ports.sh
```

This script will:
- Install required Python packages
- Copy intelligent port scripts to your system
- Add shell hooks to your bashrc/zshrc
- Set up the port registry
- Configure your first project

### 3. Activate in Current Shell

```bash
source ~/.bashrc
# or
source ~/.zshrc
```

## Manual Setup (If Automatic Fails)

### Step 1: Install Dependencies

```bash
pip3 install click rich pyyaml
```

### Step 2: Copy Scripts

```bash
# Create scripts directory
mkdir -p ~/.local/bin

# Copy intelligent port manager scripts
cp ~/.claude-templates/scripts/intelligent-port-manager.py ~/.local/bin/
cp ~/.claude-templates/scripts/port-lifecycle-manager.py ~/.local/bin/
chmod +x ~/.local/bin/intelligent-port-manager.py
chmod +x ~/.local/bin/port-lifecycle-manager.py

# Ensure ~/.local/bin is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Step 3: Add Shell Hooks

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
# Intelligent Port Management Hooks
if [ -f ~/.claude-templates/scripts/port-hooks.sh ]; then
    source ~/.claude-templates/scripts/port-hooks.sh
    # Enable by default
    export PORT_HOOKS_ENABLED=true
fi

# Convenient aliases
alias ipm='python3 ~/.local/bin/intelligent-port-manager.py'
alias plm='python3 ~/.local/bin/port-lifecycle-manager.py'
```

### Step 4: Initialize Port Registry

```bash
# Create config directory
mkdir -p ~/.config/intelligent-port-manager
mkdir -p ~/.config/port-lifecycle

# Initialize global registry
cat > ~/.config/intelligent-port-manager/port-registry.json << EOF
{
  "ports": {},
  "services": {},
  "environments": {},
  "updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
```

## Project Setup

### For New Projects

```bash
# 1. Create project
mkdir my-awesome-project && cd my-awesome-project

# 2. Copy intelligent scripts
mkdir -p scripts
cp ~/.claude-templates/scripts/intelligent-port-manager.py scripts/
cp ~/.claude-templates/scripts/port-lifecycle-manager.py scripts/
cp ~/.claude-templates/scripts/port-makefile-template.mk scripts/

# 3. Initialize intelligent ports
python3 scripts/intelligent-port-manager.py allocate $(basename $PWD)-web --type web
python3 scripts/intelligent-port-manager.py allocate $(basename $PWD)-api --type api
python3 scripts/intelligent-port-manager.py allocate $(basename $PWD)-db --type database

# 4. Generate environment file
python3 scripts/intelligent-port-manager.py generate-env $(basename $PWD)
```

### For Existing Projects

```bash
cd your-existing-project

# 1. Add intelligent port management
mkdir -p scripts
cp ~/.claude-templates/scripts/intelligent-port-manager.py scripts/

# 2. Import existing ports (if any)
if [ -f .ports.env ]; then
    # Parse existing ports and register them
    while IFS='=' read -r key value; do
        if [[ $key == *_PORT ]]; then
            service_name=$(echo $key | sed 's/_PORT$//' | tr '[:upper:]' '[:lower:]')
            python3 scripts/intelligent-port-manager.py allocate $service_name --port $value
        fi
    done < .ports.env
fi

# 3. Or start fresh
python3 scripts/intelligent-port-manager.py generate-env $(basename $PWD)
```

## Makefile Integration

Add to your project's Makefile:

```makefile
# Intelligent Port Management
-include scripts/port-makefile-template.mk

# Or add manually:
.PHONY: ports-allocate ports-status ports-sync

ports-allocate:
	@python3 scripts/intelligent-port-manager.py allocate $(shell basename $(CURDIR))-web --type web
	@python3 scripts/intelligent-port-manager.py allocate $(shell basename $(CURDIR))-api --type api
	@python3 scripts/intelligent-port-manager.py generate-env $(shell basename $(CURDIR))

ports-status:
	@python3 scripts/intelligent-port-manager.py status

ports-sync:
	@python3 scripts/intelligent-port-manager.py sync

# Include generated ports
-include .ports.development.env
export
```

## Docker Compose Integration

Update your `docker-compose.yml`:

```yaml
version: '3.8'

# Load port configuration
env_file:
  - .ports.${ENVIRONMENT:-development}.env

services:
  web:
    build: .
    ports:
      - "${WEB_PORT}:${WEB_PORT}"
    environment:
      - PORT=${WEB_PORT}

  api:
    build: ./api
    ports:
      - "${API_PORT}:${API_PORT}"
    environment:
      - PORT=${API_PORT}

  postgres:
    image: postgres:15
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
```

## Team Setup

### For Team Leaders

1. **Set Up Central Configuration**:
```bash
# Create team port allocation strategy
cat > team-port-config.json << EOF
{
  "team": "my-team",
  "projects": {
    "frontend": {"base_port": 3000, "range": [3000, 3099]},
    "backend": {"base_port": 4000, "range": [4000, 4099]},
    "services": {"base_port": 5000, "range": [5000, 5999]}
  }
}
EOF
```

2. **Create Team Setup Script**:
```bash
cat > setup-team-ports.sh << 'EOF'
#!/bin/bash
# Team Port Management Setup

echo "Setting up Intelligent Port Management for team..."

# Install for all team members
for member in alice bob charlie; do
    echo "Setting up for $member..."
    ssh $member@dev-server << 'REMOTE'
        # Install dependencies
        pip3 install --user click rich pyyaml
        
        # Get scripts
        git clone https://github.com/TEAM/claude-templates.git ~/.claude-templates
        
        # Run setup
        ~/.claude-templates/setup-intelligent-ports.sh
REMOTE
done
EOF
chmod +x setup-team-ports.sh
```

### For Team Members

Just run:
```bash
# One-line setup
curl -sSL https://your-team-url/setup-intelligent-ports.sh | bash

# Or if you have the repo
~/.claude-templates/setup-intelligent-ports.sh
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy with Intelligent Ports
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Port Manager
        run: |
          pip install click rich pyyaml
          chmod +x scripts/intelligent-port-manager.py
      
      - name: Allocate Ports
        run: |
          ./scripts/intelligent-port-manager.py allocate ${{ github.event.repository.name }}-web --type web --env staging
          ./scripts/intelligent-port-manager.py allocate ${{ github.event.repository.name }}-api --type api --env staging
          ./scripts/intelligent-port-manager.py generate-env ${{ github.event.repository.name }} --env staging
      
      - name: Deploy
        run: |
          source .ports.staging.env
          docker-compose up -d
```

### GitLab CI

```yaml
stages:
  - setup
  - deploy

setup_ports:
  stage: setup
  script:
    - pip3 install click rich pyyaml
    - python3 scripts/intelligent-port-manager.py allocate $CI_PROJECT_NAME --env $CI_ENVIRONMENT_NAME
    - python3 scripts/intelligent-port-manager.py generate-env $CI_PROJECT_NAME --env $CI_ENVIRONMENT_NAME
  artifacts:
    paths:
      - .ports.*.env
```

## Verification

After setup, verify everything works:

```bash
# 1. Check if hooks are loaded
port-hooks status
# Should show: "Port hooks are enabled"

# 2. Test automatic allocation
cd /tmp && mkdir test-project && cd test-project
npm init -y
npm start
# Should automatically allocate a port

# 3. Check intelligent status
ipm status
# Should show allocated ports

# 4. Test lifecycle management
plm init test-service api test-project
plm status
# Should show lifecycle status
```

## Troubleshooting

### Issue: Command not found

```bash
# Ensure scripts are in PATH
export PATH="$HOME/.local/bin:$PATH"

# Or use full path
python3 ~/.local/bin/intelligent-port-manager.py status
```

### Issue: Hooks not working

```bash
# Re-source hooks
source ~/.claude-templates/scripts/port-hooks.sh

# Check if enabled
echo $PORT_HOOKS_ENABLED  # Should be "true"

# Enable manually
port-hooks on
```

### Issue: Permission denied

```bash
# Make scripts executable
chmod +x ~/.local/bin/intelligent-port-manager.py
chmod +x ~/.local/bin/port-lifecycle-manager.py
chmod +x ~/.claude-templates/scripts/port-hooks.sh
```

### Issue: Python packages missing

```bash
# Install with user flag
pip3 install --user click rich pyyaml

# Or use virtual environment
python3 -m venv ~/.port-manager-venv
source ~/.port-manager-venv/bin/activate
pip install click rich pyyaml
```

## Best Practices

1. **Always use descriptive service names** - Helps with automatic type detection
2. **Run sync regularly** - Keeps registry clean
3. **Check before deploying** - Use `ipm status` to see what's allocated
4. **Use lifecycle management** - Track ports through environments
5. **Export for team** - Share port allocations via `ipm export-llm`

## Next Steps

1. Set up for all your projects
2. Configure your CI/CD pipelines
3. Train your team on the commands
4. Customize port ranges for your needs
5. Integrate with your deployment tools

---

*Intelligent Port Management Setup Guide v1.0*
*Part of Claude Templates System*