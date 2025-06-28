# Refined Warp Development Rules - Expert Approved

**Philosophy:** Ship working code fast. Automate boring stuff. Think about hard stuff. Security is about smart trade-offs, not theater.

---

## Core Engineering Reality Principles

1. **Perfection is the enemy of good** - Ship working code, iterate to improve
2. **Users don't read documentation** - Make the right thing the easy thing  
3. **Security is about trade-offs** - Perfect security is unusable, usable systems can be secure enough
4. **Automate boring stuff, think about hard stuff** - Let AI handle boilerplate, humans handle architecture

---

## Simplified Workflow (3 Steps, Not 6 Phases)

### 1. CODE - Write, Test, Commit
- Write code that works and is readable
- Test what matters (complex logic, edge cases, not getters/setters)
- Commit with clear messages

### 2. REVIEW - PR, Security Check, Merge  
- Create PR with context
- Security review for data handling and trust boundaries
- Merge when ready

### 3. DEPLOY - Automated Release
- Let automation handle deployment
- Monitor and fix issues quickly

---

## Security-by-Design (Not Security Theater)

### Threat Model (Know What You're Protecting)
```markdown
**Assets**: Code, data, credentials, infrastructure access
**Threats**: External attackers, supply chain compromises, credential leaks
**Mitigations**: Input validation, authentication, secrets management, dependency scanning
```

### Security Engineering Standards

**Before Writing Code:**
- [ ] What data does this handle?
- [ ] What are the trust boundaries?  
- [ ] What could go wrong?

**While Writing Code:**
- [ ] Input validation at boundaries (whitelist approach)
- [ ] Error handling without information leakage
- [ ] Logging for security events

**Before Deployment:**
- [ ] Security scanning (automated)
- [ ] Dependency vulnerability check
- [ ] Secrets audit

---

## Code Quality Reality Check

### Write Code That:
✅ **Works** - Correctness first, optimization later  
✅ **Is readable** - Future you will thank you  
✅ **Is debuggable** - Can you trace execution when it breaks?  
✅ **Handles errors** - Things will go wrong, plan for it  
✅ **Is changeable** - Code will be modified, design for it  

### Test What Matters:
✅ **Complex business logic** - Where bugs hide  
✅ **Edge cases** - Boundary conditions, null values  
✅ **External integrations** - APIs, databases, file systems  
✅ **Security boundaries** - Authentication, authorization  
❌ **Simple getters/setters** - Don't test what the language guarantees  

---

## Tool Selection (No Overkill)

### Primary Stack:
- **Terminal**: Warp (command execution)
- **AI**: Claude Code CLI (single agent, not multiple)
- **Version Control**: git + gh CLI
- **Security**: Built-in scanners, not custom solutions

### Infrastructure:
- **Simple projects**: GitHub settings via web UI
- **Complex projects**: Infrastructure-as-Code only when justified
- **Containers**: When you need them, not because it's trendy

---

## Git Workflow (Trunk-Based, Simplified)

### Daily Commands:
```bash
# Create feature branch
git checkout -b username/feature-name

# Work and commit
git add .
git commit -m "feat: add user authentication"

# Create PR  
gh pr create --title "feat: add user auth" --body "Closes #123"

# Merge when ready
gh pr merge --squash --delete-branch
```

### Error Recovery (When Things Break):
```bash
# Rollback last commit
git reset --hard HEAD~1

# Fix merge conflicts
git rebase main
# resolve conflicts
git rebase --continue

# Emergency rollback
git revert <commit-hash>
gh pr create --title "hotfix: revert breaking change"
```

---

## Security Patterns (Practical, Not Theoretical)

### Secrets Management:
```bash
# Environment variables with rotation
export API_KEY=$(vault kv get -field=key secret/api)

# Never in code
❌ API_KEY = "sk-1234567890abcdef"
✅ API_KEY = os.getenv("API_KEY")
```

### Input Validation:
```python
# Whitelist approach
def validate_user_id(user_id: str) -> int:
    if not user_id.isdigit():
        raise ValueError("Invalid user ID format")
    id_int = int(user_id)
    if not 1 <= id_int <= 999999:
        raise ValueError("User ID out of range")
    return id_int
```

### Error Handling:
```python
# Don't leak information
❌ except Exception as e: return str(e)
✅ except Exception as e: 
    logger.error(f"Auth failed for user {user_id}: {e}")
    return "Authentication failed"
```

---

## Command Generation for Warp

### LLM Output Format:
1. **Context acknowledgment**: "This is a [scenario] in the [workflow step]"
2. **Plan summary**: Brief explanation of approach
3. **Command block**: Executable commands for Warp
4. **Verification**: How to confirm success

### Example:
```markdown
**Context**: New feature development in CODE phase
**Plan**: Add user authentication with JWT tokens
**Commands**:
```bash
# Create feature branch
git checkout -b bjhorn/jwt-auth

# Generate auth module with tests
claude "implement JWT authentication with FastAPI, include token generation/validation, error handling, and comprehensive tests"

# Commit changes
git add .
git commit -m "feat(auth): implement JWT authentication system"
```
**Verify**: Run tests and check token validation
```

---

## When to Use What

### 80/20 Rule - Most Common Operations:

**Daily (80% of usage):**
- `claude "add feature X with tests"`
- `claude "fix bug in function Y"`
- `claude "create PR for this change"`
- `claude "review security of this code"`

**Weekly (15% of usage):**
- `claude "analyze project health"`
- `claude "update dependencies safely"`

**Setup (5% of usage):**
- `claude "initialize new project"`
- `claude "adopt existing project"`

---

## Error Scenarios & Recovery

### When Commands Fail:
1. **Read the error message** - Usually tells you what's wrong
2. **Check prerequisites** - Are dependencies installed?
3. **Verify permissions** - Can you access the resource?
4. **Ask for help**: `claude "debug: [error message]"`

### When CI Breaks:
1. **Check the logs** - What specifically failed?
2. **Run tests locally** - Reproduce the issue
3. **Fix incrementally** - Small changes, quick feedback

### When Dependencies Conflict:
1. **Check for updates** - Often resolved in newer versions
2. **Isolate the conflict** - Which specific packages?
3. **Use lockfiles** - Pin working versions

---

## Final Reality Check

**Goal**: A developer can be productive in 5 minutes, not 5 hours of reading documentation.

**Measure of Success**: 
- Can a new team member contribute code on day 1?
- Are security issues caught automatically?
- Do deployments "just work"?
- When things break, is recovery fast?

**Remember**: The best practice is the one your team actually follows consistently.