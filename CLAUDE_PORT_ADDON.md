# Port Management System

## 🚨 IMPORTANT: Check Ports Before Starting Any Service

Before running any service, I must check port availability:

```bash
# Quick status check
~/.claude-templates/scripts/port-manager.py status

# Initialize this project's ports
~/.claude-templates/scripts/port-manager.py init .
```

## Current Project Ports

To see this project's assigned ports:
```bash
cat .ports.env
```

## When I Need a Port

1. **For a new service**: Check `.ports.env` first
2. **If not listed**: Get next available:
   ```bash
   ~/.claude-templates/scripts/port-manager.py get-port --type web
   ```
3. **If port conflict**: Free it up:
   ```bash
   ~/.claude-templates/scripts/port-manager.py free 8080
   ```

## Integration Examples

### Docker Compose
```yaml
services:
  web:
    ports:
      - "${WEB_PORT:-8000}:8000"
```

### Makefile
```makefile
include .ports.env
export

run-web:
	python -m http.server $${WEB_PORT}

run-api:
	uvicorn main:app --port $${API_PORT}
```

### Node.js
```javascript
const port = process.env.WEB_PORT || 3000;
```

### Python
```python
import os
port = int(os.getenv('API_PORT', 8000))
```

## Port Conflict Resolution

If I encounter "Address already in use":
1. Check what's using it: `lsof -i :PORT`
2. Free it: `~/.claude-templates/scripts/port-manager.py free PORT`
3. Or get alternative: `~/.claude-templates/scripts/port-manager.py get-port --type SERVICE_TYPE`

## Service Type Ranges

- `web`: 8000-8099 (frontends)
- `api`: 8100-8199 (backends)
- `db`: 5400-5499 (databases)
- `cache`: 6300-6399 (Redis/Memcached)
- `misc`: 3000-3099 (other services)