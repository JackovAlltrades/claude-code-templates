# {name} - LLM Memory System

**Purpose**: Single source of truth for LLMs working on {name}. This file provides context, patterns, best practices, and project-specific knowledge that persists across sessions.

**Last Updated**: {datetime}
**Project Template**: {template}

## Project Overview

**Name**: {name}
**Description**: {name} - Managed by Project Truth System
**Tech Stack**: See technology section below
**Key Features**: Project Truth, Lean Six Sigma, Single Source of Truth

## Code Philosophy

### Core Principles
1. **Clarity over Cleverness**: Write code that is easy to understand, not just efficient
2. **Fail Fast, Recover Gracefully**: Detect issues early, handle them elegantly
3. **Test-Driven Truth**: Tests document intended behavior and catch regressions
4. **Single Source of Truth**: One authoritative location for each piece of information
5. **Continuous Improvement**: Regular refactoring guided by metrics and feedback

### Design Patterns
- **Repository Pattern**: Abstraction between data layer and business logic
- **Factory Pattern**: Consistent object creation with validation
- **Observer Pattern**: Event-driven architecture for loose coupling
- **Strategy Pattern**: Interchangeable algorithms for flexibility
- **Command Pattern**: Encapsulated requests for undo/redo and queuing

## Warp Rules (Fast Development)

### 1. **Two-Pizza Teams**
- Teams small enough to be fed by two pizzas
- Clear ownership and accountability
- Fast decision making

### 2. **Ship Small, Ship Often**
- Daily deployments preferred
- Feature flags for gradual rollout
- Rollback capability within 5 minutes

### 3. **Automate Everything**
- CI/CD pipeline for all changes
- Automated testing (unit, integration, e2e)
- Automated security scanning
- Automated dependency updates

### 4. **Measure What Matters**
- Performance metrics (p50, p95, p99)
- Business metrics (conversion, retention)
- Developer metrics (cycle time, MTTR)
- Quality metrics (test coverage, defect rate)

### 5. **Document as Code**
- README.md always current
- API documentation auto-generated
- Architecture decisions recorded (ADRs)
- This CLAUDE.md file as living documentation

## Project Commands & Patterns

### Core Commands
```bash
# Check project status
lean truth update project
lean ops quality measure

# Run tests
lean test unit
lean test integration

# Deploy
lean deploy prod --blue-green
```

### Project-Specific Patterns
Project uses standard patterns from {template} template

## Critical Project Decisions

### Architecture Decisions
- Decision: Use {template} template architecture
- Rationale: Best practices for this project type
- Date: {datetime}

### Technology Choices
- Primary stack based on {template} template
- Additional technologies as needed

## Code Organization
```
src/
├── core/           # Core business logic
├── modules/        # Feature modules
├── templates/      # Reusable templates
└── utils/          # Utility functions
tests/
├── unit/           # Unit tests
└── integration/    # Integration tests
docs/
├── api/            # API documentation
├── architecture/   # Architecture decisions
└── guides/         # User guides
```

## Key Files & Their Purpose

- `README.md`: Project documentation and quick start
- `CLAUDE.md`: LLM memory and context (this file)
- `PROJECT_TRUTH.md`: Single source of truth for project metrics
- `.github/workflows/`: CI/CD pipeline definitions
- `docker-compose.yml`: Local development environment
- `requirements.txt` / `package.json`: Dependency management

## Common Tasks

### For New Features
1. Update PROJECT_TRUTH.md with decision
2. Create feature branch following naming convention
3. Write tests first (TDD approach)
4. Implement with code philosophy in mind
5. Update documentation inline
6. Submit PR with Truth compliance check

### For Bug Fixes
1. Reproduce issue with failing test
2. Create bugfix branch
3. Fix bug following warp rules
4. Verify fix doesn't break existing tests
5. Submit PR with root cause analysis

### For Performance Optimization
1. Measure baseline performance
2. Identify bottlenecks with profiling
3. Implement optimization
4. Measure improvement
5. Document in PROJECT_TRUTH.md

### For Testing
1. Run unit tests: `lean test unit`
2. Run integration tests: `lean test integration`
3. Check coverage: `lean test coverage`
4. Fix any failures before proceeding

## Dependency Management

