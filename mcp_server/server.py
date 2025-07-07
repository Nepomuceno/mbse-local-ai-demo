#!/usr/bin/env python3
"""
MBSE Local AI MCP Server

A comprehensive MCP server specialized for accessing and analyzing 
PYRAMID Technical Standard documentation. This server provides intelligent 
access to PYRAMID documentation, enabling AI agents and applications to 
understand and work with PYRAMID compliance requirements, reference 
architecture components, and implementation guidance.
"""

from mcp_server.utils.document_parser import DocumentParser
from mcp_server.utils.pdf_processor import PDFProcessor, PDFProcessingError
from tools.document_tools import initialize_document_tools
from tools.pra_tools import initialize_pra_tools
from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("PYRAMID MCP Server")

# Define the data directory
DATA_DIR = Path(__file__).parent / "data"

# Initialize processors
pdf_processor = PDFProcessor()
document_parser = DocumentParser()

# Initialize tools

initialize_document_tools(DATA_DIR, pdf_processor, document_parser)
initialize_pra_tools(DATA_DIR, pdf_processor, document_parser)


@mcp.tool()
def list_files() -> Dict[str, Any]:
    """
    List all files in the MCP server data directory.

    Returns:
        Dict containing information about files in the data directory
    """
    try:
        if not DATA_DIR.exists():
            return {
                "error": "Data directory does not exist",
                "directory": str(DATA_DIR),
                "files": []
            }

        files = []
        for file_path in DATA_DIR.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "extension": file_path.suffix.lower()
                })

        return {
            "directory": str(DATA_DIR),
            "total_files": len(files),
            "files": files
        }

    except Exception as e:
        return {
            "error": f"Failed to list files: {str(e)}",
            "directory": str(DATA_DIR),
            "files": []
        }


@mcp.tool()
def extract_pdf_content(
    file_path: str,
    start_page: int = 1,
    end_page: Optional[int] = None
) -> Dict[str, Any]:
    """
    Extract comprehensive content from a PDF file with metadata.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)
        start_page: Starting page number (1-based, default: 1)
        end_page: Ending page number (1-based, inclusive, default: all pages)

    Returns:
        Dict containing extracted text, metadata, and structure information
    """
    try:
        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = DATA_DIR / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Extract content using PDF processor
        content = pdf_processor.extract_pdf_content(
            resolved_path, start_page, end_page)

        # Convert to JSON-serializable format
        return {
            "success": True,
            "file_path": str(resolved_path),
            "text": content.text,
            "metadata": {
                "file_path": content.metadata.file_path,
                "file_size": content.metadata.file_size,
                "page_count": content.metadata.page_count,
                "title": content.metadata.title,
                "author": content.metadata.author,
                "subject": content.metadata.subject,
                "creator": content.metadata.creator,
                "producer": content.metadata.producer,
                "creation_date": content.metadata.creation_date.isoformat() if content.metadata.creation_date else None,
                "modification_date": content.metadata.modification_date.isoformat() if content.metadata.modification_date else None,
                "is_encrypted": content.metadata.is_encrypted,
                "is_pdf_a": content.metadata.is_pdf_a,
                "has_forms": content.metadata.has_forms,
                "has_bookmarks": content.metadata.has_bookmarks
            },
            "structure": {
                "sections": content.structure.sections,
                "headers": content.structure.headers,
                "bookmarks": content.structure.bookmarks,
                "page_labels": content.structure.page_labels
            },
            "pages": [
                {
                    "page_number": page.page_number,
                    "width": page.width,
                    "height": page.height,
                    "rotation": page.rotation,
                    "text_length": page.text_length,
                    "has_images": page.has_images,
                    "has_links": page.has_links
                }
                for page in content.pages
            ],
            "extraction_timestamp": content.extraction_timestamp.isoformat(),
            "page_range": f"{start_page}-{end_page or content.metadata.page_count}"
        }

    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Unexpected error in extract_pdf_content: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


