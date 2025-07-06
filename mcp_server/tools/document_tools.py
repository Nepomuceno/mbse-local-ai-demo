"""
Document Tools for PYRAMID MCP Server

This module provides fundamental document access capabilities for PYRAMID Technical Standard documentation.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Import the existing processors
from mcp_server.pdf_processor import PDFProcessor, PDFProcessingError
from mcp_server.document_parser import DocumentParser

logger = logging.getLogger(__name__)

# Global processors (will be initialized by server)
pdf_processor: Optional[PDFProcessor] = None
document_parser: Optional[DocumentParser] = None
data_dir: Optional[Path] = None


def initialize_document_tools(data_directory: Path, pdf_proc: PDFProcessor, doc_parser: DocumentParser):
    """Initialize the document tools with processors and data directory."""
    global pdf_processor, document_parser, data_dir
    pdf_processor = pdf_proc
    document_parser = doc_parser
    data_dir = data_directory


def list_pyramid_documents() -> Dict[str, Any]:
    """
    List available PYRAMID documents with metadata.

    Returns:
        Dict containing information about available PYRAMID documents
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "directory": str(data_dir) if data_dir else None,
                "documents": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "directory": str(data_dir) if data_dir else None,
                "documents": []
            }

        documents = []
        pdf_files = list(data_dir.glob("*.pdf"))

        for pdf_file in pdf_files:
            try:
                # Extract basic metadata
                content = pdf_processor.extract_pdf_content(pdf_file, 1, 1)

                # Parse document type from filename
                doc_type = "Unknown"
                if "Technical_Standard_Guidance" in pdf_file.name:
                    doc_type = "Technical Standard Guidance"
                elif "Technical_Standard" in pdf_file.name:
                    doc_type = "Technical Standard"
                elif "VDD" in pdf_file.name:
                    doc_type = "VDD (Version Description Document)"

                # Extract version information from filename
                version_match = re.search(r'V(\d+(?:\.\d+)*)', pdf_file.name)
                version = version_match.group(
                    1) if version_match else "Unknown"

                # Extract date from filename
                date_match = re.search(r'(\d{8})', pdf_file.name)
                date_str = date_match.group(1) if date_match else None

                document_info = {
                    "file_name": pdf_file.name,
                    "file_path": str(pdf_file),
                    "document_type": doc_type,
                    "version": version,
                    "date_from_filename": date_str,
                    "file_size": pdf_file.stat().st_size,
                    "page_count": content.metadata.page_count,
                    "title": content.metadata.title,
                    "author": content.metadata.author,
                    "creation_date": content.metadata.creation_date.isoformat() if content.metadata.creation_date else None,
                    "modification_date": content.metadata.modification_date.isoformat() if content.metadata.modification_date else None,
                    "is_pyramid_document": True
                }

                documents.append(document_info)

            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {e}")
                # Add minimal info for failed documents
                documents.append({
                    "file_name": pdf_file.name,
                    "file_path": str(pdf_file),
                    "error": f"Failed to process: {str(e)}",
                    "is_pyramid_document": True
                })

        # Sort by date (newest first)
        documents.sort(key=lambda x: x.get(
            "date_from_filename", "0"), reverse=True)

        return {
            "success": True,
            "directory": str(data_dir),
            "total_documents": len(documents),
            "documents": documents
        }

    except Exception as e:
        logger.error(f"Error listing PYRAMID documents: {e}")
        return {
            "error": f"Failed to list documents: {str(e)}",
            "directory": str(data_dir) if data_dir else None,
            "documents": []
        }


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
    try:
        if not data_dir:
            return {
                "error": "Data directory not initialized",
                "file_path": file_path
            }

        if not pdf_processor or not document_parser:
            return {
                "error": "PDF processor or document parser not initialized",
                "file_path": file_path
            }

        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = data_dir / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Parse page range
        start_page = 1
        end_page = None

        if page_range:
            if "-" in page_range:
                # Range like "1-10"
                parts = page_range.split("-")
                if len(parts) == 2:
                    start_page = int(parts[0])
                    end_page = int(parts[1])
            else:
                # Single page like "5"
                start_page = int(page_range)
                end_page = start_page

        # Extract content
        content = pdf_processor.extract_pdf_content(
            resolved_path, start_page, end_page)

        # Apply section filtering if specified
        filtered_text = content.text
        if section_filter:
            # Get document structure
            structure = document_parser.parse_document_structure(resolved_path)

            # Find matching sections
            matching_sections = []
            for section in structure.sections:
                if section_filter.lower() in section.title.lower():
                    matching_sections.append(section)

            if matching_sections:
                # Extract text from matching sections
                filtered_parts = []
                for section in matching_sections:
                    filtered_parts.append(f"=== {section.title} ===")
                    filtered_parts.append(section.text_content)
                filtered_text = "\n\n".join(filtered_parts)

        return {
            "success": True,
            "file_path": str(resolved_path),
            "file_name": resolved_path.name,
            "page_range": page_range or f"1-{content.metadata.page_count}",
            "section_filter": section_filter,
            "text": filtered_text,
            "text_length": len(filtered_text),
            "total_pages": content.metadata.page_count,
            "extraction_timestamp": content.extraction_timestamp.isoformat()
        }

    except ValueError as e:
        return {
            "error": f"Invalid page range format: {page_range}",
            "file_path": file_path
        }
    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Error reading PDF content: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