### ⚠️ CRITICAL: Python Virtual Environment (venv)
**ALWAYS check for and use virtual environment before installing Python packages!**

#### Virtual Environment Commands
```bash
# Check if venv exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ No virtual environment found - CREATE ONE FIRST!"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Verify you're in venv (should show venv path)
which python

# Install packages ONLY after activation
pip install -r requirements.txt
```

#### Mistake-Proofing Rules
1. **NEVER use `sudo pip install`** - This installs globally!
2. **ALWAYS activate venv first** - Check with `which python`
3. **Create `.gitignore` entry** - Add `venv/` to avoid committing
4. **Use `pip freeze > requirements.txt`** - Keep dependencies tracked
5. **Check before every Python command** - Make it a habit!

### 🦀 Rust Development (Cargo)
**ALWAYS check workspace and target directory!**

#### Rust Commands
```bash
# Check if in a Rust project
ls Cargo.toml || echo "❌ Not in a Rust project root!"

# Build in release mode for performance testing
cargo build --release

# Run tests (includes doc tests!)
cargo test

# Update dependencies safely
cargo update --dry-run  # Preview updates first
cargo update

# Check for security vulnerabilities
cargo audit

# Format and lint
cargo fmt -- --check  # Check formatting
cargo clippy -- -D warnings  # Lint with warnings as errors
```

#### Rust Mistake-Proofing
1. **NEVER commit `/target/`** - Build artifacts (huge!)
2. **ALWAYS run `cargo fmt` before commit** - Consistent style
3. **Use `cargo check` for fast compilation** - Faster than build
4. **Lock dependencies** - Commit `Cargo.lock` for apps
5. **Use workspace** - Share dependencies in monorepos

### 🐹 Go Development (Go Modules)
**ALWAYS verify module path and Go version!**

#### Go Commands
```bash
# Check Go environment
go env GOPATH
go env GOMODULE

# Initialize module (only once per project!)
go mod init github.com/org/project

# Download dependencies
go mod download

# Add missing and remove unused modules
go mod tidy

# Verify dependencies
go mod verify

# Run tests with coverage
go test -v -cover ./...

# Build with version info
go build -ldflags="-X main.version=$(git rev-parse --short HEAD)"
```

#### Go Mistake-Proofing
1. **NEVER commit `vendor/` unless required** - Use go.mod
2. **ALWAYS run `go mod tidy`** - Clean dependencies
3. **Use `go vet` before commit** - Catch bugs
4. **Set GOPRIVATE for private repos** - Avoid public proxy
5. **Check `go.sum`** - Commit for reproducible builds

### 📦 Node.js/TypeScript Development
**ALWAYS check package manager (npm vs yarn vs pnpm)!**

#### Node.js Commands
```bash
# Check which package manager is used
if [ -f "yarn.lock" ]; then
    echo "📦 Using Yarn"
elif [ -f "pnpm-lock.yaml" ]; then
    echo "📦 Using PNPM"
else
    echo "📦 Using NPM"
fi

# Install dependencies (right way)
npm ci          # Use lockfile (faster, safer than npm install)
yarn install --frozen-lockfile
pnpm install --frozen-lockfile

# Add dependencies correctly
npm install --save package-name        # Runtime
npm install --save-dev package-name    # Dev only

# Security audit
npm audit
npm audit fix  # Be careful - test after!

# Check for outdated packages
npm outdated
```

#### Node.js Mistake-Proofing
1. **NEVER commit `node_modules/`** - Use package.json
2. **PREFER `npm ci` over `npm install`** - Respects lockfile
3. **Don't mix package managers** - Pick one per project
4. **Use exact versions for critical deps** - No surprises
5. **Run `npm audit` regularly** - Security matters

### 🐋 Docker Development
**ALWAYS use .dockerignore!**

#### Docker Best Practices
```bash
# Check what you're about to build
cat .dockerignore || echo "⚠️ No .dockerignore found!"

# Build with proper tags
docker build -t project:$(git rev-parse --short HEAD) .
docker build -t project:latest .

# Multi-stage builds for smaller images
# Use specific base image versions
FROM python:3.11-slim AS builder  # Not just 'python:latest'

# Security scan images
docker scan image-name
```