@mcp.tool()
def get_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive metadata from a PDF file.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing PDF metadata
    """
    try:
        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = DATA_DIR / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Extract just metadata (first page only for efficiency)
        content = pdf_processor.extract_pdf_content(resolved_path, 1, 1)

        return {
            "success": True,
            "file_path": str(resolved_path),
            "metadata": {
                "file_path": content.metadata.file_path,
                "file_size": content.metadata.file_size,
                "page_count": content.metadata.page_count,
                "title": content.metadata.title,
                "author": content.metadata.author,
                "subject": content.metadata.subject,
                "creator": content.metadata.creator,
                "producer": content.metadata.producer,
                "creation_date": content.metadata.creation_date.isoformat() if content.metadata.creation_date else None,
                "modification_date": content.metadata.modification_date.isoformat() if content.metadata.modification_date else None,
                "is_encrypted": content.metadata.is_encrypted,
                "is_pdf_a": content.metadata.is_pdf_a,
                "has_forms": content.metadata.has_forms,
                "has_bookmarks": content.metadata.has_bookmarks
            }
        }

    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_pdf_metadata: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


@mcp.tool()
def get_document_structure(file_path: str) -> Dict[str, Any]:
    """
    Parse and return the hierarchical structure of a PDF document.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing document structure with sections, headers, and hierarchy
    """
    try:
        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = DATA_DIR / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Parse document structure
        outline = document_parser.parse_document_structure(resolved_path)

        # Convert to JSON-serializable format
        def serialize_section(section):
            return {
                "title": section.title,
                "section_type": section.section_type.value,
                "level": section.level,
                "page_start": section.page_start,
                "page_end": section.page_end,
                "section_number": section.section_number,
                "parent_section": section.parent_section,
                "subsections": [serialize_section(sub) for sub in section.subsections],
                "text_content": section.text_content[:500] + "..." if len(section.text_content) > 500 else section.text_content
            }

        return {
            "success": True,
            "file_path": str(resolved_path),
            "structure": {
                "sections": [serialize_section(section) for section in outline.sections],
                "total_sections": outline.total_sections,
                "max_depth": outline.max_depth,
                "section_numbering_scheme": outline.section_numbering_scheme
            }
        }

    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_document_structure: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


@mcp.tool()
def extract_images_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata about images contained in a PDF file.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing image metadata information
    """
    try:
        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = DATA_DIR / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Extract image metadata
        images_metadata = pdf_processor.extract_images_metadata(resolved_path)

        return {
            "success": True,
            "file_path": str(resolved_path),
            "total_images": len(images_metadata),
            "images": images_metadata
        }

    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Unexpected error in extract_images_metadata: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


