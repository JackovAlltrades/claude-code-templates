#!/bin/bash

# Add Security Standards to Existing Project
# This script adds OWASP security standards to an existing CLAUDE.md file

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if CLAUDE.md exists
if [ ! -f "CLAUDE.md" ]; then
    print_message "$RED" "Error: CLAUDE.md not found in current directory"
    exit 1
fi

# Check if security section already exists
if grep -q "Security Standards (OWASP Compliant)" CLAUDE.md; then
    print_message "$YELLOW" "Security standards section already exists in CLAUDE.md"
    exit 0
fi

# Create backup
cp CLAUDE.md CLAUDE.md.backup
print_message "$GREEN" "Created backup: CLAUDE.md.backup"

# Find insertion point (after Code Philosophy section)
if grep -q "## Code Philosophy" CLAUDE.md; then
    # Insert after the Code Philosophy section
    awk '
    /^## Code Philosophy/ {
        philosophy_section = 1
    }
    philosophy_section && /^## / && !/^## Code Philosophy/ {
        print "## 🔒 Security Standards (OWASP Compliant)\n"
        print "### Required Security Headers"
        print "All HTTP responses MUST include these security headers:"
        print "```"
        print "X-Frame-Options: DENY"
        print "X-Content-Type-Options: nosniff"
        print "X-XSS-Protection: 1; mode=block"
        print "Strict-Transport-Security: max-age=31536000; includeSubDomains; preload"
        print "Referrer-Policy: strict-origin-when-cross-origin"
        print "Content-Security-Policy: default-src '\''self'\''; frame-ancestors '\''none'\'';"
        print "Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
        print "```\n"
        print "### Security Implementation Checklist"
        print "- [ ] **Security headers middleware** implemented (OWASP A05)"
        print "- [ ] **Input validation** on ALL endpoints (OWASP A03)"
        print "- [ ] **Authentication** required for protected routes (OWASP A07)"
        print "- [ ] **Authorization** checks at service layer (OWASP A01)"
        print "- [ ] **Audit logging** for sensitive operations (OWASP A09)"
        print "- [ ] **Rate limiting** implemented (OWASP A04)"
        print "- [ ] **CORS** properly configured"
        print "- [ ] **HTTPS** enforced everywhere"
        print "- [ ] **Dependencies** scanned for vulnerabilities (OWASP A06)"
        print "- [ ] **Error handling** doesn'\''t leak sensitive info (OWASP A09)\n"
        print "### Quick Security Wins (5 minutes)"
        print "1. Add security headers middleware"
        print "2. Enable HTTPS redirect"
        print "3. Set secure cookie flags"
        print "4. Configure CSP\n"
        print "See `~/.claude-templates/security-standards-template.md` for complete implementation guide.\n"
        philosophy_section = 0
    }
    {print}
    ' CLAUDE.md > CLAUDE.md.tmp && mv CLAUDE.md.tmp CLAUDE.md
    
    print_message "$GREEN" "✅ Security standards section added to CLAUDE.md"
else
    # If no Code Philosophy section, append at the end
    cat >> CLAUDE.md << 'EOF'

## 🔒 Security Standards (OWASP Compliant)

### Required Security Headers
All HTTP responses MUST include these security headers:
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; frame-ancestors 'none';
Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()
```

### Security Implementation Checklist
- [ ] **Security headers middleware** implemented (OWASP A05)
- [ ] **Input validation** on ALL endpoints (OWASP A03)
- [ ] **Authentication** required for protected routes (OWASP A07)
- [ ] **Authorization** checks at service layer (OWASP A01)
- [ ] **Audit logging** for sensitive operations (OWASP A09)
- [ ] **Rate limiting** implemented (OWASP A04)
- [ ] **CORS** properly configured
- [ ] **HTTPS** enforced everywhere
- [ ] **Dependencies** scanned for vulnerabilities (OWASP A06)
- [ ] **Error handling** doesn't leak sensitive info (OWASP A09)

### Quick Security Wins (5 minutes)
1. Add security headers middleware
2. Enable HTTPS redirect
3. Set secure cookie flags
4. Configure CSP

See `~/.claude-templates/security-standards-template.md` for complete implementation guide.
EOF
    
    print_message "$GREEN" "✅ Security standards section appended to CLAUDE.md"
fi

# Also update Code Philosophy if it exists
if grep -q "### Core Principles" CLAUDE.md && ! grep -q "Security First" CLAUDE.md; then
    sed -i '/5\. \*\*Continuous Improvement\*\*/a 6. **Security First**: OWASP standards built into every component' CLAUDE.md
    print_message "$GREEN" "✅ Added Security First principle to Code Philosophy"
fi

print_message "$GREEN" "\n🎉 Security standards successfully added!"
print_message "$YELLOW" "\nNext steps:"
print_message "$YELLOW" "1. Review the changes in CLAUDE.md"
print_message "$YELLOW" "2. Implement security headers middleware for your stack"
print_message "$YELLOW" "3. Run security audit: make security-audit (if available)"
print_message "$YELLOW" "4. See ~/.claude-templates/security-standards-template.md for detailed implementation"