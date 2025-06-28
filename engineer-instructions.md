# Engineer Instructions - Schema Governance Framework

Expert-approved command patterns and workflows for the Schema Rules Workflow & Governance Framework.

## Expert-Approved Command Patterns (80/20 Rule)

### DAILY COMMANDS (80% usage)

#### Schema Validation with Governance Rules & Compliance Gap Identification
```bash
# CODE: Multi-layer validation with compliance checking
python scripts/validate_data.py --file src/industry/[profile].yaml
python scripts/validate_yaml.py --schema-file schemas/[schema].schema.json --data-file [file].yaml

# REVIEW: Check validation logs for compliance gaps
LOG_LEVEL=DEBUG python scripts/validate_data.py --file [file].yaml 2>&1 | jq '.level, .message'

# DEPLOY: Validate before commit
python scripts/validate_data.py --file src/validation_rules.yaml --file rulebook.yaml
```

#### AI-Assisted Schema Generation with Multi-Layer Validation
```bash
# CODE: Generate schema using AI templates
python scripts/ask_ai.py --prompt-file src/prompts/01_industry_discovery.md
python scripts/ask_ai.py --prompt-file src/prompts/03_schema_generation.md --input-file profile.yaml

# REVIEW: Validate AI-generated output
python scripts/validate_data.py --file generated_profile.yaml
python scripts/validate_yaml.py --schema-file schemas/industry-profile.schema.json --data-file generated_profile.yaml

# DEPLOY: Test integration
pytest tests/test_validator.py -v -k "test_ai_generated"
```

#### Debug Governance Validation Errors with Regression Prevention
```bash
# CODE: Identify validation failures
python scripts/validate_data.py --file failing_file.yaml --rules src/validation_rules.yaml

# REVIEW: Analyze error patterns
LOG_LEVEL=DEBUG python scripts/validate_data.py --file [file].yaml 2>&1 | jq 'select(.level=="ERROR")'

# DEPLOY: Prevent regressions
pytest && python scripts/validate_data.py --file [fixed_file].yaml
```

#### Industry Profile Development with Comprehensive Validation
```bash
# CODE: Create and validate new profile
python scripts/scaffold_new_profile.py --industry "[name]" --output src/industry/[name]_profile.yaml
python scripts/validate_data.py --file src/industry/[name]_profile.yaml

# REVIEW: Check against governance standards
python scripts/validate_yaml.py --schema-file schemas/financial-services-profile.schema.json --data-file src/industry/[name]_profile.yaml

# DEPLOY: Add to CI pipeline
# Manual: Edit .github/workflows/ci.yml to include new profile validation
```

### WEEKLY COMMANDS (15% usage)

#### Project Health Analysis for Rulebook Compliance
```bash
# CODE: Audit all industry profiles
for file in src/industry/*_profile.yaml; do python scripts/validate_data.py --file "$file"; done

# REVIEW: Generate compliance report
python scripts/generate_rulebook.py && python scripts/update_readme.py

# DEPLOY: Update project documentation
git add dist/rulebook_dist.yaml README.md && git commit -m "chore: update project health audit"
```

#### Security Audit of Manifest and Validation Scripts
```bash
# CODE: Verify script authorization
mapfile -t authorized < <(yq '.authorized_scripts[]' manifest.yaml)
mapfile -t actual < <(ls -1 scripts/*.py | xargs -n 1 basename)

# REVIEW: Check security policies compliance
python scripts/validate_yaml.py --schema-file schemas/security-policies.schema.json --data-file src/security_policies.yaml

# DEPLOY: Audit validation in CI
gh run list --workflow=ci.yml --limit 10 | grep "verify-manifest"
```

#### Performance Optimization with Monitoring
```bash
# CODE: Profile validation performance
time python scripts/validate_data.py --file src/industry/financial-services_profile.yaml

# REVIEW: Analyze bottlenecks
LOG_LEVEL=DEBUG python scripts/validate_data.py --file large_profile.yaml 2>&1 | jq '.timestamp, .message'

# DEPLOY: Optimize and monitor
pytest tests/test_validator.py::test_performance -v
```