#### Docker Mistake-Proofing
1. **NEVER include secrets in images** - Use runtime env
2. **ALWAYS use .dockerignore** - Exclude build artifacts
3. **Pin base image versions** - Reproducible builds
4. **Use multi-stage builds** - Smaller final images
5. **Run as non-root user** - Security best practice

### Core Dependencies
- Dependencies from {template} template
- Additional project-specific dependencies

### Security Policy
- Automated vulnerability scanning
- Weekly dependency updates
- Manual review for major version changes

### Check Dependencies
```bash
# Check for vulnerabilities
lean ops security scan

# Update dependencies
lean deps update --safe
```

### Common Dependency Issues
- Document issues as they arise
- Include resolution steps

## Testing & Quality

### Test Strategy
1. **Unit Tests**: 80% minimum coverage
2. **Integration Tests**: Critical paths covered
3. **E2E Tests**: User journeys validated
4. **Performance Tests**: Load and stress testing
5. **Security Tests**: OWASP compliance

### Test Commands
```bash
# Run all tests
lean test all

# Run specific test suite
lean test unit src/core/
lean test integration api/

# Run with coverage
lean test coverage --html
```

### Quality Standards
- Code coverage minimum: 80%
- Linting rules: Project-specific .eslintrc / .flake8
- Type checking: Enabled for all new code
- Review requirements: 2 approvals minimum
- Performance budgets: Page load < 3s, API response < 200ms

## Error Patterns & Solutions

### Common Errors (Torvalds' Wisdom)
#### 1. **Bad Abstractions**
- **Problem**: Over-engineering simple solutions
- **Solution**: "Good taste" means using the simplest approach that works
- **Example**: Avoid 10 layers of indirection for a simple data fetch

#### 2. **Ignoring Edge Cases**
- **Problem**: Code works in happy path but fails in production
- **Solution**: "Think about the impossible" - handle all cases explicitly
- **Example**: Always check for null, empty arrays, network failures

#### 3. **Poor Error Messages**
- **Problem**: Generic "Error occurred" messages
- **Solution**: "Be explicit about what went wrong and why"
- **Example**: "Failed to connect to database 'users' at host:port - timeout after 30s"

#### 4. **Memory Management Issues**
- **Problem**: Leaks, inefficient allocation
- **Solution**: "Know your data structures" - choose the right tool
- **Example**: Use object pools for frequently allocated objects

#### 5. **Concurrency Bugs**
- **Problem**: Race conditions, deadlocks
- **Solution**: "Avoid shared state" - use message passing
- **Example**: Implement actor model or use channels instead of mutexes

### Error Handling Strategy
1. Log errors with context
2. Return meaningful error messages
3. Implement circuit breakers for external services
4. Use retry logic with exponential backoff
5. Monitor error rates and alert on anomalies

## Team Conventions

### Naming Conventions
- **Variables**: camelCase (JS) / snake_case (Python)
- **Functions**: Verb + Noun (e.g., `getUserData`)
- **Classes**: PascalCase, singular nouns
- **Constants**: UPPER_SNAKE_CASE
- **Files**: kebab-case for URLs, snake_case for modules

### Git Workflow
1. Feature branches from `develop`
2. Branch naming: `feature/ticket-short-description`
3. Commits: Conventional commits (feat:, fix:, docs:, etc.)
4. PR with description template
5. Squash and merge to maintain clean history

### Code Review Process
1. Self-review checklist first
2. Automated tests must pass
3. Security scan must pass
4. Two approvals required
5. Address all feedback
6. Update PROJECT_TRUTH.md if needed

### Communication
- Daily standups at 9 AM
- Slack for quick questions
- GitHub discussions for technical decisions
- Weekly retrospectives

## Integration Points

### External Services (Nielsen's UX Integration)
#### Service Integration Principles
1. **Visibility of System Status**: Always show service health
2. **Match Between System and Real World**: Use domain language
3. **User Control and Freedom**: Allow service toggling/fallbacks
4. **Consistency and Standards**: Uniform API patterns
5. **Error Prevention**: Validate before external calls
6. **Recognition Rather Than Recall**: Clear service documentation
7. **Flexibility and Efficiency**: Support both simple and advanced use
8. **Aesthetic and Minimalist Design**: Clean API interfaces
9. **Help Users Recognize Errors**: Detailed integration logs
10. **Help and Documentation**: Service-specific guides

