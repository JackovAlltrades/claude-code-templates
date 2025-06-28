# Claude Code Templates - Expert Approved

Expert-approved templates for Claude Code development following the simplified CODE → REVIEW → DEPLOY workflow.

## 🚀 Quick Start

```bash
# Clone this repository
git clone git@github.com:JackovAlltrades/claude-code-templates.git ~/.claude-templates

# Set up aliases
echo 'alias claude-patterns="head -50 ~/.claude-templates/engineer-instructions.md"' >> ~/.bashrc
echo 'alias claude-setup="~/.claude-templates/project-setup.sh"' >> ~/.bashrc
echo 'alias claude-templates="cd ~/.claude-templates && ls -la"' >> ~/.bashrc
echo 'alias claude-rules="cat ~/.claude-templates/warp-rules.md"' >> ~/.bashrc
source ~/.bashrc

# Create your first project
claude-setup my-new-project
```

## 📁 Files

- `claude-base-template.md` - Base CLAUDE.md template for new projects
- `engineer-instructions.md` - Expert-approved 80/20 command patterns
- `warp-rules.md` - Refined development workflow rules (reference)
- `project-setup.sh` - Automated project setup script
- `PRACTICAL_USAGE.md` - **Detailed usage scenarios and best practices**

## 📖 Documentation

### Essential Reading
1. **[PRACTICAL_USAGE.md](./PRACTICAL_USAGE.md)** - Daily workflows, scenarios, and best practices
2. **[engineer-instructions.md](./engineer-instructions.md)** - 80/20 command patterns
3. **[warp-rules.md](./warp-rules.md)** - Core development principles

### Usage Patterns

**Daily Development:**
```bash
claude-patterns  # View 80/20 command patterns
claude-rules     # Review workflow principles
```

**New Project Setup:**
```bash
claude-setup project-name  # Automated project creation
```

**Reference Workflow:**
```bash
# CODE → REVIEW → DEPLOY (3 steps, not 6 phases)
claude "implement [feature] with error handling, validation, and tests"
claude "review [component] for security and performance issues" 
claude "prepare [changes] for production deployment with monitoring"
```

## 🎯 Expert-Approved Principles

Based on feedback from **Linus Torvalds**, **Jakob Nielsen**, and **Bruce Schneier** principles:

### Core Philosophy
- **Perfection is the enemy of good** - Ship working code, iterate to improve
- **Users don't read documentation** - Make the right thing the easy thing
- **Security is about trade-offs** - Practical security, not security theater
- **Automate boring stuff, think about hard stuff** - AI handles boilerplate, humans handle architecture

### 80/20 Rule Implementation
- **Daily commands (80%):** Feature development, bug fixes, code review
- **Weekly commands (15%):** Project health, dependency updates, security audits
- **Setup commands (5%):** New projects, major configuration changes

### Success Metrics
- ✅ Developer productive in **5 minutes**, not 5 hours
- ✅ Common tasks have **clear, simple patterns**
- ✅ Error recovery is **fast and systematic**
- ✅ Security issues caught in **development, not production**

## 🔧 Advanced Usage

See [PRACTICAL_USAGE.md](./PRACTICAL_USAGE.md) for:
- Daily workflow scenarios
- Team collaboration patterns
- Security-first development approaches
- Troubleshooting common issues
- Building productive habits

## 📊 Version History

- **v1.0-expert-approved** - Initial expert-reviewed templates
- **v1.1-practical-guide** - Added comprehensive usage scenarios

## 🤝 Contributing

1. Follow the expert-approved principles
2. Test patterns in real projects before suggesting
3. Maintain the 80/20 focus (common use cases first)
4. Update practical guide with new scenarios

## 📄 License

MIT License - Feel free to adapt for your team's needs while maintaining the core expert-approved principles.