### SETUP COMMANDS (5% usage)

#### New Industry Profile Setup Following Governance Framework
```bash
# CODE: Initialize complete profile structure
python scripts/scaffold_new_profile.py --industry "[industry]" --output src/industry/[industry]_profile.yaml
python scripts/ask_ai.py --prompt-file src/prompts/02_profile_enrichment.md --input-file src/industry/[industry]_profile.yaml

# REVIEW: Validate complete setup
python scripts/validate_data.py --file src/industry/[industry]_profile.yaml
python scripts/validate_yaml.py --schema-file schemas/industry-categories.schema.json --data-file src/industry/industry_categories.yaml

# DEPLOY: Integrate into governance framework
echo "[industry]_profile.yaml" >> manifest.yaml && git add . && git commit -m "feat: add [industry] profile"
```

#### Schema Distribution with Rulebook Package Generation
```bash
# CODE: Generate distributable packages
python scripts/generate_rulebook.py
python scripts/update_readme.py

# REVIEW: Validate distribution integrity
python scripts/validate_yaml.py --schema-file schemas/schema-rulebook.schema.json --data-file dist/rulebook_dist.yaml

# DEPLOY: Create release package
git tag v$(yq '.schema.version' rulebook.yaml) && git push --tags
```

## Core Validation Commands

### Multi-Layer Validation (Recommended)
```bash
# Validate with both schema and business logic
python scripts/validate_data.py --file src/industry/financial-services_profile.yaml

# Validate multiple files
python scripts/validate_data.py --file src/validation_rules.yaml --file rulebook.yaml

# Use custom validation rules
python scripts/validate_data.py --file profile.yaml --rules custom_rules.yaml
```

### Schema-Only Validation
```bash
# Validate YAML structure against JSON Schema
python scripts/validate_yaml.py --schema-file schemas/financial-services-profile.schema.json --data-file src/industry/financial-services_profile.yaml

# Dry run (simulation mode)
python scripts/validate_yaml.py --schema-file schemas/rulebook.schema.json --data-file rulebook.yaml --dry-run
```

## Development Workflow Commands

### Project Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run test suite
pytest

# Run specific test file
pytest tests/test_validator.py -v
```

### Rulebook Management
```bash
# Generate distributable rulebook
python scripts/generate_rulebook.py

# Update README from rulebook
python scripts/update_readme.py

# Validate core governance files
python scripts/validate_data.py --file rulebook.yaml
python scripts/validate_data.py --file src/validation_rules.yaml
```

### Industry Profile Development
```bash
# Create new industry profile scaffold
python scripts/scaffold_new_profile.py --industry "healthcare" --output src/industry/healthcare_profile.yaml

# Validate new profile
python scripts/validate_data.py --file src/industry/healthcare_profile.yaml

# Add to CI pipeline (manual step)
# Edit .github/workflows/ci.yml to include new profile validation
```

## AI-Assisted Development

### Schema Generation Workflow
```bash
# Industry discovery
python scripts/ask_ai.py --prompt-file src/prompts/01_industry_discovery.md

# Profile enrichment
python scripts/ask_ai.py --prompt-file src/prompts/02_profile_enrichment.md --input-file initial_profile.yaml

# Schema generation
python scripts/ask_ai.py --prompt-file src/prompts/03_schema_generation.md --input-file enriched_profile.yaml

# Validation and review
python scripts/ask_ai.py --prompt-file src/prompts/04_validation_and_review.md --input-file generated_schema.yaml
```

## Security & Governance Commands

### Script Authorization
```bash
# Verify script manifest (done in CI)
yq '.authorized_scripts[]' manifest.yaml

# Add new script to manifest
yq '.authorized_scripts += ["new_script.py"]' -i manifest.yaml
```

### Security Validation
```bash
# Validate security policies
python scripts/validate_yaml.py --schema-file schemas/security-policies.schema.json --data-file src/security_policies.yaml