### APIs (RESTful Best Practices)
#### Endpoint Design
```yaml
# Resource-oriented design
GET    /api/v1/users          # List users
POST   /api/v1/users          # Create user
GET    /api/v1/users/{id}     # Get user
PUT    /api/v1/users/{id}     # Update user
DELETE /api/v1/users/{id}     # Delete user

# Query parameters for filtering
GET /api/v1/users?status=active&role=admin

# Pagination
GET /api/v1/users?page=2&limit=20

# Sorting
GET /api/v1/users?sort=created_at:desc

# Field selection
GET /api/v1/users?fields=id,name,email
```

#### API Versioning Strategy
- URL versioning: `/api/v1/`, `/api/v2/`
- Deprecation notices: 6-month warning
- Backward compatibility: 1 year minimum

### Webhooks (Event-Driven Architecture)
#### Webhook Security (Schneier's Principles)
1. **Defense in Depth**: Multiple security layers
   - HMAC signature validation
   - IP whitelist
   - Rate limiting
   - Request replay prevention

2. **Principle of Least Privilege**: Minimal webhook permissions
   - Read-only by default
   - Scoped to specific resources
   - Time-limited tokens

3. **Audit Everything**: Complete webhook logs
   - All attempts (success/failure)
   - Payload hashes
   - Response times
   - Consumer identification

#### Webhook Configuration
```json
{
  "url": "https://example.com/webhooks/receive",
  "events": ["user.created", "order.completed"],
  "secret": "webhook_secret_key",
  "retry": {
    "max_attempts": 3,
    "backoff": "exponential",
    "timeout": 30
  }
}
```

## Performance Considerations

### Optimization Guidelines
1. Profile before optimizing
2. Focus on user-perceived performance
3. Use caching strategically
4. Implement pagination for large datasets
5. Use CDN for static assets

### Performance Budget
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- API Response Time: < 200ms (p95)
- Database Query Time: < 50ms (p95)

### Monitoring
- APM: Track performance metrics
- Logs: Centralized logging with search
- Metrics: Custom dashboards for KPIs
- Alerts: PagerDuty integration

## Security Practices

### Security Checklist
- [ ] No hardcoded secrets (use environment variables)
- [ ] Input validation on all endpoints
- [ ] Authentication required for protected routes
- [ ] Authorization checks at service layer
- [ ] Audit logging for sensitive operations
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] Security headers enabled
- [ ] Dependencies regularly updated
- [ ] Penetration testing scheduled

### Sensitive Data Locations
- `.env` files (never commit)
- `config/secrets/` directory
- Database connection strings
- API keys and tokens
- User PII

### 🔐 Secrets Management Mistake-Proofing
**CRITICAL: Never commit secrets to Git!**

#### Pre-commit Checks
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Basic .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-yaml
      - id: end-of-file-fixer
EOF
```

#### Environment Variables Best Practices
```bash
# Check for accidental .env commit
git ls-files | grep -E '\.env$' && echo "⚠️ WARNING: .env in git!"

# Use template files
cp .env.example .env  # Never commit actual .env

# For different environments
.env.development
.env.staging
.env.production
.env.local  # Local overrides

# Load env vars safely
set -a  # Export all vars
source .env
set +a  # Stop exporting
```

### 🗄️ Database Migration Mistake-Proofing
**ALWAYS backup before migrations!**

#### Safe Migration Practices
```bash
# Python (Alembic/Django)
alembic current  # Check current version
alembic check    # Verify migration integrity
alembic upgrade --sql  # Preview SQL first!
alembic upgrade head

# Node.js (Prisma/TypeORM)
npx prisma migrate status
npx prisma migrate dev --create-only  # Review first
npx prisma migrate dev

# Rollback plan
alembic downgrade -1  # Go back one version
alembic history      # See all versions
```

### 🧪 Testing Mistake-Proofing
**NEVER skip tests to save time!**

#### Test Organization
```bash
# Check test coverage before commit
pytest --cov=src --cov-report=term-missing
go test -cover ./...
cargo tarpaulin
npm test -- --coverage

# Separate test databases
TEST_DATABASE_URL=postgresql://localhost/myapp_test
DATABASE_URL=postgresql://localhost/myapp_dev

