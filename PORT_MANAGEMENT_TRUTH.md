# Universal Port Management - Single Source of Truth

## Purpose
Eliminate "Address already in use" errors forever by providing a centralized port management system for all development projects.

## Core Components

### 1. Port Manager Script
**Location**: `~/.claude-templates/scripts/port-manager.py`
**Purpose**: Central registry and management of all project ports
**Registry**: `~/.config/port-manager/registry.json`

### 2. Project Port Configuration
**File**: `.ports.env` (per project)
**Format**: Environment variables (KEY=PORT)
**Example**:
```bash
WEB_PORT=8000
API_PORT=8100
DB_PORT=5400
REDIS_PORT=6300
```

### 3. Port Ranges by Service Type

| Service | Range | Description |
|---------|-------|-------------|
| web | 8000-8099 | Frontend web servers |
| api | 8100-8199 | Backend APIs |
| db | 5400-5499 | Databases |
| cache | 6300-6399 | Redis/Memcached |
| queue | 5670-5680 | Message queues |
| monitoring | 9000-9099 | Metrics/monitoring |
| temporal | 7230-7239 | Temporal services |
| misc | 3000-3099 | Other services |

## Workflow

### For New Projects

1. **Initialize Ports** (MANDATORY FIRST STEP)
   ```bash
   cd my-project
   python3 ~/.claude-templates/scripts/port-manager.py init .
   ```

2. **Source Port Configuration**
   ```bash
   source .ports.env
   ```

3. **Use Environment Variables** (NEVER hardcode)
   ```javascript
   const port = process.env.WEB_PORT || 8000;
   ```

### For Existing Projects

1. **Check for `.ports.env`**
   - If exists: `source .ports.env`
   - If missing: Run init (step 1 above)

2. **Verify No Conflicts**
   ```bash
   make check-ports  # or
   python3 ~/.claude-templates/scripts/port-manager.py status
   ```

## Integration Patterns

### Makefile Integration
```makefile
# Always include at top
-include .ports.env
export

# Add standard targets
check-ports:
	@python3 ~/.claude-templates/scripts/port-manager.py show

init-ports:
	@python3 ~/.claude-templates/scripts/port-manager.py init .
```

### Docker Compose Integration
```yaml
services:
  web:
    ports:
      - "${WEB_PORT:-8000}:8000"
    environment:
      - PORT=${WEB_PORT}
```

### Package.json Integration
```json
{
  "scripts": {
    "dev": "PORT=$WEB_PORT node server.js",
    "start": "PORT=$WEB_PORT NODE_ENV=production node server.js"
  }
}
```

### Python Integration
```python
import os
from pathlib import Path

# Load ports automatically
ports_file = Path('.ports.env')
if ports_file.exists():
    from dotenv import load_dotenv
    load_dotenv(ports_file)

PORT = int(os.getenv('API_PORT', 8080))
```

## Troubleshooting

### Port Already in Use
```bash
# Option 1: Free the port
python3 ~/.claude-templates/scripts/port-manager.py free 8080

# Option 2: Check what's using it
lsof -i :8080

# Option 3: Get alternative port
python3 ~/.claude-templates/scripts/port-manager.py get-port --type web
```

### Missing .ports.env
```bash
# Regenerate it
python3 ~/.claude-templates/scripts/port-manager.py init .
```

### Port Not in Registry
```bash
# Clean up dead entries
python3 ~/.claude-templates/scripts/port-manager.py clean

# Re-initialize
python3 ~/.claude-templates/scripts/port-manager.py init .
```

## Best Practices

### DO ✅
- Run `init` for EVERY new project
- Use environment variables from `.ports.env`
- Include `.ports.env` in `.gitignore`
- Create `.ports.env.example` for team
- Check ports before starting services
- Document special port requirements

### DON'T ❌
- Hardcode ports in source code
- Edit `.ports.env` manually
- Commit `.ports.env` to git
- Skip port initialization
- Use random ports without checking
- Ignore port conflicts

## Commands Reference

| Command | Description |
|---------|-------------|
| `init [path]` | Initialize ports for project |
| `status` | Show all registered ports |
| `show [project]` | Show ports for specific project |
| `free <port>` | Kill process using port |
| `get-port --type <type>` | Get next available port |
| `clean` | Remove dead port entries |

## File Locations

- **Script**: `~/.claude-templates/scripts/port-manager.py`
- **Registry**: `~/.config/port-manager/registry.json`
- **Project Ports**: `./.ports.env` (each project)
- **Documentation**: This file

## Updates & Maintenance

- Registry auto-cleans dead ports
- Projects persist until manually removed
- Port assignments are stable (same project = same ports)

---
*This is the single source of truth for Universal Port Management*
*Last Updated: ${DATE}*