# 🔌 MCP (Model Context Protocol) Setup Guide

## Table of Contents
1. [What is MCP?](#what-is-mcp)
2. [Prerequisites](#prerequisites)
3. [Quick Setup](#quick-setup)
4. [Available MCP Servers](#available-mcp-servers)
5. [mem0 Server Setup](#mem0-server-setup)
6. [Project Configuration](#project-configuration)
7. [Using MCP with Claude](#using-mcp-with-claude)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Configuration](#advanced-configuration)
10. [Creating Custom MCP Servers](#creating-custom-mcp-servers)

## What is MCP?

Model Context Protocol (MCP) is a system that extends Claude's capabilities by connecting it to external tools and services. Think of MCP servers as plugins that give Claude superpowers!

### Key Benefits
- 📝 **Persistent Memory**: Remember context across sessions
- 🔧 **Enhanced Tools**: Access to specialized functionality
- 🌐 **External Integration**: Connect to APIs and services
- 📁 **Better File Handling**: Advanced file operations
- 🧠 **Context Awareness**: Deeper project understanding

## Prerequisites

### System Requirements
- Python 3.8+
- Node.js 16+ (for some servers)
- WSL or Linux environment
- 4GB+ RAM recommended

### Required Software
```bash
# Check Python
python3 --version  # Should be 3.8+

# Check pip
pip3 --version

# Check Node (optional)
node --version  # Should be 16+

# Install dependencies
pip3 install anthropic pydantic httpx
```

## Quick Setup

### 1. Run the Setup Script
```bash
# Navigate to claude-templates
cd ~/workspace/.claude-templates

# Run MCP setup
./scripts/add-mcp-server-shared.sh --init
./scripts/add-mcp-server-shared.sh --common
```

### 2. Verify Installation
```bash
# Check MCP directory
ls ~/.mcp-shared/

# Should see:
# venv/       # Python virtual environment
# servers/    # MCP server scripts
# storage/    # Data storage
```

### 3. Test with Claude
```bash
# From your project directory
./claude "What do you remember about this project?"
```

## Available MCP Servers

### 1. **mem0** - Persistent Memory
Long-term memory storage for Claude across sessions.

**Features:**
- Stores project context
- Remembers previous conversations
- Learns from interactions
- Searchable memory

**Use Cases:**
- Project documentation
- Team knowledge base
- Decision history
- Code patterns

### 2. **filesystem** - Enhanced File Operations
Advanced file system operations beyond standard tools.

**Features:**
- Batch operations
- Advanced search
- File watching
- Metadata handling

**Use Cases:**
- Large-scale refactoring
- File organization
- Code analysis
- Bulk updates

### 3. **context7** - Project Context
Deep project understanding and analysis.

**Features:**
- Dependency analysis
- Code structure mapping
- Pattern detection
- Architecture visualization

**Use Cases:**
- Onboarding new developers
- Code reviews
- Architecture decisions
- Technical documentation

## mem0 Server Setup

### Step 1: Install Dependencies
```bash
# Create shared virtual environment
python3 -m venv ~/.mcp-shared/venv
source ~/.mcp-shared/venv/bin/activate

# Install mem0
pip install mem0ai chromadb openai
```

### Step 2: Configure API Keys

#### Using Doppler (Recommended)
```bash
# Setup Doppler project
doppler setup --project your-project --config dev

# Run with Doppler
doppler run -- ./claude "Your prompt"
```

#### Using Environment Variables
```bash
# Add to ~/.bashrc or project .env
export OPENAI_API_KEY="your-api-key-here"
```

### Step 3: Create mem0 Server Script
```python
# ~/.mcp-shared/servers/mem0-server.py
#!/usr/bin/env python3

import os
import asyncio
from typing import Any, Dict
from anthropic_mcp.server import Server
from anthropic_mcp.types import TextContent, Tool, ToolResult
from mem0 import Memory

# Initialize mem0
memory = Memory()

# Create MCP server
server = Server("mem0")

@server.tool()
async def add_memory(content: str, metadata: Dict[str, Any] = None) -> ToolResult:
    """Add a memory to the system"""
    result = memory.add(content, metadata=metadata)
    return ToolResult(
        content=[TextContent(text=f"Memory added: {result['id']}")]
    )

@server.tool()
async def search_memory(query: str, limit: int = 5) -> ToolResult:
    """Search memories"""
    results = memory.search(query, limit=limit)
    return ToolResult(
        content=[TextContent(text=str(results))]
    )

@server.tool()
async def get_all_memories(limit: int = 10) -> ToolResult:
    """Get all memories"""
    results = memory.get_all(limit=limit)
    return ToolResult(
        content=[TextContent(text=str(results))]
    )

if __name__ == "__main__":
    asyncio.run(server.run())
```

### Step 4: Project Configuration
```json
// .mcp/config.json
{
  "servers": {
    "mem0": {
      "command": "python3",
      "args": ["/home/user/.mcp-shared/servers/mem0-server.py"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "MEM0_STORAGE_PATH": ".mcp/storage/mem0"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

## Project Configuration

### Directory Structure
```
your-project/
├── .mcp/
│   ├── config.json         # MCP configuration
│   └── storage/           # Local storage
│       └── mem0/         # mem0 data
├── CLAUDE.md             # Project memory
└── claude               # Claude CLI wrapper
```

### Creating the Claude Wrapper
```bash
#!/bin/bash
# ./claude - Project-specific Claude wrapper

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Use Doppler if available
if command -v doppler &> /dev/null; then
    doppler run -- claude "$@"
else
    claude "$@"
fi
```

### Environment Variables
```bash
# .env (for local development)
OPENAI_API_KEY=your-key-here
PROJECT_NAME=my-awesome-project
MCP_STORAGE_PATH=.mcp/storage
```

## Using MCP with Claude

### Basic Usage
```bash
# Ask about the project
./claude "What is the architecture of this project?"

# Store information
./claude "Remember that we use PostgreSQL for the main database and Redis for caching"

# Retrieve information
./claude "What database technologies do we use?"
```

### Advanced Commands
```bash
# Search memories
./claude "Search your memory for authentication implementation"

# Analyze codebase
./claude "Analyze the dependency structure of this project"

# Bulk file operations
./claude "Rename all test files from *.test.js to *.spec.js"
```

### Best Practices
1. **Be Specific**: Give clear context for memories
2. **Regular Updates**: Keep memories current
3. **Organize Memories**: Use metadata and categories
4. **Review Periodically**: Clean up outdated memories
5. **Share Knowledge**: Export memories for team use

## Troubleshooting

### Common Issues

#### 1. MCP Server Not Starting
```bash
# Check if server is running
ps aux | grep mcp

# Check logs
tail -f ~/.mcp/logs/mem0.log

# Test server directly
python3 ~/.mcp-shared/servers/mem0-server.py
```

#### 2. API Key Issues
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test with Doppler
doppler secrets get OPENAI_API_KEY

# Check config.json
cat .mcp/config.json | grep OPENAI
```

#### 3. Memory Not Persisting
```bash
# Check storage permissions
ls -la .mcp/storage/mem0/

# Verify storage path
cat .mcp/config.json | grep STORAGE

# Test write permissions
touch .mcp/storage/mem0/test.txt
```

#### 4. Connection Timeout
```bash
# Increase timeout in config
{
  "servers": {
    "mem0": {
      "timeout": 60000  // 60 seconds
    }
  }
}
```

### Debug Mode
```bash
# Enable MCP debug logging
export MCP_DEBUG=1

# Run with verbose output
./claude --debug "Test prompt"

# Check detailed logs
cat ~/.claude/logs/mcp-debug.log
```

## Advanced Configuration

### Multiple MCP Servers
```json
// .mcp/config.json
{
  "servers": {
    "mem0": {
      "command": "python3",
      "args": ["~/.mcp-shared/servers/mem0-server.py"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Per-Project mem0 Configuration
```python
# .mcp/mem0_config.py
from mem0 import Memory

# Custom configuration
config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4",
            "temperature": 0.1
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "my_project_memories",
            "path": ".mcp/storage/mem0/chroma"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-ada-002"
        }
    }
}

memory = Memory.from_config(config)
```

### Shared vs Project Storage
```bash
# Shared storage (across projects)
~/.mem0/
└── shared/
    ├── memories.db
    └── embeddings/

# Project storage (project-specific)
.mcp/storage/mem0/
├── memories.db
├── embeddings/
└── metadata.json
```

## Creating Custom MCP Servers

### Basic Template
```python
#!/usr/bin/env python3
"""Custom MCP Server for [Your Purpose]"""

import asyncio
from anthropic_mcp.server import Server
from anthropic_mcp.types import TextContent, Tool, ToolResult

# Initialize your server
server = Server("my-custom-server")

@server.tool()
async def my_custom_tool(param1: str, param2: int = 10) -> ToolResult:
    """Description of what this tool does"""
    # Your logic here
    result = f"Processed {param1} with {param2}"
    
    return ToolResult(
        content=[TextContent(text=result)]
    )

@server.tool()
async def another_tool() -> ToolResult:
    """Another useful tool"""
    # Implementation
    return ToolResult(
        content=[TextContent(text="Tool executed successfully")]
    )

if __name__ == "__main__":
    asyncio.run(server.run())
```

### Advanced Example - Database MCP
```python
#!/usr/bin/env python3
"""Database MCP Server"""

import asyncio
import os
from typing import List, Dict, Any
import asyncpg
from anthropic_mcp.server import Server
from anthropic_mcp.types import TextContent, ToolResult

server = Server("database")

# Database connection pool
db_pool = None

async def init_db():
    global db_pool
    db_pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=10
    )

@server.tool()
async def query_database(sql: str, params: List[Any] = None) -> ToolResult:
    """Execute a database query"""
    async with db_pool.acquire() as conn:
        try:
            if params:
                results = await conn.fetch(sql, *params)
            else:
                results = await conn.fetch(sql)
            
            # Convert to list of dicts
            data = [dict(row) for row in results]
            
            return ToolResult(
                content=[TextContent(text=str(data))]
            )
        except Exception as e:
            return ToolResult(
                content=[TextContent(text=f"Error: {str(e)}")]
            )

@server.tool()
async def list_tables() -> ToolResult:
    """List all database tables"""
    sql = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    """
    return await query_database(sql)

async def main():
    await init_db()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Testing Your MCP Server
```bash
# 1. Run server directly
python3 my-mcp-server.py

# 2. Add to config
{
  "servers": {
    "my-server": {
      "command": "python3",
      "args": ["./my-mcp-server.py"]
    }
  }
}

# 3. Test with Claude
./claude "Use my custom tool to process data"
```

## Best Practices

### 1. **Security**
- Never hardcode API keys
- Use environment variables or Doppler
- Validate all inputs
- Limit permissions
- Audit tool usage

### 2. **Performance**
- Use connection pooling
- Implement caching
- Async operations
- Batch processing
- Resource limits

### 3. **Reliability**
- Error handling
- Retry logic
- Timeouts
- Health checks
- Graceful degradation

### 4. **Maintenance**
- Version your MCP servers
- Document tools clearly
- Log important operations
- Monitor usage
- Regular updates

### 5. **Team Collaboration**
- Share MCP configurations
- Document custom servers
- Standardize naming
- Central repository
- Training materials

## Example Workflows

### 1. Project Onboarding
```bash
# New developer joins
./claude "Explain the architecture and key decisions of this project"

# Claude uses mem0 to recall:
# - Architecture decisions
# - Technology choices
# - Team conventions
# - Recent changes
```

### 2. Code Review
```bash
# Before code review
./claude "Remember that we decided to use Repository pattern for data access"

# During review
./claude "Does this PR follow our established patterns?"
```

### 3. Debugging Session
```bash
# Store debugging context
./claude "Remember: The authentication bug occurs when users have special characters in passwords"

# Later debugging
./claude "What do we know about authentication bugs?"
```

### 4. Knowledge Transfer
```bash
# Export memories
./claude "Export all memories about our API design decisions"

# Import to new project
./claude "Import these API design memories: [content]"
```

---

*MCP Setup Guide v1.0 - Extending Claude's Capabilities 🚀*

*Part of the Claude Templates System*