# Clean test state
pytest --fixtures  # List available fixtures
pytest -vv -s     # Verbose output for debugging
```

### 📝 Git Workflow Mistake-Proofing
**ALWAYS check what you're committing!**

#### Safe Git Practices
```bash
# Review changes before commit
git diff --staged
git diff --staged --name-only  # Just filenames

# Interactive staging (pick specific changes)
git add -p

# Amend without changing message
git commit --amend --no-edit

# Check file size before commit
find . -type f -size +5M | grep -v "\.git"

# Undo accidental commits (before push!)
git reset --soft HEAD~1  # Keep changes staged
git reset HEAD~1        # Keep changes unstaged
```

### Security Tools
- SAST: Static analysis in CI/CD
- DAST: Dynamic analysis in staging
- Dependency scanning: Daily automated checks
- Secret scanning: Pre-commit hooks

## Development Environment Setup

### 🐳 Docker vs Local Development
**IMPORTANT**: Projects may use a hybrid approach:

#### Common Services in Docker
- Databases (PostgreSQL, MySQL, MongoDB)
- Caches (Redis, Dragonfly, Memcached)
- Message Queues (RabbitMQ, Kafka, NATS)
- Search Engines (Elasticsearch, MeiliSearch)
- Workflow Engines (Temporal, Airflow)

#### Typically Running Locally (with venv)
- Application code (Backend API, Frontend)
- Scripts and tools
- Development servers
- Test runners

#### Key Development Commands
```bash
# Start Docker services (check docker-compose.yml first!)
docker compose up -d

# For Python development (ALWAYS DO THIS!)
source venv/bin/activate
cd [project_directory]
pip install -r requirements.txt

# Check what's running where
docker ps                    # Docker services
lsof -i :8000               # Local services
```

### ☸️ Kubernetes Mistake-Proofing
**ALWAYS know which context you're in!**

#### Context Safety
```bash
# Check current context BEFORE any kubectl command
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Safe context switching
kubectl config use-context staging
kubectl config use-context production  # ⚠️ DANGER!

# Namespace safety
kubectl config set-context --current --namespace=my-namespace

# Dry run everything first!
kubectl apply --dry-run=client -f deployment.yaml
kubectl delete --dry-run=client -f deployment.yaml
```

#### K8s Best Practices
```bash
# Resource limits (prevent cluster destruction)
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# Liveness/Readiness probes (prevent bad deploys)
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

# Rolling updates (safe deployments)
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### 🚀 CI/CD Pipeline Mistake-Proofing
**NEVER skip stages or tests!**

#### Pipeline Safety Gates
```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    npm test
    if [ $? -ne 0 ]; then
      echo "❌ Tests failed - stopping pipeline"
      exit 1
    fi

# Require manual approval for production
- name: Wait for approval
  uses: trstringer/manual-approval@v1
  if: github.ref == 'refs/heads/main'
  with:
    approvers: senior-dev-team
```

## Deployment

### Environments
1. **Development**: Local docker-compose + venv
2. **Staging**: Mirrors production, used for QA
3. **Production**: Blue-green deployment ready

### CI/CD Pipeline
1. Code push triggers pipeline
2. Install dependencies
3. Run linting and type checking
4. Run all tests with coverage
5. Security scanning
6. Build artifacts
7. Deploy to staging
8. Run smoke tests
9. Manual approval for production
10. Deploy to production
11. Run health checks
12. Monitor for 30 minutes

### Rollback Strategy
- Automated rollback on health check failure
- Manual rollback available via CLI
- Database migrations must be backward compatible
- Feature flags for gradual rollout

## Troubleshooting Guide

### Debug Commands
```bash
# Check application health
lean ops health check

# View recent logs
lean logs tail -n 100

# Check database connection
lean db health

# Run diagnostics
lean debug diagnose
```

### Common Issues
1. **Connection timeouts**: Check network and firewall rules
2. **Memory leaks**: Enable heap dumps and analyze
3. **Slow queries**: Check query plans and indexes
4. **High CPU**: Profile and identify hot paths

### Log Locations
- Application logs: `/var/log/app/`
- Error logs: `/var/log/app/error.log`
- Access logs: `/var/log/app/access.log`
- System logs: `journalctl -u app-name`

## Project-Specific Context