@mcp.tool()
def search_pdf_content(
    query: str,
    file_path: Optional[str] = None,
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Search for text content within PDF files.

    Args:
        query: Text to search for
        file_path: Specific file to search in (optional, searches all PDFs if not provided)
        case_sensitive: Whether to perform case-sensitive search

    Returns:
        Dict containing search results with context
    """
    try:
        results = []

        # Determine files to search
        if file_path:
            # Search specific file
            if not os.path.isabs(file_path):
                resolved_path = DATA_DIR / file_path
            else:
                resolved_path = Path(file_path)

            if not resolved_path.exists():
                return {
                    "error": f"File not found: {file_path}",
                    "file_path": str(resolved_path)
                }

            search_files = [resolved_path]
        else:
            # Search all PDF files in data directory
            search_files = list(DATA_DIR.glob("*.pdf"))

        # Perform search
        for pdf_path in search_files:
            try:
                # Extract content
                content = pdf_processor.extract_pdf_content(pdf_path)

                # Search in text
                search_text = content.text if case_sensitive else content.text.lower()
                search_query = query if case_sensitive else query.lower()

                # Find matches
                matches = []
                start_pos = 0
                while True:
                    pos = search_text.find(search_query, start_pos)
                    if pos == -1:
                        break

                    # Extract context around match
                    context_start = max(0, pos - 100)
                    context_end = min(len(search_text), pos +
                                      len(search_query) + 100)
                    context = content.text[context_start:context_end]

                    # Try to determine page number (rough estimate)
                    page_num = 1
                    for page_meta in content.pages:
                        if pos < page_meta.text_length:
                            break
                        page_num += 1

                    matches.append({
                        "position": pos,
                        "context": context,
                        "page_estimate": min(page_num, content.metadata.page_count)
                    })

                    start_pos = pos + 1

                if matches:
                    results.append({
                        "file_path": str(pdf_path),
                        "file_name": pdf_path.name,
                        "total_matches": len(matches),
                        # Limit to first 10 matches per file
                        "matches": matches[:10]
                    })

            except Exception as e:
                logger.error(f"Error searching in {pdf_path}: {e}")
                continue

        return {
            "success": True,
            "query": query,
            "case_sensitive": case_sensitive,
            "total_files_searched": len(search_files),
            "files_with_matches": len(results),
            "results": results
        }

    except Exception as e:
        logger.error(f"Unexpected error in search_pdf_content: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "query": query
        }


# =============================================================================
# PYRAMID-Specific Tools
# =============================================================================

@mcp.tool()
def list_pyramid_documents() -> Dict[str, Any]:
    """
    List available PYRAMID documents with metadata.

    Returns:
        Dict containing information about available PYRAMID documents
    """
    from tools.document_tools import list_pyramid_documents
    return list_pyramid_documents()


@mcp.tool()
def read_pdf_content(
    file_path: str,
    page_range: Optional[str] = None,
    section_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract PDF content with support for page ranges and section filtering.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)
        page_range: Page range (e.g., "1-10", "25-30", "5") - optional
        section_filter: Section name filter (e.g., "Compliance Rules", "Component Definitions") - optional

    Returns:
        Dict containing extracted content
    """
    from tools.document_tools import read_pdf_content
    return read_pdf_content(file_path, page_range, section_filter)


@mcp.tool()
def get_document_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get document information and structure metadata.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing document metadata
    """
    from tools.document_tools import get_document_metadata
    return get_document_metadata(file_path)


@mcp.tool()
def search_documents(
    query: str,
    doc_filter: Optional[str] = None,
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search across PYRAMID documents with filtering and relevance scoring.

    Args:
        query: Search query text
        doc_filter: Document type filter (e.g., "Technical Standard", "Guidance")
        max_results: Maximum number of results to return

    Returns:
        Dict containing search results
    """
    from tools.document_tools import search_documents
    return search_documents(query, doc_filter, max_results)


@mcp.tool()
def get_document_outline(file_path: str) -> Dict[str, Any]:
    """
    Extract document structure/table of contents.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing document outline
    """
    from tools.document_tools import get_document_outline
    return get_document_outline(file_path)


@mcp.tool()
def search_pra_components(
    component_type: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find PRA components by type and category.

    Args:
        component_type: Type of component (e.g., "Core", "Optional", "Interface")
        category: Category filter (e.g., "Data", "Communication", "Security")

    Returns:
        Dict containing matching PRA components
    """
    from tools.pra_tools import search_pra_components
    return search_pra_components(component_type, category)


@mcp.tool()
def get_pra_component_details(component_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific PRA component.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing detailed component information
    """
    from tools.pra_tools import get_component_details
    return get_component_details(component_id)


@mcp.tool()
def search_pra_component_relationships(component_id: str) -> Dict[str, Any]:
    """
    Find relationships between components.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing component relationships
    """
    from tools.pra_tools import search_component_relationships
    return search_component_relationships(component_id)


@mcp.tool()
def get_pra_component_owners(component_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get component ownership and responsibility information.

    Args:
        component_id: Specific component to get ownership for, or None for all components

    Returns:
        Dict containing component ownership information including responsible people and sectors
    """
    from tools.pra_tools import get_component_owners
    return get_component_owners(component_id)


@mcp.tool()
def get_components_by_responsible_person(person_name: str) -> Dict[str, Any]:
    """
    Get components associated with a specific person (owner, lead, etc.).

    Args:
        person_name: Name of the person to search for

    Returns:
        Dict containing components associated with the person
    """
    from tools.pra_tools import get_components_by_responsible_person
    return get_components_by_responsible_person(person_name)


@mcp.tool()
def get_components_by_sector(sector: str) -> Dict[str, Any]:
    """
    Get components associated with a specific sector.

    Args:
        sector: Name of the sector to search for (e.g., "Defence", "Cybersecurity", "Data")

    Returns:
        Dict containing components associated with the sector
    """
    from tools.pra_tools import get_components_by_sector
    return get_components_by_sector(sector)


def main():
    """Main entry point for the MCP server."""
    logger.info("Starting PYRAMID MCP Server...")
    logger.info(f"Data directory: {DATA_DIR}")
    logger.info("Available tools:")
    logger.info("Phase 1: Basic PDF processing (6 tools)")
    logger.info("Phase 2: PYRAMID-specific tools (18 tools)")
    logger.info("  - Document Access: 5 tools")
    logger.info("  - Compliance: 5 tools")
    logger.info("  - PRA Components: 5 tools")
    logger.info("  - Component Ownership: 3 tools")
    mcp.run()


if __name__ == "__main__":
    main()
