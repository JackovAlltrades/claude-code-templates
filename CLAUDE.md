# ${PROJECT_NAME} - LLM Memory System

**Purpose**: Single source of truth for LLMs working on ${PROJECT_NAME}. This file provides context, patterns, best practices, and project-specific knowledge that persists across sessions.

**Last Updated**: ${DATE}
**Project Type**: ${PROJECT_TYPE}

## Project Overview

**Name**: ${PROJECT_NAME}
**Description**: ${PROJECT_DESCRIPTION}
**Tech Stack**: ${TECH_STACK}
**Key Features**: ${KEY_FEATURES}

## Port Configuration 🚨 IMPORTANT

This project uses Universal Port Manager. All ports are defined in `.ports.env`:
- Web UI: ${WEB_PORT}
- API: ${API_PORT}
- Database: ${DB_PORT}
- Redis/Cache: ${REDIS_PORT}
- Docs: ${DOCS_PORT}

**Before starting ANY service**:
```bash
# Check port availability
make check-ports

# Or directly:
python3 ~/.claude-templates/scripts/port-manager.py status

# Source ports for shell
source .ports.env
```

## Code Philosophy

### Core Principles
1. **Clarity over Cleverness**: Write code that is easy to understand
2. **Fail Fast, Recover Gracefully**: Detect issues early, handle them elegantly
3. **Test-Driven Truth**: Tests document intended behavior
4. **Single Source of Truth**: One authoritative location for each piece of information
5. **Continuous Improvement**: Regular refactoring guided by metrics

### Design Patterns
- **Repository Pattern**: Abstraction between data layer and business logic
- **Factory Pattern**: Consistent object creation with validation
- **Observer Pattern**: Event-driven architecture
- **Strategy Pattern**: Interchangeable algorithms
- **Command Pattern**: Encapsulated requests

## Project Commands

### Port Management
```bash
# Initialize ports for project
make init-ports

# Check port conflicts
make check-ports

# Free a specific port
make free-port
```

### Development
```bash
# Start services (uses .ports.env)
make dev

# Run tests
make test

# Check code quality
make lint

# Update project truth
lean truth update project
```

## Project Structure
```
.
├── .ports.env          # Port assignments (DO NOT EDIT MANUALLY)
├── CLAUDE.md           # This file - LLM memory
├── README.md           # Human-readable documentation
├── Makefile            # Project commands
└── src/                # Source code
```

## Key Files & Their Purpose

- `.ports.env`: Auto-generated port configuration from Universal Port Manager
- `CLAUDE.md`: LLM memory and context (this file)
- `Makefile`: Standardized commands with port integration
- `.env.example`: Example environment variables (never commit real .env)

## Common Tasks

### Starting a New Feature
1. Check port availability: `make check-ports`
2. Create feature branch
3. Write tests first
4. Implement feature
5. Update documentation
6. Submit PR

### Debugging Port Conflicts
```bash
# See what's using a port
lsof -i :8080

# Free the port
python3 ~/.claude-templates/scripts/port-manager.py free 8080

# Or get an alternative port
python3 ~/.claude-templates/scripts/port-manager.py get-port --type web
```

## Integration Points

### Docker Integration
```yaml
# docker-compose.yml
services:
  web:
    ports:
      - "${WEB_PORT:-8000}:8000"
    environment:
      - PORT=${WEB_PORT}
```

### Node.js Integration
```javascript
// Use port from environment
const port = process.env.WEB_PORT || 8000;
```

### Python Integration
```python
import os
from dotenv import load_dotenv

load_dotenv('.ports.env')
port = int(os.getenv('API_PORT', 8080))
```

## Error Patterns & Solutions

### Port Already in Use
**Problem**: "Error: Address already in use"
**Solution**: 
1. Run `make check-ports` to see conflicts
2. Run `make free-port` to kill process
3. Or use different port from `.ports.env`

### Missing Port Configuration
**Problem**: Service starts on wrong port
**Solution**: 
1. Ensure `.ports.env` exists: `make init-ports`
2. Source it: `source .ports.env`
3. Use environment variables, not hardcoded ports

## Team Conventions

### Port Usage
- **NEVER hardcode ports** in source code
- **ALWAYS use `.ports.env`** environment variables
- **CHECK availability** before starting services
- **DOCUMENT** any special port requirements

### Git Workflow
1. Feature branches from `main`
2. Include `.ports.env` in `.gitignore`
3. Commit `.ports.env.example` with defaults

## Recent Changes
- ${DATE}: Project initialized with Universal Port Manager

## AI/LLM Guidelines

When working on this project:
1. **Always check `.ports.env`** before running services
2. **Use environment variables** for all port references
3. **Run `make check-ports`** if you see port conflicts
4. **Update this file** when adding new services

---
*This file is the single source of truth for LLMs working on ${PROJECT_NAME}*
*Generated from Claude Templates*