# MBSE Local AI MCP Server

This Model Context Protocol (MCP) server is specifically designed to provide intelligent access to **PYRAMID Technical Standard documentation** and related Model-Based Systems Engineering (MBSE) resources. PYRAMID is a reusable and open avionics system reference architecture developed by the UK Ministry of Defence (MOD) that aims to make legacy and future air mission systems affordable, capable, and adaptable through open systems architecture.

## Overview

The server provides specialized tools for accessing and analyzing PYRAMID documentation, including:

- **PYRAMID Technical Standard V1.0** - Defines the PYRAMID Reference Architecture (PRA) and compliance rules
- **PYRAMID Technical Standard Guidance V1.0** - Provides guidance on understanding and applying the standard
- **Version Description Documents** - Details changes and updates to the documentation

## Key Features

### Document Access & Analysis
- **PDF Document Reading**: Extract and search text content from PYRAMID PDF documents
- **Semantic Search**: Intelligent search across PYRAMID documentation using natural language queries
- **Content Extraction**: Retrieve specific sections, concepts, and guidance from the technical standards
- **Metadata Analysis**: Access document structure, sections, and cross-references

### PYRAMID-Specific Tools
- **Compliance Guidance**: Access rules and guidance for achieving PYRAMID compliance
- **Component Information**: Retrieve details about PYRAMID Reference Architecture components
- **Interaction Views**: Access examples of how components integrate for specific scenarios
- **Deployment Guidance**: Get engineering guidance for PYRAMID-based system development

### File Management
- **Document Listing**: Browse available PYRAMID documents and resources
- **Version Tracking**: Access different versions of PYRAMID documentation
- **Search by Topic**: Find relevant sections based on MBSE concepts and requirements

## Available Documents

The server provides access to the following PYRAMID documentation:

1. **PYRAMID Technical Standard V1.0** (20250224-PYRAMID_Technical_Standard_V1-O.pdf)
   - 1,513 pages of technical specifications
   - PYRAMID Reference Architecture (PRA) definitions
   - Compliance rules and requirements

2. **PYRAMID Technical Standard Guidance V1.0** (20250224-PYRAMID_Technical_Standard_Guidance_V1-O.pdf)
   - 571 pages of implementation guidance
   - PYRAMID Concepts and Interaction Views
   - Deployment and Compliance guides

3. **Version Description Documents** (Issue 1.0)
   - Change documentation and updates
   - Restructuring information
   - Migration from previous versions

## Use Cases

This MCP server is designed for:

- **Systems Engineers** implementing PYRAMID-compliant systems
- **Acquisition Teams** requiring PYRAMID compliance verification
- **Integrators** developing components for PYRAMID architectures
- **Researchers** studying open systems architecture approaches
- **AI Agents** needing access to structured PYRAMID knowledge

## Technology Stack

- **Python 3.12+** with FastMCP framework
- **PyMuPDF (fitz)** for PDF processing and text extraction
- **Advanced NLP libraries** for semantic search and content analysis
- **Structured data extraction** for PYRAMID-specific concepts

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install PyMuPDF fastmcp python-dotenv
   ```

2. **Configure Environment**:
   - Place PYRAMID PDF documents in the `data/` directory
   - Configure MCP client to connect to this server

3. **Run the Server**:
   ```bash
   python mcp_server/server.py
   ```

## MCP Tools Available

### Core Document Tools
- `list_files()` - List available PYRAMID documents
- `read_pdf_content(file_path, page_range)` - Extract text from PDF pages
- `search_documents(query, doc_filter)` - Search across all documents
- `get_document_metadata(file_path)` - Get document information and structure

### PYRAMID-Specific Tools
- `get_compliance_rules(category)` - Retrieve compliance guidance
- `search_components(component_type)` - Find PRA component information
- `get_interaction_views(scenario)` - Access integration examples
- `extract_concepts(topic)` - Get PYRAMID concept definitions

### Analysis Tools
- `analyze_document_structure(file_path)` - Parse document sections
- `find_cross_references(term)` - Locate related content
- `extract_requirements(section)` - Get requirement specifications
- `get_implementation_guidance(topic)` - Access deployment advice

## Configuration

The server can be configured through environment variables:

- `PYRAMID_DATA_DIR`: Directory containing PYRAMID documents (default: `./data`)
- `MAX_CONTENT_LENGTH`: Maximum content length per response (default: 10000)
- `SEARCH_RESULTS_LIMIT`: Maximum search results returned (default: 50)
- `ENABLE_SEMANTIC_SEARCH`: Enable advanced semantic search (default: true)

## Integration with MCP Clients

This server is designed to work with MCP-compatible clients and can be integrated into:

- **Claude Desktop** - For interactive PYRAMID documentation access
- **VS Code Extensions** - For development environment integration
- **Custom Applications** - Via the MCP protocol
- **AI Agent Frameworks** - For automated PYRAMID compliance checking

## Contributing

This server is focused on PYRAMID documentation access and MBSE workflows. Contributions should maintain this focus and enhance the server's ability to provide accurate, structured access to PYRAMID technical standards.
