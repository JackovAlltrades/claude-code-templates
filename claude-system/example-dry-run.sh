#!/bin/bash
# Example: Using dry-run feature with the Claude merger

echo "=== Claude Template Merger - Dry Run Examples ==="
echo

# 1. Basic dry run
echo "1. Preview changes without applying:"
echo "   python merger.py --dry-run"
echo

# 2. Dry run with developer preferences
echo "2. Preview with developer customizations:"
echo "   python merger.py --username alice --dry-run"
echo

# 3. Dry run with debug output
echo "3. Detailed debug information:"
echo "   python merger.py --debug --dry-run"
echo

# 4. Check policy violations
echo "4. When policy violations are detected:"
echo "   python merger.py --dry-run"
echo "   # Review report at .claude-project/dry-run-report.txt"
echo "   # If you must override (NOT RECOMMENDED):"
echo "   python merger.py --force"
echo

# Example output format:
cat << 'EOF'

==============================================================
DRY RUN SUMMARY
==============================================================
✅ Added sections: 3
❌ Removed sections: 0
📝 Modified sections: 5
⚠️  Policy violations: 1

Full report: .claude-project/dry-run-report.txt
Preview file: .claude-project/CLAUDE.md.preview

⚠️  WARNING: Policy violations detected!
The merge cannot proceed with these violations.
EOF