def get_document_metadata(file_path: str) -> Dict[str, Any]:
    """
    Get document information and structure metadata.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing document metadata
    """
    try:
        if not data_dir:
            return {
                "error": "Data directory not initialized",
                "file_path": file_path
            }

        if not pdf_processor or not document_parser:
            return {
                "error": "PDF processor or document parser not initialized",
                "file_path": file_path
            }

        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = data_dir / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Extract metadata
        content = pdf_processor.extract_pdf_content(resolved_path, 1, 1)

        # Get document structure
        structure = document_parser.parse_document_structure(resolved_path)

        # Parse document type and version from filename
        doc_type = "Unknown"
        if "Technical_Standard_Guidance" in resolved_path.name:
            doc_type = "Technical Standard Guidance"
        elif "Technical_Standard" in resolved_path.name:
            doc_type = "Technical Standard"
        elif "VDD" in resolved_path.name:
            doc_type = "VDD (Version Description Document)"

        version_match = re.search(r'V(\d+(?:\.\d+)*)', resolved_path.name)
        version = version_match.group(1) if version_match else "Unknown"

        date_match = re.search(r'(\d{8})', resolved_path.name)
        date_str = date_match.group(1) if date_match else None

        return {
            "success": True,
            "file_path": str(resolved_path),
            "file_name": resolved_path.name,
            "document_type": doc_type,
            "version": version,
            "date_from_filename": date_str,
            "metadata": {
                "title": content.metadata.title,
                "author": content.metadata.author,
                "subject": content.metadata.subject,
                "creator": content.metadata.creator,
                "producer": content.metadata.producer,
                "creation_date": content.metadata.creation_date.isoformat() if content.metadata.creation_date else None,
                "modification_date": content.metadata.modification_date.isoformat() if content.metadata.modification_date else None,
                "page_count": content.metadata.page_count,
                "file_size": content.metadata.file_size,
                "is_encrypted": content.metadata.is_encrypted,
                "is_pdf_a": content.metadata.is_pdf_a,
                "has_forms": content.metadata.has_forms,
                "has_bookmarks": content.metadata.has_bookmarks
            },
            "structure": {
                "total_sections": structure.total_sections,
                "max_depth": structure.max_depth,
                "section_numbering_scheme": structure.section_numbering_scheme,
                # First 10 sections
                "section_titles": [section.title for section in structure.sections[:10]]
            }
        }

    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Error getting document metadata: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


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
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "query": query,
                "results": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "query": query,
                "results": []
            }

        results = []
        pdf_files = list(data_dir.glob("*.pdf"))

        # Filter documents if specified
        if doc_filter:
            filtered_files = []
            for pdf_file in pdf_files:
                if doc_filter.lower() in pdf_file.name.lower():
                    filtered_files.append(pdf_file)
            pdf_files = filtered_files

        # Search in each document
        for pdf_file in pdf_files:
            try:
                # Extract content
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Search in text (case-insensitive)
                text_lower = content.text.lower()
                query_lower = query.lower()

                # Find matches
                matches = []
                start_pos = 0
                while len(matches) < max_results:
                    pos = text_lower.find(query_lower, start_pos)
                    if pos == -1:
                        break

                    # Extract context around match
                    context_start = max(0, pos - 150)
                    context_end = min(len(content.text),
                                      pos + len(query) + 150)
                    context = content.text[context_start:context_end]

                    # Estimate page number
                    page_num = 1
                    char_count = 0
                    for page_meta in content.pages:
                        if char_count + page_meta.text_length > pos:
                            break
                        char_count += page_meta.text_length
                        page_num += 1

                    matches.append({
                        "position": pos,
                        "context": context,
                        "page_estimate": min(page_num, content.metadata.page_count)
                    })

                    start_pos = pos + 1

                if matches:
                    # Calculate relevance score (simple word count)
                    relevance_score = len(matches) + (
                        10 if query_lower in pdf_file.name.lower() else 0
                    )

                    results.append({
                        "file_path": str(pdf_file),
                        "file_name": pdf_file.name,
                        "relevance_score": relevance_score,
                        "total_matches": len(matches),
                        # Limit to first 5 matches per document
                        "matches": matches[:5]
                    })

            except Exception as e:
                logger.error(f"Error searching in {pdf_file}: {e}")
                continue

        # Sort by relevance score (highest first)
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return {
            "success": True,
            "query": query,
            "doc_filter": doc_filter,
            "total_files_searched": len(pdf_files),
            "files_with_matches": len(results),
            "results": results[:max_results]
        }

    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "query": query,
            "results": []
        }


