# Security Standards Template - OWASP Compliant

## 🔒 Security Best Practices (OWASP Top 10)

### 1. Security Headers (OWASP A05:2021 – Security Misconfiguration)

#### Required HTTP Security Headers
```http
# Prevent clickjacking attacks
X-Frame-Options: DENY

# Prevent MIME type sniffing
X-Content-Type-Options: nosniff

# Enable XSS protection in older browsers
X-XSS-Protection: 1; mode=block

# Force HTTPS (HSTS)
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

# Control referrer information
Referrer-Policy: strict-origin-when-cross-origin

# Content Security Policy
Content-Security-Policy: default-src 'self'; frame-ancestors 'none';

# Permissions Policy
Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()

# Additional security headers
X-Permitted-Cross-Domain-Policies: none
```

#### Implementation Examples

**Go (Middleware)**
```go
func SecurityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-XSS-Protection", "1; mode=block")
        w.Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload")
        w.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
        w.Header().Set("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none';")
        w.Header().Set("Permissions-Policy", "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()")
        next.ServeHTTP(w, r)
    })
}
```

**Python (FastAPI)**
```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
        response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
        return response

app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)
```

**Node.js (Express with Helmet)**
```javascript
const helmet = require('helmet');

app.use(helmet({
    frameguard: { action: 'deny' },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    },
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            frameAncestors: ["'none'"]
        }
    },
    permissionsPolicy: {
        features: {
            accelerometer: ["'none'"],
            camera: ["'none'"],
            geolocation: ["'none'"],
            gyroscope: ["'none'"],
            magnetometer: ["'none'"],
            microphone: ["'none'"],
            payment: ["'none'"],
            usb: ["'none'"]
        }
    }
}));
```

### 2. Input Validation (OWASP A03:2021 – Injection)

#### Validation Rules
- **Whitelist over Blacklist**: Define what IS allowed, not what isn't
- **Validate on Server Side**: Never trust client-side validation alone
- **Escape Output**: Always escape data before rendering
- **Use Parameterized Queries**: Prevent SQL injection
- **Validate File Uploads**: Check MIME types, extensions, and content

#### Implementation Examples
```python
# Python - Pydantic validation
from pydantic import BaseModel, validator, EmailStr
from typing import Optional
import re

class UserInput(BaseModel):
    email: EmailStr
    username: str
    age: int
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match("^[a-zA-Z0-9_-]{3,20}$", v):
            raise ValueError('Username must be 3-20 characters, alphanumeric only')
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v < 13 or v > 120:
            raise ValueError('Age must be between 13 and 120')
        return v
```

### 3. Authentication & Session Management (OWASP A07:2021)

#### Best Practices
- **Strong Password Policy**: Min 12 chars, complexity requirements
- **Multi-Factor Authentication**: Implement where possible
- **Secure Session Tokens**: Use cryptographically secure random tokens
- **Session Timeout**: Implement idle and absolute timeouts
- **Secure Cookie Flags**: HttpOnly, Secure, SameSite

```python
# Secure session configuration
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JS access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
SESSION_COOKIE_MAX_AGE = 1800  # 30 minutes
```

### 4. Access Control (OWASP A01:2021 – Broken Access Control)

#### Implementation Checklist
- [ ] Deny by default
- [ ] Implement least privilege principle
- [ ] Validate user permissions on every request
- [ ] Use indirect object references
- [ ] Log access control failures
- [ ] Rate limit API access

### 5. Cryptography (OWASP A02:2021 – Cryptographic Failures)

#### Standards
- **Encryption at Rest**: AES-256
- **Encryption in Transit**: TLS 1.3
- **Password Hashing**: Argon2id, bcrypt, or scrypt
- **Key Management**: Use dedicated key management service
- **Random Number Generation**: Use cryptographically secure methods

```python
# Python - Secure password hashing
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=1,
    hash_len=32,
    salt_len=16
)

# Hash password
hashed = ph.hash(password)

# Verify password
try:
    ph.verify(hashed, password)
except VerifyMismatchError:
    # Invalid password
    pass
```

### 6. Error Handling & Logging (OWASP A09:2021)

#### Security Logging Requirements
- Log authentication attempts (success/failure)
- Log authorization failures
- Log input validation failures
- Log security header violations
- Include: timestamp, user ID, IP, action, result
- Exclude: passwords, tokens, sensitive data

```python
import logging
from datetime import datetime

security_logger = logging.getLogger('security')

def log_security_event(event_type, user_id, ip_address, details, success=True):
    security_logger.info({
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'ip_address': ip_address,
        'success': success,
        'details': details
    })
```

### 7. API Security

#### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/endpoint")
@limiter.limit("10/minute")
async def limited_endpoint():
    return {"message": "This endpoint is rate limited"}
```

#### API Security Headers
```yaml
# OpenAPI security definition
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### 8. Dependency Security (OWASP A06:2021)

#### Automated Scanning
```bash
# Python
pip install safety
safety check

# Node.js
npm audit
npm audit fix

# Go
go list -m all | nancy sleuth

# General
trivy fs .
```

### 9. Security Testing

#### SAST (Static Application Security Testing)
```yaml
# GitHub Actions example
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/owasp
```

#### DAST (Dynamic Application Security Testing)
```bash
# OWASP ZAP baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://your-app.com
```

### 10. Security Monitoring & Incident Response

#### Key Metrics to Monitor
- Failed authentication attempts
- Unusual access patterns
- Rate limit violations
- Security header violations
- Error rate spikes
- Response time anomalies

#### Incident Response Plan
1. **Detect**: Automated alerting on security events
2. **Respond**: Immediate actions (block IP, disable account)
3. **Investigate**: Log analysis, impact assessment
4. **Remediate**: Fix vulnerability, patch systems
5. **Learn**: Post-mortem, update procedures

### 11. Compliance Requirements

#### GDPR (Data Protection)
- [ ] Privacy by design
- [ ] Data minimization
- [ ] Right to erasure
- [ ] Data portability
- [ ] Consent management

#### PCI DSS (Payment Card Security)
- [ ] Network segmentation
- [ ] Encryption of cardholder data
- [ ] Access control
- [ ] Regular security testing
- [ ] Security policies

### 12. Security Quick Wins Checklist

**Immediate (5 minutes)**
- [ ] Add security headers middleware
- [ ] Enable HTTPS only
- [ ] Set secure cookie flags

**Short-term (1 hour)**
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Configure CSP

**Medium-term (1 day)**
- [ ] Set up dependency scanning
- [ ] Implement proper logging
- [ ] Add authentication middleware

**Long-term (1 week)**
- [ ] Complete security audit
- [ ] Implement WAF rules
- [ ] Set up monitoring alerts

---
*Always follow the principle of Defense in Depth - multiple layers of security controls*