# 🧠 Intelligent Port Management Guide

## Overview

The Intelligent Port Management System is an advanced evolution of the basic port manager that automatically:
- Detects service types from names
- Assigns ports from industry-standard ranges
- Tracks port lifecycle from development to production
- Integrates with your development workflow
- Provides LLM-friendly data export

## Quick Start

### 1. Enable Intelligent Port Management

```bash
# Add to your ~/.bashrc
source ~/.claude-templates/scripts/port-hooks.sh

# Or activate manually in any project
source ~/.claude-templates/scripts/port-hooks.sh
port-hooks on
```

### 2. Automatic Port Allocation

With hooks enabled, ports are allocated automatically:

```bash
# These commands auto-allocate appropriate ports:
docker-compose up    # Allocates ports for all services
npm start           # Allocates web port (3000-3999)
yarn dev            # Allocates web port
python3 app.py      # Allocates API port (4000-4999)
```

### 3. Manual Allocation

```bash
# Allocate specific service type
python3 scripts/intelligent-port-manager.py allocate my-api --type api

# Auto-detect type from name
python3 scripts/intelligent-port-manager.py allocate my-postgres-db
# Automatically detects "database" type and assigns from 5432-5499
```

## Service Type Detection

The system intelligently detects service types from names:

| Name Contains | Detected Type | Port Range |
|--------------|---------------|------------|
| web, ui, frontend, react, vue | web | 3000-3999 |
| api, rest, graphql, backend | api | 4000-4999 |
| postgres, pg | database | 5432-5499 |
| mysql, maria | database | 3306-3399 |
| mongo, mongodb | database | 27017-27099 |
| redis, cache | cache | 6379-6399 |
| rabbitmq, amqp, queue | messaging | 5672-5699 |
| kafka | messaging | 9092-9099 |
| elastic, search | search | 9200-9299 |
| prometheus, grafana, metrics | monitoring | 9090-9099 |
| temporal, airflow, workflow | workflow | 7233-7299 |
| auth, keycloak, oauth | auth | 8080-8099 |

## Environment-Based Port Management

### Development (Default)
```bash
# Uses standard development ranges
python3 scripts/intelligent-port-manager.py allocate my-api --env development
# Assigns from 4000-4999
```

### Staging
```bash
# Adds 10000 to development ports
python3 scripts/intelligent-port-manager.py allocate my-api --env staging
# Assigns from 14000-14999
```

### Production
```bash
# Uses standard ports (80, 443, etc.)
python3 scripts/intelligent-port-manager.py allocate my-web --env production
# Assigns port 80 or 443
```

## Lifecycle Management

### 1. Initialize Service
```bash
# Start tracking a service through its lifecycle
python3 scripts/port-lifecycle-manager.py init my-api api my-project
```

### 2. Promote Through Stages
```bash
# Development → Testing
python3 scripts/port-lifecycle-manager.py promote my-api my-project development testing

# Testing → Staging
python3 scripts/port-lifecycle-manager.py promote my-api my-project testing staging

# Staging → Production
python3 scripts/port-lifecycle-manager.py promote my-api my-project staging production
```

### 3. View Status
```bash
# See all services and their lifecycle stages
python3 scripts/port-lifecycle-manager.py status

# Example output:
# Service    | Development | Testing | Staging | Production
# my-api     | 🟢 4000    | 🟢 5000 | 🟢 14000| 🔴 443
```

### 4. Export Deployment Configs
```bash
# Generate Docker Compose for staging
python3 scripts/port-lifecycle-manager.py export staging --format docker -o docker-compose.staging.yml

# Generate Kubernetes manifests for production
python3 scripts/port-lifecycle-manager.py export production --format kubernetes -o k8s-prod.yml
```

## Workflow Integration

### Makefile Integration
```makefile
# Include intelligent port management
include ~/.claude-templates/scripts/port-makefile-template.mk

# Now you can use:
make port-allocate   # Allocate all service ports
make port-status     # Show status
make dev-start       # Start with auto-allocation
```

