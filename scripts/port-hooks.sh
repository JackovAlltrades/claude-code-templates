#!/bin/bash
# Port Management Hooks for Development Workflow
# Automatically tracks port allocation and releases

# Source this file in your shell: source scripts/port-hooks.sh

INTELLIGENT_PORT_MANAGER="python3 $(dirname "${BASH_SOURCE[0]}")/intelligent-port-manager.py"
PORT_HOOKS_ENABLED=${PORT_HOOKS_ENABLED:-true}

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to allocate port before starting a service
allocate_port() {
    local service_name=$1
    local service_type=$2
    local environment=${3:-development}
    local project=$(basename "$(pwd)")
    
    if [ "$PORT_HOOKS_ENABLED" != "true" ]; then
        return
    fi
    
    echo -e "${YELLOW}🔍 Allocating port for $service_name...${NC}"
    
    # Allocate port
    local output=$($INTELLIGENT_PORT_MANAGER allocate "$service_name" --type "$service_type" --env "$environment" --project "$project")
    echo "$output"
    
    # Extract port number
    local port=$(echo "$output" | grep "Allocated port" | grep -oE '[0-9]+' | head -1)
    
    if [ -n "$port" ]; then
        # Export as environment variable
        local var_name="${service_name^^}_PORT"
        var_name=${var_name//-/_}
        export "$var_name=$port"
        echo -e "${GREEN}✅ Exported $var_name=$port${NC}"
        
        # Return the port
        echo "$port"
    else
        echo -e "${RED}❌ Failed to allocate port${NC}"
        return 1
    fi
}

# Function to release port after stopping a service
release_port() {
    local port=$1
    
    if [ "$PORT_HOOKS_ENABLED" != "true" ]; then
        return
    fi
    
    if [ -n "$port" ]; then
        echo -e "${YELLOW}🔓 Releasing port $port...${NC}"
        $INTELLIGENT_PORT_MANAGER release "$port"
    fi
}

# Hook for docker-compose up
docker-compose() {
    if [ "$1" = "up" ] && [ "$PORT_HOOKS_ENABLED" = "true" ]; then
        echo -e "${YELLOW}🐳 Port hook: Checking port allocations...${NC}"
        
        # Sync registry before starting
        $INTELLIGENT_PORT_MANAGER sync
        
        # Extract services from docker-compose.yml
        if [ -f "docker-compose.yml" ]; then
            # Parse services and allocate ports
            local services=$(grep -E '^\s*[a-zA-Z_-]+:' docker-compose.yml | sed 's/://g' | tr -d ' ')
            
            for service in $services; do
                # Skip if port already allocated
                local var_name="${service^^}_PORT"
                var_name=${var_name//-/_}
                
                if [ -z "${!var_name}" ]; then
                    # Detect service type
                    local service_type="web"  # Default
                    
                    if [[ "$service" =~ (postgres|mysql|mongo|redis) ]]; then
                        service_type="database"
                    elif [[ "$service" =~ (api|backend) ]]; then
                        service_type="api"
                    elif [[ "$service" =~ (rabbitmq|kafka|nats) ]]; then
                        service_type="messaging"
                    fi
                    
                    allocate_port "$service" "$service_type"
                fi
            done
        fi
        
        # Show current allocations
        echo -e "${GREEN}📊 Current port allocations:${NC}"
        $INTELLIGENT_PORT_MANAGER status
    fi
    
    # Call original docker-compose
    command docker-compose "$@"
    
    if [ "$1" = "down" ] && [ "$PORT_HOOKS_ENABLED" = "true" ]; then
        echo -e "${YELLOW}🐳 Port hook: Releasing allocated ports...${NC}"
        # Note: Ports will be released on next sync
        $INTELLIGENT_PORT_MANAGER sync
    fi
}

# Hook for npm/yarn commands
npm() {
    if [[ "$1" = "start" || "$1" = "run" ]] && [ "$PORT_HOOKS_ENABLED" = "true" ]; then
        local project=$(basename "$(pwd)")
        
        # Check if PORT is already set
        if [ -z "$PORT" ]; then
            echo -e "${YELLOW}📦 Port hook: Allocating port for npm...${NC}"
            local port=$(allocate_port "$project-web" "web" | tail -1)
            export PORT=$port
        fi
    fi
    
    command npm "$@"
}

yarn() {
    if [[ "$1" = "start" || "$1" = "dev" ]] && [ "$PORT_HOOKS_ENABLED" = "true" ]; then
        local project=$(basename "$(pwd)")
        
        # Check if PORT is already set
        if [ -z "$PORT" ]; then
            echo -e "${YELLOW}📦 Port hook: Allocating port for yarn...${NC}"
            local port=$(allocate_port "$project-web" "web" | tail -1)
            export PORT=$port
        fi
    fi
    
    command yarn "$@"
}

# Hook for Python development servers
python() {
    if [[ "$*" =~ (runserver|uvicorn|gunicorn|flask) ]] && [ "$PORT_HOOKS_ENABLED" = "true" ]; then
        local project=$(basename "$(pwd)")
        
        # Extract port from command if specified
        local cmd_port=$(echo "$*" | grep -oE '(:|--port[= ])[0-9]+' | grep -oE '[0-9]+')
        
        if [ -z "$cmd_port" ] && [ -z "$PORT" ]; then
            echo -e "${YELLOW}🐍 Port hook: Allocating port for Python server...${NC}"
            local port=$(allocate_port "$project-api" "api" | tail -1)
            export PORT=$port
            export API_PORT=$port
        fi
    fi
    
    command python "$@"
}

python3() {
    if [[ "$*" =~ (runserver|uvicorn|gunicorn|flask) ]] && [ "$PORT_HOOKS_ENABLED" = "true" ]; then
        local project=$(basename "$(pwd)")
        
        # Extract port from command if specified
        local cmd_port=$(echo "$*" | grep -oE '(:|--port[= ])[0-9]+' | grep -oE '[0-9]+')
        
        if [ -z "$cmd_port" ] && [ -z "$PORT" ]; then
            echo -e "${YELLOW}🐍 Port hook: Allocating port for Python server...${NC}"
            local port=$(allocate_port "$project-api" "api" | tail -1)
            export PORT=$port
            export API_PORT=$port
        fi
    fi
    
    command python3 "$@"
}

# Function to show port status
port-status() {
    $INTELLIGENT_PORT_MANAGER status
}

# Function to show available ports
port-available() {
    $INTELLIGENT_PORT_MANAGER ranges
}

# Function to sync ports
port-sync() {
    echo -e "${YELLOW}🔄 Syncing port registry...${NC}"
    $INTELLIGENT_PORT_MANAGER sync
}

# Function to export ports for current project
port-export() {
    local project=$(basename "$(pwd)")
    local env=${1:-development}
    
    echo -e "${YELLOW}📤 Generating port configuration for $project ($env)...${NC}"
    $INTELLIGENT_PORT_MANAGER generate-env "$project" --env "$env"
}

# Function to get LLM-friendly port data
port-llm() {
    $INTELLIGENT_PORT_MANAGER export-llm
}

# Enable/disable port hooks
port-hooks() {
    case "$1" in
        on|enable)
            export PORT_HOOKS_ENABLED=true
            echo -e "${GREEN}✅ Port hooks enabled${NC}"
            ;;
        off|disable)
            export PORT_HOOKS_ENABLED=false
            echo -e "${YELLOW}⚠️  Port hooks disabled${NC}"
            ;;
        status)
            if [ "$PORT_HOOKS_ENABLED" = "true" ]; then
                echo -e "${GREEN}Port hooks are enabled${NC}"
            else
                echo -e "${YELLOW}Port hooks are disabled${NC}"
            fi
            ;;
        *)
            echo "Usage: port-hooks [on|off|status]"
            ;;
    esac
}

# Add to shell prompt to show allocated ports
update_port_prompt() {
    local port_count=$($INTELLIGENT_PORT_MANAGER status 2>/dev/null | grep -c "🟢")
    if [ "$port_count" -gt 0 ]; then
        echo " [🔌 $port_count]"
    fi
}

# Optional: Add to PS1 (uncomment to enable)
# export PS1="\u@\h:\w\$(update_port_prompt)\$ "

echo -e "${GREEN}🔌 Port management hooks loaded!${NC}"
echo -e "${YELLOW}Commands available:${NC}"
echo "  port-status    - Show allocated ports"
echo "  port-available - Show available port ranges"
echo "  port-sync      - Sync registry with actual usage"
echo "  port-export    - Export ports for current project"
echo "  port-llm       - Export port data for LLM"
echo "  port-hooks     - Enable/disable automatic port allocation"
echo ""
echo -e "${YELLOW}Hooks active for:${NC} docker-compose, npm, yarn, python"
echo -e "${YELLOW}Status:${NC} $([ "$PORT_HOOKS_ENABLED" = "true" ] && echo -e "${GREEN}Enabled${NC}" || echo -e "${RED}Disabled${NC}")"