### Business Logic (Lean Six Sigma SIPOC)
#### SIPOC Analysis Template
```yaml
Suppliers:
  - User Input: Form submissions, API requests
  - External APIs: Payment processors, email services
  - Database: Persistent storage
  - Cache: Performance optimization

Inputs:
  - User Data: Registration, preferences
  - Business Rules: Validation, calculations
  - Configuration: Environment settings

Process:
  - Validate: Input sanitization
  - Transform: Business logic application
  - Persist: Data storage
  - Respond: Result delivery

Outputs:
  - API Responses: JSON/XML data
  - UI Updates: Real-time changes
  - Notifications: Email/SMS/Push
  - Reports: Analytics data

Customers:
  - End Users: Primary consumers
  - Admin Users: System managers
  - API Consumers: Third-party integrations
  - Analytics: Business intelligence
```

### Domain Terminology (Ubiquitous Language)
#### Core Domain Terms
```yaml
# User Domain
User: Person with system account
Role: Permission grouping (admin, user, viewer)
Permission: Specific action allowance
Session: Active user connection

# Business Domain
Entity: Core business object
Aggregate: Related entity cluster
Repository: Data access layer
Service: Business logic container

# Technical Domain
Endpoint: API access point
Middleware: Request processor
Handler: Request responder
Worker: Background processor
```

### User Personas (Nielsen's User-Centered Design)
#### Primary Personas
1. **Developer Dana**
   - Goal: Quick project setup and deployment
   - Pain Points: Complex configurations, poor documentation
   - Needs: Clear examples, automated tools, good defaults

2. **Manager Mike**
   - Goal: Project visibility and control
   - Pain Points: Lack of metrics, unclear status
   - Needs: Dashboards, reports, notifications

3. **Admin Alice**
   - Goal: System stability and security
   - Pain Points: Hidden issues, security vulnerabilities
   - Needs: Monitoring, alerts, audit logs

4. **User Uma**
   - Goal: Complete tasks efficiently
   - Pain Points: Slow performance, confusing UI
   - Needs: Fast response, clear navigation

## Current State & TODOs

### Active Work
- Current sprint goals
- In-progress features
- Blocked items

### Known Issues
- Technical debt items
- Bug backlog
- Performance bottlenecks

### Technical Debt
- Refactoring needs
- Deprecated dependencies
- Legacy code to update

## Memory Extensions

### Short-term Memory (Session)
- Current branch: {current_branch}
- Recent changes: {recent_changes}
- Active TODOs: {active_todos}

### Long-term Memory (Persistent)
- Project patterns and conventions
- Team decisions and rationale
- Error solutions and workarounds
- Performance benchmarks and trends

## AI/LLM Guidelines

### When Working on This Project
1. Always read this file first
2. Check PROJECT_TRUTH.md for latest metrics
3. Review recent commits for context
4. Follow code philosophy and warp rules
5. Update this file after significant changes

### AI Assistance Best Practices
1. **Check Virtual Environment FIRST**: Always verify venv is active before any Python work
2. **Context First**: Provide relevant code context
3. **Explain Intent**: Describe what you're trying to achieve
4. **Iterative Refinement**: Start simple, iterate to complex
5. **Verify Output**: Always test AI-generated code
6. **Document Changes**: Update relevant documentation

### Python-Specific Checklist for AI
- [ ] Is there a `venv` directory? If not, create it!
- [ ] Is venv activated? Check with `which python`
- [ ] Are we in the right directory? Backend vs scripts vs services
- [ ] Should we use project-specific requirements.txt?
- [ ] Did we update requirements.txt after installing new packages?

### Do's and Don'ts
**DO:**
- Read CLAUDE.md and PROJECT_TRUTH.md first
- ALWAYS check for and activate venv before Python work
- Follow established patterns and conventions
- Write tests for new functionality
- Update documentation as you code
- Ask for clarification when unsure
- Run `pip freeze > requirements.txt` after adding packages

**DON'T:**
- NEVER use `sudo pip install` or install packages globally
- NEVER install Python packages without activating venv first
- Make assumptions about business logic
- Skip tests to save time
- Ignore linting warnings
- Commit sensitive data
- Break existing functionality
- Commit `venv/` directory to git

---
*This file is the single source of truth for LLMs working on {name}.*
*Generated by Universal Scaffolder's LLM Memory System.*
*Update after significant changes or decisions.*