# 📚 Universal Port Manager - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Integration](#integration)
6. [Troubleshooting](#troubleshooting)
7. [Architecture](#architecture)

## Overview

The Universal Port Manager is a centralized tool for managing ports across all your development projects. It prevents port conflicts, tracks port usage, and provides a consistent interface for port management.

### Key Features
- 🔍 **Port Discovery**: Automatically find available ports
- 📊 **Status Tracking**: See what's using each port
- 🧹 **Cleanup**: Remove dead port registrations
- 🔧 **Integration**: Works with Docker, Make, and more
- 📁 **Project Isolation**: Each project gets its own port space
- 🌐 **System-wide Registry**: Track ports across all projects

## Installation

### Prerequisites
- Python 3.7+
- Click library: `pip install click rich`
- WSL or Linux environment

### Setup Steps

1. **Install Claude Templates**
   ```bash
   cd ~/workspace/.claude-templates
   ./setup.sh
   ```

2. **Add to Bashrc**
   ```bash
   echo 'alias port-manager="python3 ~/.claude-templates/scripts/universal-port-manager.py"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Verify Installation**
   ```bash
   port-manager --help
   ```

## Basic Usage

### 1. Check System Status
```bash
# See all ports in use
port-manager status

# Example output:
#                System Port Status                
# ╭────────┬────────────────┬───────────┬─────────╮
# │ Port   │ Project        │ Service   │ Status  │
# ├────────┼────────────────┼───────────┼─────────┤
# │ 8000   │ my-app         │ web       │ Active  │
# │ 5432   │ my-app         │ db        │ Active  │
# ╰────────┴────────────────┴───────────┴─────────╯
```

### 2. Initialize Project
```bash
# In your project directory
port-manager init

# This creates .ports.env:
# WEB_PORT=8000
# API_PORT=8100
# DB_PORT=5432
# REDIS_PORT=6379
```

### 3. Show Project Ports
```bash
# Show current project's ports
port-manager show

# Show specific project's ports
port-manager show my-project
```

### 4. Free a Port
```bash
# Kill process using port
port-manager free 8080

# Force free (use carefully)
port-manager free 8080 --force
```

### 5. Clean Dead Registrations
```bash
# Remove ports no longer in use
port-manager clean
```

## Advanced Features

### Port Scanning
```bash
# Scan directory for port configurations
port-manager scan

# Finds ports in:
# - docker-compose.yml
# - package.json
# - Makefile
# - .env files
```

### Export Configuration
```bash
# Export as environment variables
port-manager export

# Export as JSON
port-manager export --format json

# Export as YAML
port-manager export --format yaml
```

### Service Type Ranges

The port manager uses predefined ranges for different service types:

| Service Type | Range | Purpose |
|-------------|-------|---------|
| web | 8000-8099 | Frontend applications |
| api | 8100-8199 | Backend APIs |
| db | 5400-5499 | Databases |
| cache | 6300-6399 | Redis, Memcached |
| queue | 4200-4299 | RabbitMQ, NATS |
| search | 9200-9299 | Elasticsearch |
| metrics | 9000-9099 | Prometheus, Grafana |
| docs | 3000-3099 | Documentation |
| proxy | 8800-8899 | Nginx, Traefik |
| workflow | 7200-7299 | Temporal, Airflow |
| ml | 8500-8599 | ML model servers |
| test | 4400-4499 | Test servers |
| dev | 3100-3199 | Development tools |
| misc | 10000-10999 | Everything else |

## Integration

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "${WEB_PORT:-8000}:8000"
    env_file:
      - .ports.env

  api:
    build: ./api
    ports:
      - "${API_PORT:-8100}:8100"
    env_file:
      - .ports.env

  postgres:
    image: postgres:15
    ports:
      - "${DB_PORT:-5432}:5432"
    env_file:
      - .ports.env
```

### Makefile
```makefile
# Include port configuration
include .ports.env
export

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make run-web    - Run web server on port $(WEB_PORT)"
	@echo "  make run-api    - Run API server on port $(API_PORT)"
	@echo "  make check-ports - Check port availability"

# Check ports before running
.PHONY: check-ports
check-ports:
	@port-manager status

# Run services
.PHONY: run-web
run-web: check-ports
	python -m http.server $${WEB_PORT}

.PHONY: run-api
run-api: check-ports
	uvicorn main:app --port $${API_PORT}

.PHONY: run-all
run-all:
	make -j2 run-web run-api
```

### Node.js/Package.json
```json
{
  "name": "my-app",
  "scripts": {
    "start": "PORT=${WEB_PORT:-3000} node server.js",
    "dev": "PORT=${WEB_PORT:-3000} nodemon server.js",
    "check-ports": "port-manager status"
  }
}
```

### Python Application
```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load port configuration
ports_file = Path(".ports.env")
if ports_file.exists():
    load_dotenv(ports_file)

# Use configured ports
WEB_PORT = int(os.getenv("WEB_PORT", 8000))
API_PORT = int(os.getenv("API_PORT", 8100))
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=API_PORT)
```

### Shell Scripts
```bash
#!/bin/bash
# Load port configuration
if [ -f .ports.env ]; then
    export $(cat .ports.env | xargs)
fi

# Use ports
echo "Starting web server on port ${WEB_PORT:-8000}"
python -m http.server ${WEB_PORT:-8000}
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Error: Port 8080 is already in use

# Solution 1: Find what's using it
lsof -i :8080

# Solution 2: Free the port
port-manager free 8080

# Solution 3: Use different port
WEB_PORT=8081 npm start
```

#### 2. Permission Denied
```bash
# Error: Permission denied when killing process

# Solution: Use sudo (carefully)
sudo port-manager free 8080
```

#### 3. Port Not in Registry
```bash
# Error: Port not found in registry

# Solution: Initialize project
port-manager init

# Or manually register
echo "WEB_PORT=8000" >> .ports.env
```

#### 4. Line Ending Issues (Windows/WSL)
```bash
# Error: /usr/bin/env: 'python3\r': No such file or directory

# Solution: Fix line endings
dos2unix ~/.claude-templates/scripts/universal-port-manager.py
```

### Debug Mode
```bash
# Enable verbose output
PORT_MANAGER_DEBUG=1 port-manager status

# Check configuration
port-manager show --debug
```

## Architecture

### Directory Structure
```
~/.config/port-manager/
├── registry.json        # Global port registry
└── projects/           # Project configurations
    ├── project1.json
    └── project2.json

<project>/
├── .ports.env          # Project port configuration
└── .port-manager.yml   # Advanced configuration (optional)
```

### Registry Format
```json
{
  "version": "1.0",
  "ports": {
    "8000": {
      "project": "my-app",
      "service": "web",
      "pid": 12345,
      "started": "2023-07-11T10:00:00Z"
    }
  },
  "projects": {
    "my-app": {
      "path": "/home/user/projects/my-app",
      "ports": {
        "web": 8000,
        "api": 8100,
        "db": 5432
      }
    }
  }
}
```

### Configuration File (.port-manager.yml)
```yaml
# Optional project-specific configuration
project:
  name: my-app
  description: My awesome application

services:
  web:
    port: 8000
    type: web
    healthcheck: http://localhost:8000/health
    
  api:
    port: 8100
    type: api
    depends_on: [db, redis]
    
  db:
    port: 5432
    type: db
    persistent: true

# Custom port ranges
ranges:
  custom:
    start: 9500
    end: 9599
```

## Best Practices

1. **Always Initialize Projects**
   ```bash
   cd new-project
   port-manager init
   ```

2. **Use Environment Files**
   ```bash
   # Development
   .ports.env
   
   # Production (different ports)
   .ports.prod.env
   ```

3. **Check Before Starting**
   ```bash
   # In your start script
   port-manager status || exit 1
   npm start
   ```

4. **Clean Regularly**
   ```bash
   # Add to cron
   0 * * * * port-manager clean
   ```

5. **Document Port Usage**
   ```markdown
   # README.md
   ## Ports
   - Web UI: 8000
   - API: 8100  
   - Database: 5432
   See `.ports.env` for configuration
   ```

## Advanced Topics

### Custom Port Allocation
```python
# Custom allocation script
from universal_port_manager import PortManager

pm = PortManager()

# Get next available port in range
port = pm.get_next_port("web")  # Returns 8001 if 8000 is taken

# Register custom port
pm.register_port(9999, "my-app", "custom-service")
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Setup Ports
  run: |
    pip install click rich
    port-manager init
    port-manager export >> $GITHUB_ENV

- name: Run Tests
  run: |
    npm test
  env:
    PORT: ${{ env.WEB_PORT }}
```

### Multi-Environment Setup
```bash
# Development
ln -s .ports.dev.env .ports.env

# Staging  
ln -s .ports.staging.env .ports.env

# Production
ln -s .ports.prod.env .ports.env
```

---

*Universal Port Manager Guide v1.0 - Part of Claude Templates System*