def get_document_outline(file_path: str) -> Dict[str, Any]:
    """
    Extract document structure/table of contents.

    Args:
        file_path: Path to the PDF file (relative to data directory or absolute)

    Returns:
        Dict containing document outline
    """
    try:
        if not data_dir:
            return {
                "error": "Data directory not initialized",
                "file_path": file_path
            }

        if not document_parser:
            return {
                "error": "Document parser not initialized",
                "file_path": file_path
            }

        # Resolve file path
        if not os.path.isabs(file_path):
            resolved_path = data_dir / file_path
        else:
            resolved_path = Path(file_path)

        if not resolved_path.exists():
            return {
                "error": f"File not found: {file_path}",
                "file_path": str(resolved_path)
            }

        # Parse document structure
        structure = document_parser.parse_document_structure(resolved_path)

        # Convert to outline format
        def create_outline_item(section):
            return {
                "title": section.title,
                "level": section.level,
                "section_number": section.section_number,
                "page_start": section.page_start,
                "page_end": section.page_end,
                "section_type": section.section_type.value,
                "subsections": [create_outline_item(sub) for sub in section.subsections]
            }

        outline = [create_outline_item(section)
                   for section in structure.sections]

        return {
            "success": True,
            "file_path": str(resolved_path),
            "file_name": resolved_path.name,
            "structure": {
                "total_sections": structure.total_sections,
                "max_depth": structure.max_depth,
                "section_numbering_scheme": structure.section_numbering_scheme,
                "outline": outline
            }
        }

    except PDFProcessingError as e:
        return {
            "error": f"PDF processing error: {str(e)}",
            "file_path": file_path
        }
    except Exception as e:
        logger.error(f"Error getting document outline: {e}")
        return {
            "error": f"Unexpected error: {str(e)}",
            "file_path": file_path
        }


# Export functions
__all__ = [
    'initialize_document_tools',
    'list_pyramid_documents',
    'read_pdf_content',
    'get_document_metadata',
    'search_documents',
    'get_document_outline'
]
