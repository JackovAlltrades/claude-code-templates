#!/bin/bash
# Lean API initialization script using OpenAPI template

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Lean API Initialization${NC}"
echo "================================"

# Initialize port management FIRST
echo -e "${BLUE}Initializing port management...${NC}"
python3 ~/.claude-templates/scripts/port-manager.py init . > /dev/null 2>&1
source .ports.env

# Get project details
read -p "Project name: " PROJECT_NAME
read -p "Project description: " PROJECT_DESCRIPTION
read -p "Domain (e.g., example.com): " DOMAIN

# Use API_PORT from port manager
PORT=${API_PORT:-8080}
echo -e "${GREEN}✓ Using port $PORT for API (from .ports.env)${NC}"

# Create API directory structure
echo -e "\n${YELLOW}Creating API structure...${NC}"
mkdir -p api/v1/{routers,schemas,services,tests}
mkdir -p docs
mkdir -p .spectral

# Generate OpenAPI spec from template
echo -e "${YELLOW}Generating OpenAPI specification...${NC}"
cat /home/bjhorn/workspace/.claude-templates/openapi-lean.yaml | \
  sed "s/\${PROJECT_NAME}/$PROJECT_NAME/g" | \
  sed "s/\${PROJECT_DESCRIPTION}/$PROJECT_DESCRIPTION/g" | \
  sed "s/\${DOMAIN}/$DOMAIN/g" | \
  sed "s/\${PORT:-8000}/$PORT/g" > api/v1/openapi.yaml

# Create Spectral configuration
echo -e "${YELLOW}Setting up API linting...${NC}"
cat > .spectral.yml << 'EOF'
extends:
  - spectral:oas
  - spectral:asyncapi

rules:
  # Custom rules for your project
  operation-id-pattern:
    description: Operation IDs must follow our naming convention
    given: "$.paths[*][*].operationId"
    severity: error
    then:
      function: pattern
      functionOptions:
        match: "^(get|list|create|update|delete|validate|export|import)[A-Z].*"
        
  x-terminology-required:
    description: Must document terminology choices
    given: "$.info"
    severity: warn
    then:
      field: "x-terminology"
      function: truthy
EOF

# Create API validation Makefile targets
echo -e "${YELLOW}Adding API targets to Makefile...${NC}"
if [ -f "Makefile" ]; then
    echo "" >> Makefile
else
    echo "include /home/bjhorn/workspace/.claude-templates/Makefile.lean" > Makefile
    echo "" >> Makefile
fi

cat >> Makefile << 'EOF'

## API Commands
.PHONY: api-validate api-docs api-generate api-serve

api-validate: ## Validate OpenAPI specification
	@echo "🔍 Validating OpenAPI spec..."
	@npx @stoplight/spectral-cli lint api/v1/openapi.yaml

api-docs: ## Generate API documentation
	@echo "📚 Generating API documentation..."
	@npx @redocly/openapi-cli build-docs api/v1/openapi.yaml -o docs/api.html
	@echo "✅ Documentation generated at docs/api.html"

api-generate: api-validate ## Generate API code from OpenAPI spec
	@echo "🏗️ Generating API code..."
	@openapi-generator generate -i api/v1/openapi.yaml -g python-fastapi -o api/v1/generated
	@echo "✅ API code generated"

api-serve: ## Serve API documentation locally
	@echo "🌐 Serving API docs at http://localhost:8080"
	@python -m http.server 8080 --directory docs
EOF

# Create initial FastAPI app
echo -e "${YELLOW}Creating FastAPI application...${NC}"
cat > api/v1/main.py << 'EOF'
"""
Generated API using Lean OpenAPI standards
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml

# Load OpenAPI spec
with open("api/v1/openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

app = FastAPI(
    title=openapi_spec["info"]["title"],
    version=openapi_spec["info"]["version"],
    description=openapi_spec["info"]["description"],
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
# from .routers import resources

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": openapi_spec["info"]["title"],
        "version": openapi_spec["info"]["version"],
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
EOF

# Create git hooks for API validation
echo -e "${YELLOW}Setting up git hooks...${NC}"
mkdir -p .git/hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Validate OpenAPI spec before commit

if [ -f "api/v1/openapi.yaml" ]; then
    echo "🔍 Validating OpenAPI spec..."
    npx @stoplight/spectral-cli lint api/v1/openapi.yaml
    if [ $? -ne 0 ]; then
        echo "❌ OpenAPI validation failed. Please fix errors before committing."
        exit 1
    fi
fi
EOF
chmod +x .git/hooks/pre-commit

# Create README section
echo -e "${YELLOW}Updating README...${NC}"
cat >> README.md << EOF

## API Documentation

This project follows OpenAPI 3.1 standards for API design.

### Quick Start

\`\`\`bash
# Validate API specification
make api-validate

# Generate API documentation
make api-docs

# Generate API code
make api-generate

# Serve docs locally
make api-serve
\`\`\`

### API Design Principles

- **Resource-based URLs**: Use plural nouns (/resources, not /resource)
- **Operation naming**: Use verbs in operationIds (getResource, not resource)
- **Consistency**: Single source of truth in \`api/v1/openapi.yaml\`
- **Validation**: Automated via git hooks and CI/CD

### Terminology

See \`x-terminology\` in the OpenAPI spec for project-specific naming conventions.
EOF

echo -e "\n${GREEN}✅ Lean API structure initialized!${NC}"
echo -e "\nNext steps:"
echo "1. Edit api/v1/openapi.yaml to define your API"
echo "2. Run 'make api-validate' to check your spec"
echo "3. Run 'make api-generate' to generate code"
echo "4. Run 'make api-docs' to generate documentation"