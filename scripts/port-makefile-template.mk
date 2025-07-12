# Intelligent Port Management for Makefile
# Include this in your project Makefile: include scripts/port-makefile-template.mk

# Port management commands
INTELLIGENT_PORT_MANAGER := python3 scripts/intelligent-port-manager.py
PROJECT_NAME := $(shell basename $(CURDIR))
ENVIRONMENT ?= development

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m

# Load existing port allocations
-include .ports.$(ENVIRONMENT).env
export

# Port management targets
.PHONY: port-allocate port-release port-status port-sync port-export port-check

## Allocate ports for all services
port-allocate:
	@echo "$(YELLOW)🔍 Allocating ports for $(PROJECT_NAME)...$(NC)"
	@# Allocate web port if not set
	@if [ -z "$(WEB_PORT)" ]; then \
		$(INTELLIGENT_PORT_MANAGER) allocate $(PROJECT_NAME)-web --type web --env $(ENVIRONMENT) --project $(PROJECT_NAME); \
	fi
	@# Allocate API port if not set
	@if [ -z "$(API_PORT)" ]; then \
		$(INTELLIGENT_PORT_MANAGER) allocate $(PROJECT_NAME)-api --type api --env $(ENVIRONMENT) --project $(PROJECT_NAME); \
	fi
	@# Allocate database port if not set
	@if [ -z "$(DB_PORT)" ]; then \
		$(INTELLIGENT_PORT_MANAGER) allocate $(PROJECT_NAME)-db --type database --env $(ENVIRONMENT) --project $(PROJECT_NAME); \
	fi
	@# Allocate Redis port if not set
	@if [ -z "$(REDIS_PORT)" ]; then \
		$(INTELLIGENT_PORT_MANAGER) allocate $(PROJECT_NAME)-redis --type database --env $(ENVIRONMENT) --project $(PROJECT_NAME); \
	fi
	@# Generate environment file
	@$(INTELLIGENT_PORT_MANAGER) generate-env $(PROJECT_NAME) --env $(ENVIRONMENT)
	@echo "$(GREEN)✅ Ports allocated and saved to .ports.$(ENVIRONMENT).env$(NC)"

## Release all allocated ports
port-release:
	@echo "$(YELLOW)🔓 Releasing ports for $(PROJECT_NAME)...$(NC)"
	@if [ -f .ports.$(ENVIRONMENT).env ]; then \
		grep '_PORT=' .ports.$(ENVIRONMENT).env | cut -d'=' -f2 | while read port; do \
			$(INTELLIGENT_PORT_MANAGER) release $$port; \
		done; \
	fi
	@echo "$(GREEN)✅ All ports released$(NC)"

## Show port status
port-status:
	@$(INTELLIGENT_PORT_MANAGER) status

## Sync port registry
port-sync:
	@echo "$(YELLOW)🔄 Syncing port registry...$(NC)"
	@$(INTELLIGENT_PORT_MANAGER) sync

## Export port configuration
port-export:
	@$(INTELLIGENT_PORT_MANAGER) generate-env $(PROJECT_NAME) --env $(ENVIRONMENT)

## Check if required ports are available
port-check:
	@echo "$(YELLOW)🔍 Checking port availability...$(NC)"
	@AVAILABLE=true; \
	if [ -f .ports.$(ENVIRONMENT).env ]; then \
		grep '_PORT=' .ports.$(ENVIRONMENT).env | while read line; do \
			VAR=$$(echo $$line | cut -d'=' -f1); \
			PORT=$$(echo $$line | cut -d'=' -f2); \
			if lsof -i :$$PORT >/dev/null 2>&1; then \
				echo "$(RED)❌ Port $$PORT ($$VAR) is already in use$(NC)"; \
				AVAILABLE=false; \
			else \
				echo "$(GREEN)✅ Port $$PORT ($$VAR) is available$(NC)"; \
			fi; \
		done; \
	else \
		echo "$(YELLOW)⚠️  No port configuration found. Run 'make port-allocate' first.$(NC)"; \
		AVAILABLE=false; \
	fi; \
	if [ "$$AVAILABLE" = "false" ]; then exit 1; fi

# Enhanced run commands with automatic port allocation
.PHONY: run-web run-api run-db run-all

