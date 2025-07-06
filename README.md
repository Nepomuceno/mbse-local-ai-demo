# 🚀 MBSE Local AI

A demonstration of local AI integration with GitHub Copilot and specialized document processing using MCP servers.

## Overview

This project demonstrates the integration of local AI models with development tools and specialized document processing capabilities. It provides a practical example of how to enhance developer workflows while maintaining data privacy and offline functionality.

The project includes two main components:

1. **🔄 Local AI Integration**: A local AI system that intercepts GitHub Copilot requests and routes them to local models (Ollama) with Azure OpenAI fallback, providing enhanced privacy and offline capabilities.

2. **🧠 MCP Server**: A Model Context Protocol server that processes PYRAMID specification documents and provides specialized knowledge for systems engineering requirements analysis.

## ✨ Features

- **🏠 Local AI Integration**: Complete setup for routing GitHub Copilot requests to local models
- **🤖 MCP Server**: Model Context Protocol server for specialized document processing
- **📋 PYRAMID Specification Support**: Process and analyze PYRAMID technical standard documents
- **🌐 Offline Capabilities**: Runs completely offline while enhancing developer capabilities
- **🚀 Development Container**: Pre-configured development environment with VS Code integration
- **🔧 Extensible Architecture**: Designed to be extended with additional AI models and document types

## 🛠️ Requirements

- **Git LFS**: Required for handling large PYRAMID specification documents
- Python 3.12+
- Docker and Docker Compose
- MCP (Model Context Protocol) Python SDK
- UV (for dependency management)
- VS Code with dev container support

### 🎪 Git LFS Setup

This project uses Git LFS (Large File Storage) to handle large PDF documents in the `mcp_server/data/` directory.

#### First-time Git LFS Setup

```bash
# Install Git LFS (if not already installed)
# On Ubuntu/Debian:
sudo apt-get install git-lfs

# On macOS:
brew install git-lfs

# On Windows:
# Download from: https://git-lfs.github.io/

# Initialize Git LFS for your user account
git lfs install
```

#### Working with this Repository

```bash
# Clone the repository (Git LFS files will be downloaded automatically)
git clone <repository-url>
cd mbse-local-ai

# If you cloned before LFS setup, pull LFS files:
git lfs pull

# Check LFS status
git lfs ls-files
```

**Note**: The dev container automatically configures Git LFS.

## 🚀 Installation

### Method 1: Quick Start with Dev Container (Recommended)

1. **Prerequisites**: Ensure Git LFS is installed and configured (see requirements above)

2. **Clone Repository**: 
   ```bash
   git clone <repository-url>
   cd mbse-local-ai
   ```

3. **Open in Dev Container**: Open the project in VS Code and select "Reopen in Container" when prompted. The dev container will automatically:
   - Install Git LFS and configure it
   - Install all dependencies
   - Configure the MCP server
   - Set up the complete development environment

4. **Setup Local AI (Optional)**: Follow the guide in `local-config/README.md` to set up the local AI system.

### Method 2: Manual Installation

