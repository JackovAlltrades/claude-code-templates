# Universal Port Manager for Claude

## Quick Reference for Claude

When starting work on a project, I should:

1. **Check available ports**:
   ```bash
   python ~/.claude-templates/scripts/port-manager.py status
   ```

2. **Initialize project ports**:
   ```bash
   python ~/.claude-templates/scripts/port-manager.py init .
   ```

3. **Use assigned ports from `.ports.env`**:
   ```bash
   source .ports.env
   echo "Web server will run on port: $WEB_PORT"
   echo "API server will run on port: $API_PORT"
   ```

## Port Ranges by Service Type

| Service Type | Port Range | Purpose |
|-------------|------------|---------|
| web         | 8000-8099  | Frontend web servers |
| api         | 8100-8199  | Backend APIs |
| db          | 5400-5499  | Databases |
| cache       | 6300-6399  | Redis/Memcached |
| queue       | 5670-5680  | RabbitMQ/NATS |
| monitoring  | 9000-9099  | Prometheus/Grafana |
| temporal    | 7230-7239  | Temporal services |
| misc        | 3000-3099  | Other services |

## Common Commands I Should Use

### When setting up a new service:
```bash
# Check what's available
python ~/.claude-templates/scripts/port-manager.py status

# Get next available port for service type
PORT=$(python ~/.claude-templates/scripts/port-manager.py get-port --type web)
echo "Using port: $PORT"
```

### When there's a port conflict:
```bash
# See what's using a port
lsof -i :8080

# Free up the port
python ~/.claude-templates/scripts/port-manager.py free 8080
```

### For Docker Compose projects:
```yaml
# Use environment variables from .ports.env
version: '3.8'
services:
  web:
    ports:
      - "${WEB_PORT:-8000}:8000"
  api:
    ports:
      - "${API_PORT:-8080}:8080"
```

### For Node.js projects:
```json
{
  "scripts": {
    "start": "PORT=${WEB_PORT:-3000} node server.js",
    "dev": "PORT=${WEB_PORT:-3000} nodemon server.js"
  }
}
```

### For Python projects:
```python
import os
from dotenv import load_dotenv

# Load port configuration
load_dotenv('.ports.env')

PORT = int(os.getenv('API_PORT', 8000))
app.run(host='0.0.0.0', port=PORT)
```

## Integration with CLAUDE.md

Add this to project's CLAUDE.md:

```markdown
## Port Configuration

This project uses Universal Port Manager. Ports are defined in `.ports.env`:

- Web UI: ${WEB_PORT}
- API: ${API_PORT}
- Database: ${DB_PORT}
- Redis: ${REDIS_PORT}

To check port availability: `make check-ports`
```

## Makefile Integration

Add to project Makefile:

```makefile
# Port management
check-ports:
	@python ~/.claude-templates/scripts/port-manager.py status
	@echo "Project ports:"
	@cat .ports.env 2>/dev/null || echo "No .ports.env file found"

init-ports:
	@python ~/.claude-templates/scripts/port-manager.py init .

free-port:
	@read -p "Enter port to free: " port; \
	python ~/.claude-templates/scripts/port-manager.py free $$port

# Include ports in environment
-include .ports.env
export
```

## Best Practices

1. **Always check first**: Before hardcoding any port, check availability
2. **Use .ports.env**: Source this file in all scripts and services
3. **Document in CLAUDE.md**: List all ports used by the project
4. **Clean up**: When project is done, run cleanup command
5. **Prefer environment variables**: Never hardcode ports in source code

## Example Workflow

When Claude starts a new web project:

```bash
# 1. Initialize ports for the project
$ python ~/.claude-templates/scripts/port-manager.py init .
✓ Created .ports.env with:
  web: 8003
  api: 8103
  db: 5432
  redis: 6379

# 2. Use in docker-compose.yml
services:
  frontend:
    ports:
      - "${WEB_PORT}:3000"
  backend:
    ports:
      - "${API_PORT}:8000"

# 3. Document in CLAUDE.md
"This project runs on:
- Frontend: http://localhost:${WEB_PORT}
- Backend API: http://localhost:${API_PORT}"

# 4. Check status anytime
$ python ~/.claude-templates/scripts/port-manager.py show myproject
```

## Auto-Detection Rules

The port manager scans for:
1. `docker-compose*.yml` files
2. `package.json` scripts
3. `.env*` files (excluding .example)
4. `Makefile` port references
5. Running processes
6. Docker containers

## Emergency Commands

```bash
# Kill all processes on common dev ports
for port in 3000 8000 8080 5000; do
  lsof -ti:$port | xargs kill -9 2>/dev/null
done

# Reset port registry
rm -rf ~/.config/universal-port-manager/registry.json
python ~/.claude-templates/scripts/port-manager.py init
```