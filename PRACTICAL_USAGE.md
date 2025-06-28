# Claude Code Templates - Practical Usage Guide

## Daily Workflow Scenarios

### Scenario 1: Starting Your Development Day

**Morning Routine (2 minutes):**
```bash
# Quick check of your patterns
claude-patterns

# Navigate to your project
cd ~/workspace/schema-rules-workflow

# Start Claude Code
claude
```

**First task - check project health:**
```bash
claude "analyze current project status: check for any validation errors, review recent changes, and identify priority tasks for today's development session"
```

### Scenario 2: Implementing a New Feature

**Example: Adding a new industry profile**

**Step 1 - Planning (CODE phase):**
```bash
claude "help me plan implementation of a healthcare industry profile. Generate the development approach: file structure, validation requirements, schema definitions, and testing strategy following our governance framework"
```

**Step 2 - Implementation:**
```bash
claude "create healthcare industry profile following our governance framework: generate healthcare_profile.yaml with appropriate validation rules, create corresponding JSON schema, and implement comprehensive tests"
```

**Step 3 - Validation:**
```bash
claude "validate the new healthcare profile: run multi-layer validation, check compliance with rulebook, and ensure all security policies are met"
```

### Scenario 3: Debugging Issues

**When validation fails:**
```bash
claude "debug validation failure: [paste error message]. Analyze root cause, implement fix with regression prevention, and add monitoring to detect similar issues early"
```

**When AI generation produces unexpected results:**
```bash
claude "review AI-generated schema for healthcare profile: check for governance compliance, validate business logic rules, and suggest improvements for reliability"
```

### Scenario 4: Code Review & Quality

**Before creating PR:**
```bash
claude "prepare this code for review: analyze security vulnerabilities, check performance implications, verify test coverage, and ensure documentation is complete"
```

**Weekly quality check:**
```bash
claude "perform weekly project health analysis: dependency vulnerabilities, code quality metrics, technical debt assessment, and governance compliance across all industry profiles"
```

## Advanced Usage Patterns

### Working with AI Prompt Templates

**Schema generation workflow:**
```bash
# Use your existing prompt templates
claude "use prompt template 03_schema_generation.md to create schema for retail industry with comprehensive validation layers and error handling"

# Follow up with validation
claude "validate the AI-generated retail schema using our multi-layer validation system and suggest improvements"
```

### Managing Multiple Projects

**Setting up a new project:**
```bash
# Use your setup script
claude-setup fintech-compliance-tool

# Navigate and initialize
cd ~/workspace/fintech-compliance-tool
claude /init

# Customize for the specific project
claude "help me customize this CLAUDE.md for a fintech compliance tool: update technology stack, add domain-specific patterns, and include regulatory requirements"
```

### Security-First Development

**Before any schema changes:**
```bash
claude "security review: analyze proposed schema changes for potential vulnerabilities, data exposure risks, and compliance impacts. Include recommendations for secure implementation"
```

**Regular security audits:**
```bash
claude "comprehensive security audit: review manifest.yaml for unauthorized scripts, validate security policies, check for dependency vulnerabilities, and assess governance framework security posture"
```

## Team Collaboration Patterns

### Onboarding New Team Members

**Day 1 setup for new developer:**
```bash
# Clone the templates
git clone <your-templates-repo> ~/.claude-templates

# Set up aliases
source ~/.claude-templates/setup-aliases.sh

# Quick orientation
claude-rules  # Show them the workflow
claude-patterns  # Show them the patterns
```

**First task assignment:**
```bash
claude "help onboard new team member: explain our schema governance framework, walk through validation pipeline, and suggest a good first contribution task"
```

### Code Review Process

**Reviewer workflow:**
```bash
claude "review this PR for schema governance changes: check compliance with rulebook, validate security implications, assess impact on existing industry profiles, and provide actionable feedback"
```

**Author workflow:**
```bash
claude "prepare PR description: summarize changes to governance framework, explain validation additions, document testing performed, and highlight any breaking changes"
```

## Troubleshooting Common Issues

### Template Updates

**When you discover better patterns:**
```bash
cd ~/.claude-templates

# Update the templates
claude "improve engineer-instructions.md: add new pattern for [specific use case], update best practices based on recent experience, and maintain 80/20 focus"

# Version the improvement
git add .
git commit -m "feat: improve patterns for schema validation workflows"
git tag v1.1-improved-patterns
```

### Project-Specific Customization

**Adapting templates for different project types:**
```bash
# For API projects
claude "customize CLAUDE.md template for REST API development: add API-specific patterns, security considerations, and testing strategies"

# For data processing projects  
claude "customize CLAUDE.md template for data pipeline development: add data validation patterns, performance optimization guidelines, and monitoring approaches"
```

## Success Metrics & Habits

### Daily Habits to Build

1. **Start with context:** Always use `claude-patterns` to refresh your memory
2. **Be specific:** Use engineer-level instructions, not vague requests
3. **Security first:** Include security considerations in every request
4. **Test everything:** Always ask for tests with implementation
5. **Document as you go:** Update templates when you find better patterns

### Weekly Habits

1. **Template review:** Check if you've discovered better patterns
2. **Project health:** Run comprehensive analysis
3. **Security audit:** Regular security review
4. **Knowledge sharing:** Update team documentation

### Monthly Habits

1. **Template evolution:** Version and tag improvements
2. **Team feedback:** Gather input on template effectiveness
3. **Metrics review:** Assess productivity improvements
4. **Best practice updates:** Incorporate lessons learned

## Measuring Success

**Productivity Indicators:**
- Can implement new features without reading documentation
- Error recovery is systematic and fast
- Code reviews focus on business logic, not style issues
- New team members productive within hours, not days

**Quality Indicators:**
- Security issues caught in development, not production
- Tests catch real bugs before deployment
- Governance compliance is automatic, not manual
- Technical debt is managed proactively

## Emergency Procedures

**When templates are corrupted:**
```bash
# Restore from git
cd ~/.claude-templates
git reset --hard v1.0-expert-approved
```

**When Claude Code behaves unexpectedly:**
```bash
# Check CLAUDE.md configuration
claude "analyze current CLAUDE.md configuration: verify it follows our expert-approved patterns and suggest any needed corrections"
```

**When project validation fails:**
```bash
# Emergency validation bypass (use carefully)
claude "emergency analysis: project validation failing, need immediate assessment of critical issues and minimal viable fixes for production deployment"
```

Remember: These templates are living documents. They should evolve with your experience and team needs while maintaining the core expert-approved principles.