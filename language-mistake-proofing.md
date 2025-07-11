# Language-Specific Mistake-Proofing Guide

Expert-approved patterns to prevent common mistakes across all major programming languages and tools.

## 🎯 Universal Principles

1. **Check Environment First** - Know where you are before you act
2. **Use Lock Files** - Reproducible builds save debugging time
3. **Never Use Sudo for Package Managers** - Avoid system-wide pollution
4. **Commit Wisely** - Check file sizes, secrets, and generated files
5. **Test Locally First** - Catch issues before CI/CD

## 🐍 Python Mistake-Proofing

### Virtual Environment Checklist
```bash
# BEFORE ANY PYTHON WORK
which python              # Should show venv path
echo $VIRTUAL_ENV        # Should show venv directory
pip --version            # Should reference venv pip

# Common mistakes to avoid
sudo pip install X       # ❌ NEVER! Installs system-wide
pip install X            # ⚠️ Only if venv active
python script.py         # ⚠️ Check 'which python' first
```

### Requirements Management
```bash
# Save exact versions
pip freeze > requirements.txt

# But better: use pip-tools
pip install pip-tools
echo "django>=4.0,<5.0" > requirements.in
pip-compile requirements.in  # Creates requirements.txt with hashes

# For different environments
requirements/
├── base.txt      # Common dependencies
├── dev.txt       # Development only
├── prod.txt      # Production only
└── test.txt      # Testing only
```

## 🦀 Rust Mistake-Proofing

### Workspace Management
```bash
# Check Cargo.toml exists
[[ -f Cargo.toml ]] || echo "❌ Not in a Rust project!"

# Workspace structure for monorepos
[workspace]
members = ["crates/*"]
resolver = "2"  # Use v2 resolver!

# Shared dependencies
[workspace.dependencies]
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
```

### Build & Release
```bash
# Development builds
cargo build              # Debug mode (slow, with symbols)
cargo check             # Fast syntax/type check only

# Release builds
cargo build --release   # Optimized (put in target/release/)
cargo build --profile=release-lto  # With Link Time Optimization

# NEVER commit these
target/                # Build artifacts (can be GBs!)
Cargo.lock            # Only for libraries, commit for apps
```

## 🐹 Go Mistake-Proofing

### Module Management
```bash
# Initialize ONCE per project
go mod init github.com/org/project  # Use proper module path!

# Common module issues
go mod tidy            # Add missing, remove unused
go mod verify          # Check integrity
go mod why package     # Why is this included?

# Private modules
export GOPRIVATE=github.com/mycompany/*
go env -w GOPRIVATE=github.com/mycompany/*
```

### Vendoring Decision
```bash
# When to vendor (commit vendor/)?
# ✅ Enterprise environments with proxy issues
# ✅ Need reproducible builds without module proxy
# ❌ Open source projects (use go.mod/go.sum)

go mod vendor          # Create vendor directory
go build -mod=vendor   # Build using vendor
```

## 📦 Node.js/TypeScript Mistake-Proofing

### Package Manager Consistency
```bash
# Detect and enforce package manager
if [[ -f "yarn.lock" ]]; then
    alias npm="echo '❌ This project uses Yarn!' && false"
elif [[ -f "pnpm-lock.yaml" ]]; then
    alias npm="echo '❌ This project uses PNPM!' && false"
fi

# Lock file best practices
npm ci                 # Use lock file (production)
npm install           # Updates lock file (development)
--save-exact          # Pin exact versions for critical deps
```

### TypeScript Configuration
```json
// tsconfig.json best practices
{
  "compilerOptions": {
    "strict": true,                    // Enable ALL strict checks
    "noUncheckedIndexedAccess": true,  // Catch array[i] undefined
    "noUnusedLocals": true,           // Catch unused variables
    "noUnusedParameters": true,       // Catch unused params
    "exactOptionalPropertyTypes": true // Stricter optional props
  }
}
```

## 🐋 Docker Mistake-Proofing

### Dockerfile Best Practices
```dockerfile
# Always use specific versions
FROM node:18.19-alpine AS builder  # NOT node:latest

# Run as non-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# Multi-stage to reduce size
FROM node:18.19-alpine AS deps
COPY package*.json ./
RUN npm ci --only=production

FROM node:18.19-alpine AS runner
COPY --from=deps /app/node_modules ./node_modules
```

### .dockerignore Essentials
```dockerignore
# MUST HAVE entries
.git
.env*
node_modules
venv
target
*.log
.DS_Store
coverage
.pytest_cache
__pycache__
```

## ☸️ Kubernetes Mistake-Proofing