## Run web service with auto port allocation
run-web: port-check
	@if [ -z "$(WEB_PORT)" ]; then \
		echo "$(YELLOW)Allocating web port...$(NC)"; \
		$(MAKE) port-allocate; \
		$(MAKE) port-export; \
		include .ports.$(ENVIRONMENT).env; \
	fi
	@echo "$(GREEN)🚀 Starting web service on port $(WEB_PORT)$(NC)"
	@# Your web service start command here
	@# Example: PORT=$(WEB_PORT) npm start

## Run API service with auto port allocation
run-api: port-check
	@if [ -z "$(API_PORT)" ]; then \
		echo "$(YELLOW)Allocating API port...$(NC)"; \
		$(MAKE) port-allocate; \
		$(MAKE) port-export; \
		include .ports.$(ENVIRONMENT).env; \
	fi
	@echo "$(GREEN)🚀 Starting API service on port $(API_PORT)$(NC)"
	@# Your API service start command here
	@# Example: uvicorn main:app --port $(API_PORT)

## Run database with auto port allocation
run-db: port-check
	@if [ -z "$(DB_PORT)" ]; then \
		echo "$(YELLOW)Allocating database port...$(NC)"; \
		$(MAKE) port-allocate; \
		$(MAKE) port-export; \
		include .ports.$(ENVIRONMENT).env; \
	fi
	@echo "$(GREEN)🚀 Starting database on port $(DB_PORT)$(NC)"
	@# Your database start command here
	@# Example: docker run -p $(DB_PORT):5432 postgres

## Run all services
run-all: port-allocate port-check
	@echo "$(GREEN)🚀 Starting all services...$(NC)"
	@$(MAKE) -j3 run-web run-api run-db

# Docker compose integration
.PHONY: docker-up docker-down

## Start docker services with port allocation
docker-up: port-allocate
	@echo "$(GREEN)🐳 Starting Docker services with allocated ports...$(NC)"
	@docker-compose --env-file .ports.$(ENVIRONMENT).env up -d

## Stop docker services and sync ports
docker-down:
	@echo "$(YELLOW)🐳 Stopping Docker services...$(NC)"
	@docker-compose down
	@$(MAKE) port-sync

# Development workflow helpers
.PHONY: dev-start dev-stop dev-restart

## Start development environment
dev-start: port-allocate port-check docker-up
	@echo "$(GREEN)✅ Development environment started$(NC)"
	@$(MAKE) port-status

## Stop development environment
dev-stop: docker-down port-release
	@echo "$(GREEN)✅ Development environment stopped$(NC)"

## Restart development environment
dev-restart: dev-stop dev-start

# Port information helpers
.PHONY: port-info port-ranges port-llm

## Show detailed port information
port-info:
	@echo "$(YELLOW)📋 Port Configuration for $(PROJECT_NAME) ($(ENVIRONMENT))$(NC)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@if [ -f .ports.$(ENVIRONMENT).env ]; then \
		cat .ports.$(ENVIRONMENT).env | grep -v '^#' | grep '_PORT='; \
	else \
		echo "No port configuration found."; \
	fi
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

## Show available port ranges
port-ranges:
	@$(INTELLIGENT_PORT_MANAGER) ranges

## Export port data for LLM
port-llm:
	@$(INTELLIGENT_PORT_MANAGER) export-llm

# Help target
.PHONY: port-help

## Show port management help
port-help:
	@echo "$(YELLOW)🔌 Intelligent Port Management Commands$(NC)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  $(GREEN)make port-allocate$(NC)  - Allocate ports for all services"
	@echo "  $(GREEN)make port-release$(NC)   - Release all allocated ports"
	@echo "  $(GREEN)make port-status$(NC)    - Show current port allocations"
	@echo "  $(GREEN)make port-sync$(NC)      - Sync registry with actual usage"
	@echo "  $(GREEN)make port-check$(NC)     - Check if ports are available"
	@echo "  $(GREEN)make port-info$(NC)      - Show project port configuration"
	@echo "  $(GREEN)make port-ranges$(NC)    - Show standard port ranges"
	@echo "  $(GREEN)make port-llm$(NC)       - Export port data for LLM"
	@echo ""
	@echo "  $(GREEN)make dev-start$(NC)      - Start dev environment with ports"
	@echo "  $(GREEN)make dev-stop$(NC)       - Stop dev environment and release"
	@echo "  $(GREEN)make dev-restart$(NC)    - Restart dev environment"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"