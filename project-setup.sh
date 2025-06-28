#!/bin/bash
# Project Setup Script for Claude Code Integration

set -e

PROJECT_NAME="$1"
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

echo "Setting up new project: $PROJECT_NAME"

# Create project directory
mkdir -p ~/workspace/"$PROJECT_NAME"
cd ~/workspace/"$PROJECT_NAME"

# Initialize git
git init

# Copy base Claude template
cp ~/workspace/.claude-templates/claude-base-template.md ./CLAUDE.md

# Replace project name placeholder
sed -i "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" CLAUDE.md

echo "Project $PROJECT_NAME created successfully!"
echo "Next steps:"
echo "1. cd ~/workspace/$PROJECT_NAME"
echo "2. Run: claude /init"
echo "3. Customize CLAUDE.md for your specific project"