```bash
# Ensure Git LFS is installed and configured
git lfs install

# Clone the repository
git clone <repository-url>
cd mbse-local-ai

# Pull LFS files if needed
git lfs pull

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## 🎮 Usage

### 🔧 Local AI Setup

Configure GitHub Copilot to use local AI models:

1. **Follow Setup Guide**: See `local-config/README.md` for complete instructions
2. **Start Local Services**: Run `docker-compose up -d` in the `local-config` directory
3. **Configure Hosts**: Modify your hosts file to redirect OpenAI API calls to local setup

### 🧠 MCP Server for Document Processing

Run the MCP server to process PYRAMID specification documents:

```bash
# Start the MCP server
python mcp_server/server.py
```

The MCP server provides tools for:
- **📋 Document Analysis**: Process PYRAMID technical standard documents
- **✅ Compliance Tools**: Check requirements against PYRAMID specifications
- **🔍 PRA Analysis**: Analyze component impact for requirements changes
- **📁 File Processing**: Handle large PDF documents with metadata extraction

### 🎪 Demo Examples

The `demo/` folder contains a sample requirement diagram in Mermaid format. Try asking the MCP server to:

- 🌡️ "Add temperature monitoring and alerts to the fuel reading requirement"
- 🔍 "Identify which components would be impacted by adding temperature sensors"
- 📋 "Modify the requirements to include engine temperature limits while maintaining the Mermaid diagram format"
- 📊 "Perform a PRA analysis for the temperature alert requirement changes"

## 🤖 MCP Server Integration

The MCP server provides specialized knowledge processing for PYRAMID specifications and systems engineering documents. It runs completely offline while enhancing developer capabilities.

### 🎯 MCP Server Features

- **📄 Document Processing**: Extract and analyze PYRAMID technical standard documents
- **✅ Compliance Analysis**: Check requirements against PYRAMID specifications
- **📊 PRA Tools**: Perform Probabilistic Risk Assessment for component changes
- **📋 PDF Processing**: Handle large PDF documents with metadata extraction
- **🔧 Requirements Modification**: Modify system requirements while maintaining traceability

### 🚀 Using MCP Server in VS Code

1. **⚡ Auto-Configuration**: The MCP server is pre-configured in the dev container
2. **🤖 Agent Mode**: Open Chat (⌃⌘I), select "Agent" mode, and click "Tools"
3. **🎯 Specialized Queries**: Ask questions about PYRAMID specifications or requirements analysis

### 🎪 Example MCP Queries

- 📋 "List all PYRAMID documents in the data directory"
- 🔍 "Analyze the fuel monitoring requirements and suggest temperature integration"
- 🤔 "What components would be affected by adding temperature sensors to the fuel system?"
- 📊 "Modify the requirements to include engine temperature monitoring while preserving the Mermaid diagram structure"

## 🛠️ Development

### 🚀 Development Container

Run the project from the supplied dev container:

- **🌟 Complete Environment**: Python 3.12, UV, Docker, Git LFS, and all dependencies pre-installed
- **🔧 VS Code Extensions**: Pre-configured with Python, Mermaid, Copilot, and MCP support
- **⚡ Auto-Setup**: Automatic dependency installation, Git LFS configuration, and MCP server setup
- **🌐 Offline Capable**: Full functionality without internet access once configured
- **📋 LFS Support**: Automatic Git LFS initialization and configuration for large documents

### 🏗️ Project Structure

```
mbse-local-ai/
├── .devcontainer/            # Complete dev container setup
├── .vscode/                  # VS Code configuration with MCP enabled
├── mcp_server/               # MCP server for document processing
│   ├── server.py            # Main MCP server implementation
│   ├── document_parser.py   # Document processing utilities
│   ├── pdf_processor.py     # PDF handling and metadata extraction
│   ├── data/                # PYRAMID specification documents
│   └── tools/               # Specialized tools (compliance, PRA, documents)
├── demo/                     # Sample requirements in Mermaid format
│   └── requirement.mmd      # Example fuel monitoring system requirements
├── local-config/            # Local AI setup for GitHub Copilot
│   ├── docker-compose.yaml # LiteLLM and Caddy proxy setup
│   ├── Caddyfile           # Reverse proxy configuration
│   └── README.md           # Complete setup instructions
└── pyproject.toml          # Project configuration
```

## ⚙️ Configuration

### 🚀 Local AI Configuration

The `local-config/` directory contains complete setup for GitHub Copilot local AI integration:

- **🐳 Docker Compose**: LiteLLM server with Ollama integration and Azure OpenAI fallback
- **🔄 Caddy Proxy**: SSL-enabled reverse proxy for intercepting OpenAI API calls
- **🔒 SSL Certificates**: Pre-configured certificates for `api.openai.com` interception
- **⚙️ Configuration Files**: Multiple LiteLLM configurations for different use cases

### 🤖 MCP Server Configuration

The MCP server is automatically configured in `.vscode/mcp.json` for seamless VS Code integration with specialized tools for PYRAMID document processing and requirements analysis.

---

## Summary

This project provides a practical example of integrating local AI models with development workflows while maintaining privacy and offline capabilities. The combination of local AI processing, specialized document handling, and developer-friendly tools demonstrates how to build enhanced development environments.

The project is designed to be extended and modified for different use cases and document types.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