### Context Safety Script
```bash
# Add to ~/.bashrc or ~/.zshrc
function kubectl() {
    local context=$(command kubectl config current-context 2>/dev/null)
    if [[ "$context" == *"prod"* ]]; then
        echo "⚠️  WARNING: You're in PRODUCTION context: $context"
        echo -n "Are you sure? (yes/no): "
        read answer
        if [[ "$answer" != "yes" ]]; then
            return 1
        fi
    fi
    command kubectl "$@"
}
```

### Resource Limits Template
```yaml
# ALWAYS set resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
    
# Prevent cascading failures
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

## 🔐 Security Mistake-Proofing

### Pre-commit Hook Setup
```yaml
# .pre-commit-config.yaml
repos:
  # Secret detection
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        
  # Security scanning
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/', '-ll']
        
  # Dependency checking
  - repo: https://github.com/pyupio/safety
    rev: v2.3.5
    hooks:
      - id: safety
```

### Environment Variable Safety
```bash
# Never do this
export API_KEY=sk_live_abcd1234  # ❌ In shell history!

# Do this instead
read -s -p "Enter API key: " API_KEY && export API_KEY

# Or use a secrets manager
op read "op://vault/api/key"        # 1Password CLI
aws secretsmanager get-secret-value # AWS
vault kv get secret/api/key         # HashiCorp Vault
```

## 🗄️ Database Mistake-Proofing

### Migration Safety
```bash
# ALWAYS backup first
pg_dump dbname > backup_$(date +%Y%m%d_%H%M%S).sql

# Preview migrations
alembic upgrade head --sql > migration_preview.sql
# Review the SQL before running!

# Safe rollback strategy
alembic current
alembic history
alembic downgrade -1  # Go back one step
```

### Connection String Safety
```bash
# Development
DATABASE_URL=postgresql://user:pass@localhost/myapp_dev

# Test (separate database!)
TEST_DATABASE_URL=postgresql://user:pass@localhost/myapp_test

# Production (use connection pooling)
DATABASE_URL=postgresql://user:pass@host/myapp?pool_size=10&max_overflow=20
```

## 📊 Performance Mistake-Proofing

### Profiling Before Optimizing
```bash
# Python
python -m cProfile -o profile.stats script.py
python -m pstats profile.stats

# Go
go test -bench=. -cpuprofile=cpu.prof
go tool pprof cpu.prof

# Node.js
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Rust
cargo build --release
perf record --call-graph=dwarf target/release/myapp
perf report
```

## 🧪 Testing Mistake-Proofing

### Test Database Isolation
```bash
# Python/pytest
@pytest.fixture
def db():
    """Create a fresh database for each test"""
    test_db = create_test_database()
    yield test_db
    test_db.drop_all_tables()

# Go
func TestMain(m *testing.M) {
    // Setup test database
    testDB := setupTestDB()
    defer testDB.Close()
    
    // Run tests
    code := m.Run()
    os.Exit(code)
}
```

### Coverage Requirements
```bash
# Set minimum coverage in CI/CD
pytest --cov=src --cov-fail-under=80
go test -cover -coverprofile=coverage.out ./...
npm test -- --coverage --coverageThreshold='{"global":{"branches":80}}'
```

## 📝 Git Workflow Mistake-Proofing

### Commit Size Limits
```bash
# Check before committing
git diff --stat
find . -size +5M -not -path "./.git/*"

# Git hooks (.git/hooks/pre-commit)
#!/bin/bash
files=$(git diff --cached --name-only)
for file in $files; do
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    if [[ $size -gt 5242880 ]]; then  # 5MB
        echo "❌ File $file is too large: $(($size/1048576))MB"
        exit 1
    fi
done
```

## 🚀 CI/CD Mistake-Proofing

### Required Checks
```yaml
# GitHub Actions example
jobs:
  safety-checks:
    runs-on: ubuntu-latest
    steps:
      - name: No secrets in code
        run: |
          if git grep -E "(api_key|password|secret)" -- '*.py' '*.js' '*.go'; then
            echo "❌ Possible secrets found!"
            exit 1
          fi
          
      - name: No debug code
        run: |
          if git grep -E "(console\.log|print\(|fmt\.Println)" -- '*.js' '*.py' '*.go'; then
            echo "⚠️ Debug statements found"
          fi
```

## 📚 Additional Resources

- [The Twelve-Factor App](https://12factor.net/) - Best practices for modern apps
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Security mistakes to avoid
- [Google's Engineering Practices](https://google.github.io/eng-practices/) - Code review standards
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message standards

---

Remember: **The best mistake is one that never happens.** Use these patterns to build safety into your workflow!