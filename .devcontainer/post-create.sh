#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Initialize Git LFS if not already done
echo "📦 Initializing Git LFS..."
git lfs install

echo "🔄 Installing Git LFS hooks..."
git lfs install --local

# Create UV virtual environment
echo "📦 Creating UV virtual environment..."
uv venv

# Activate the environment and install dependencies
echo "🔄 Installing dependencies..."
source .venv/bin/activate
uv pip install -e .

# Verify the installation
echo "✅ Verifying installation..."
source .venv/bin/activate
python --version
pip list

# Test that FastAPI and uvicorn are working
echo "🧪 Testing FastAPI installation..."
python -c "import fastapi; import uvicorn; print('✅ FastAPI and uvicorn are working!')"

# Test that MCP is working
echo "🧪 Testing MCP installation..."
python -c "import mcp; print('✅ MCP is working!')"
python -c "from mcp.server.fastmcp import FastMCP; print('✅ FastMCP is working!')"

# Test the MCP server file listing tool
echo "🧪 Testing MCP server list_files tool..."
python -c "
import sys
sys.path.insert(0, '/workspaces/mbse-local-ai')
from mcp_server.server import list_files
result = list_files()
print('✅ MCP server is working!')
print(f'Found {result.get(\"total_files\", 0)} files in data directory')
if result.get('files'):
    for file in result['files']:
        print(f'  - {file[\"name\"]} ({file[\"size\"]} bytes)')
"

echo "🎉 Setup complete! Virtual environment is ready."