# Check industry categories
python scripts/validate_yaml.py --schema-file schemas/industry-categories.schema.json --data-file src/industry/industry_categories.yaml
```

## CI/CD Integration Commands

### Local CI Simulation
```bash
# Run manifest verification locally
mapfile -t authorized < <(yq '.authorized_scripts[]' manifest.yaml)
mapfile -t actual < <(ls -1 scripts/*.py | xargs -n 1 basename)

# Validate all core files (CI pipeline simulation)
python scripts/validate_yaml.py --schema-file schemas/schema-rulebook.schema.json --data-file rulebook.yaml
python scripts/validate_yaml.py --schema-file schemas/validation-rules.schema.json --data-file src/validation_rules.yaml
python scripts/validate_yaml.py --schema-file schemas/industry-categories.schema.json --data-file src/industry/industry_categories.yaml
```

### GitHub Actions Commands
```bash
# Push changes to trigger CI
git add . && git commit -m "feat: update schema validation" && git push

# Check CI status
gh run list --workflow=ci.yml --limit 5
```

## Advanced Operations

### Performance Optimization
```bash
# Enable debug logging
LOG_LEVEL=DEBUG python scripts/validate_data.py --file large_profile.yaml

# Profile validation performance
time python scripts/validate_data.py --file src/industry/financial-services_profile.yaml
```

### Custom Rule Development
```bash
# Test custom validation rules
python scripts/validate_data.py --file test_data.yaml --rules custom_validation_rules.yaml

# Validate rule structure
python scripts/validate_yaml.py --schema-file schemas/validation-rules.schema.json --data-file custom_validation_rules.yaml
```

### Batch Operations
```bash
# Validate all industry profiles
for file in src/industry/*_profile.yaml; do
  echo "Validating $file..."
  python scripts/validate_data.py --file "$file"
done

# Validate all schemas
for schema in schemas/*.schema.json; do
  filename=$(basename "$schema" .schema.json)
  if [ -f "src/${filename}.yaml" ]; then
    python scripts/validate_yaml.py --schema-file "$schema" --data-file "src/${filename}.yaml"
  fi
done
```

## Troubleshooting Commands

### Common Issues
```bash
# Fix import path issues
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Check file permissions
ls -la scripts/*.py

# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('problematic_file.yaml'))"

# Check JSON Schema validity
python -c "import json; json.load(open('schemas/schema.json'))"
```

### Debug Validation Failures
```bash
# Enable verbose logging
LOG_LEVEL=DEBUG python scripts/validate_data.py --file failing_file.yaml 2>&1 | jq '.'

# Test individual validation rules
python -c "
import yaml
from scripts.validate_data import validate_file_content
data = yaml.safe_load(open('test_file.yaml'))
rules = yaml.safe_load(open('src/validation_rules.yaml'))
validate_file_content('test_file.yaml', data, rules)
"
```

## Environment Setup

### Required Dependencies
```bash
# Core dependencies
pip install PyYAML jsonschema python-dotenv

# AI providers (optional)
pip install openai  # For OpenAI integration

# Development tools
pip install pytest  # For testing
```

### Environment Variables
```bash
# Set logging level
export LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# AI provider configuration (if using AI features)
export OPENAI_API_KEY="your-api-key"
```

## Best Practices

1. **Always validate before committing**: Run `python scripts/validate_data.py --file [modified-file]`
2. **Update manifest for new scripts**: Add to `manifest.yaml` authorized_scripts list
3. **Use structured logging**: All scripts use JsonFormatter from `src/utils.py`
4. **Follow naming conventions**: snake_case for fields, specific patterns per rulebook
5. **Test thoroughly**: Run `pytest` before submitting changes
6. **Security first**: Never commit sensitive data, always validate security policies

## Quick Reference

| Task | Command |
|------|---------|
| Validate single file | `python scripts/validate_data.py --file filename.yaml` |
| Generate rulebook | `python scripts/generate_rulebook.py` |
| Run tests | `pytest` |
| Schema validation only | `python scripts/validate_yaml.py --schema-file schema.json --data-file data.yaml` |
| AI schema generation | `python scripts/ask_ai.py --prompt-file src/prompts/03_schema_generation.md` |
| Update documentation | `python scripts/update_readme.py` |