### Docker Compose
```yaml
version: '3.8'
services:
  web:
    ports:
      - "${WEB_PORT:-3000}:3000"
  
  api:
    ports:
      - "${API_PORT:-4000}:4000"
  
  postgres:
    ports:
      - "${DB_PORT:-5432}:5432"
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Allocate Staging Ports
  run: |
    python3 scripts/intelligent-port-manager.py allocate ${{ github.event.repository.name }} --env staging
    python3 scripts/intelligent-port-manager.py generate-env ${{ github.event.repository.name }} --env staging
    
- name: Deploy
  run: |
    source .ports.staging.env
    docker-compose up -d
```

## LLM Integration

### Export Port Data
```bash
# Generate LLM-friendly port data
python3 scripts/intelligent-port-manager.py export-llm

# Output includes:
# - Total ports allocated by type
# - Available port ranges
# - Current allocations with metadata
# - Recommendations for optimization
```

### Example LLM Query Response
```json
{
  "timestamp": "2024-01-11T10:00:00",
  "summary": {
    "total_ports_allocated": 15,
    "by_type": {
      "web": 3,
      "api": 4,
      "database": 5,
      "cache": 2,
      "monitoring": 1
    }
  },
  "available_ranges": {
    "web": [[3003, 3999]],
    "api": [[4005, 4999]],
    "database": {
      "postgres": [[5434, 5499]],
      "mysql": [[3307, 3399]]
    }
  }
}
```

## Shell Hook Commands

When hooks are enabled, these commands are available:

```bash
port-status      # Show allocated ports with service info
port-available   # Show available port ranges by type
port-sync        # Sync registry with actual usage
port-export      # Export current project ports
port-llm         # Export data for LLM
port-hooks on    # Enable automatic allocation
port-hooks off   # Disable automatic allocation
```

## Best Practices

### 1. Naming Conventions
```bash
# Good - type is auto-detected
my-app-web
my-app-api
my-app-postgres
my-app-redis

# Less ideal - requires manual type
frontend
backend
db
```

### 2. Project Organization
```
project/
├── .ports.development.env   # Auto-generated
├── .ports.staging.env      # Auto-generated
├── .ports.production.env   # Auto-generated
├── docker-compose.yml      # Uses ${*_PORT} variables
├── Makefile               # Includes port management
└── scripts/
    ├── intelligent-port-manager.py
    ├── port-hooks.sh
    └── port-lifecycle-manager.py
```

### 3. Regular Maintenance
```bash
# Daily sync to clean up stale entries
python3 scripts/intelligent-port-manager.py sync

# Check for optimization opportunities
python3 scripts/intelligent-port-manager.py export-llm
```

## Troubleshooting

### Port Auto-Allocation Not Working
```bash
# Check hooks are enabled
port-hooks status

# Re-enable if needed
port-hooks on

# Verify by running
echo $PORT_HOOKS_ENABLED  # Should show "true"
```

### Wrong Port Range Assigned
```bash
# Explicitly specify type
python3 scripts/intelligent-port-manager.py allocate my-service --type database

# Check detection logic
python3 scripts/intelligent-port-manager.py ranges
```

### Port Conflicts After Sync
```bash
# Force release stale port
python3 scripts/intelligent-port-manager.py release 8080

# Re-sync
python3 scripts/intelligent-port-manager.py sync
```

## Advanced Configuration

### Custom Service Types
Add to `SERVICE_PORT_RANGES` in `intelligent-port-manager.py`:

```python
"ml_model": {
    "development": (8500, 8599),
    "staging": (18500, 18599),
    "production": (8500, 8500),
    "description": "ML model servers"
}
```

### Multi-Project Setup
```bash
# Set up intelligent port management for all projects
cd ~/workspace
for project in */; do
    cd "$project"
    cp ~/.claude-templates/scripts/intelligent-port-manager.py scripts/
    python3 scripts/intelligent-port-manager.py init
    cd ..
done
```

---

*Intelligent Port Management - Part of Claude Templates System*