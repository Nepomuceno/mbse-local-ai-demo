"""
PDF Processing Utilities for PYRAMID MCP Server

This module provides comprehensive PDF text extraction and processing capabilities
using PyMuPDF (fitz) with robust error handling and metadata extraction.
"""

import fitz  # PyMuPDF
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from pydantic import BaseModel, Field
from datetime import datetime

# Type hints for PyMuPDF objects
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # For static analysis, we'll use Any for PyMuPDF objects
        PyMuPDFDocument = Any
        PyMuPDFPage = Any
    else:
        PyMuPDFDocument = fitz.Document
        PyMuPDFPage = fitz.Page
except ImportError:
    # Fallback for older Python versions
    PyMuPDFDocument = Any
    PyMuPDFPage = Any


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PageMetadata(BaseModel):
    """Metadata for a single PDF page."""
    page_number: int = Field(..., description="Page number (1-based)")
    width: float = Field(..., description="Page width in points")
    height: float = Field(..., description="Page height in points")
    rotation: int = Field(..., description="Page rotation in degrees")
    text_length: int = Field(..., description="Number of characters in text")
    has_images: bool = Field(
        default=False, description="Whether page contains images")
    has_links: bool = Field(
        default=False, description="Whether page contains links")


class DocumentMetadata(BaseModel):
    """Comprehensive metadata for a PDF document."""
    file_path: str = Field(..., description="Path to the PDF file")
    file_size: int = Field(..., description="File size in bytes")
    page_count: int = Field(..., description="Total number of pages")
    title: Optional[str] = Field(None, description="Document title")
    author: Optional[str] = Field(None, description="Document author")
    subject: Optional[str] = Field(None, description="Document subject")
    creator: Optional[str] = Field(None, description="Document creator")
    producer: Optional[str] = Field(None, description="Document producer")
    creation_date: Optional[datetime] = Field(
        None, description="Document creation date")
    modification_date: Optional[datetime] = Field(
        None, description="Document modification date")
    is_encrypted: bool = Field(
        default=False, description="Whether document is encrypted")
    is_pdf_a: bool = Field(
        default=False, description="Whether document is PDF/A compliant")
    has_forms: bool = Field(
        default=False, description="Whether document has forms")
    has_bookmarks: bool = Field(
        default=False, description="Whether document has bookmarks")


class DocumentStructure(BaseModel):
    """Document structure information including sections and headers."""
    sections: List[Dict[str, Any]] = Field(
        default_factory=list, description="Document sections")
    headers: List[Dict[str, Any]] = Field(
        default_factory=list, description="Document headers")
    bookmarks: List[Dict[str, Any]] = Field(
        default_factory=list, description="Document bookmarks")
    page_labels: List[str] = Field(
        default_factory=list, description="Page labels")


class ExtractedContent(BaseModel):
    """Container for extracted PDF content with metadata."""
    text: str = Field(..., description="Extracted text content")
    metadata: DocumentMetadata = Field(..., description="Document metadata")
    structure: DocumentStructure = Field(..., description="Document structure")
    pages: List[PageMetadata] = Field(
        default_factory=list, description="Per-page metadata")
    extraction_timestamp: datetime = Field(
        default_factory=datetime.now, description="When content was extracted")


class PDFProcessingError(Exception):
    """Custom exception for PDF processing errors."""
    pass


class PDFProcessor:
    """
    Robust PDF processing utility with comprehensive error handling.

    This class provides methods for extracting text, metadata, and structure
    from PDF documents using PyMuPDF.
    """

    def __init__(self, max_file_size: int = 100 * 1024 * 1024):  # 100MB default
        """
        Initialize the PDF processor.

        Args:
            max_file_size: Maximum file size in bytes to process
        """
        self.max_file_size = max_file_size
        self.logger = logging.getLogger(__name__)

    def validate_file(self, file_path: Union[str, Path]) -> Path:
        """
        Validate that a file exists and is processable.

        Args:
            file_path: Path to the PDF file

        Returns:
            Path object for the validated file

        Raises:
            PDFProcessingError: If file is invalid
        """
        path = Path(file_path)

        if not path.exists():
            raise PDFProcessingError(f"File does not exist: {path}")

        if not path.is_file():
            raise PDFProcessingError(f"Path is not a file: {path}")

        if path.suffix.lower() != '.pdf':
            raise PDFProcessingError(f"File is not a PDF: {path}")

        file_size = path.stat().st_size
        if file_size > self.max_file_size:
            raise PDFProcessingError(
                f"File too large: {file_size} bytes (max: {self.max_file_size})"
            )

        return path

    def extract_document_metadata(self, doc: Any, file_path: Path) -> DocumentMetadata:
        """
        Extract comprehensive metadata from a PDF document.

        Args:
            doc: PyMuPDF Document object
            file_path: Path to the PDF file

        Returns:
            DocumentMetadata object with extracted information
        """
        try:
            # Get basic file information
            file_size = file_path.stat().st_size

            # Get document metadata
            metadata = doc.metadata or {}

            # Parse dates safely
            creation_date = None
            modification_date = None

            if metadata.get('creationDate'):
                try:
                    creation_date = self._parse_pdf_date(
                        metadata['creationDate'])
                except (ValueError, TypeError):
                    self.logger.warning(
                        f"Could not parse creation date: {metadata.get('creationDate')}")

            if metadata.get('modDate'):
                try:
                    modification_date = self._parse_pdf_date(
                        metadata['modDate'])
                except (ValueError, TypeError):
                    self.logger.warning(
                        f"Could not parse modification date: {metadata.get('modDate')}")

            return DocumentMetadata(
                file_path=str(file_path),
                file_size=file_size,
                page_count=doc.page_count,
                title=metadata.get('title'),
                author=metadata.get('author'),
                subject=metadata.get('subject'),
                creator=metadata.get('creator'),
                producer=metadata.get('producer'),
                creation_date=creation_date,
                modification_date=modification_date,
                is_encrypted=doc.is_encrypted,
                is_pdf_a=False,  # doc.is_pdf is not available in current API
                has_forms=getattr(doc, "is_form_pdf", False),
                has_bookmarks=len(doc.get_toc()) > 0
            )

        except Exception as e:
            self.logger.error(f"Error extracting document metadata: {e}")
            # Return basic metadata if detailed extraction fails
            return DocumentMetadata(
                file_path=str(file_path),
                file_size=file_path.stat().st_size,
                page_count=doc.page_count,
                title=None,
                author=None,
                subject=None,
                creator=None,
                producer=None,
                creation_date=None,
                modification_date=None,
                is_encrypted=doc.is_encrypted,
                is_pdf_a=False,
                has_forms=False,
                has_bookmarks=False
            )

    def extract_page_metadata(self, page: Any) -> PageMetadata:
        """
        Extract metadata for a single page.

        Args:
            page: PyMuPDF Page object

        Returns:
            PageMetadata object with page information
        """
        try:
            # Get page dimensions
            rect = page.rect

            # Check for images and links
            has_images = len(page.get_images()) > 0
            has_links = len(page.get_links()) > 0

            # Get text length
            text = page.get_text()
            text_length = len(text)

            return PageMetadata(
                page_number=(page.number or 0) + 1,  # Convert to 1-based
                width=rect.width,
                height=rect.height,
                rotation=page.rotation,
                text_length=text_length,
                has_images=has_images,
                has_links=has_links
            )

        except Exception as e:
            self.logger.error(
                f"Error extracting page metadata for page {page.number or 0}: {e}")
            # Return minimal metadata if extraction fails
            return PageMetadata(
                page_number=(page.number or 0) + 1,
                width=0,
                height=0,
                rotation=0,
                text_length=0
            )

    def extract_document_structure(self, doc: Any) -> DocumentStructure:
        """
        Extract document structure including bookmarks and headers.

        Args:
            doc: PyMuPDF Document object

        Returns:
            DocumentStructure object with structure information
        """
        try:
            # Extract table of contents (bookmarks)
            toc = doc.get_toc()
            bookmarks = []

            for entry in toc:
                level, title, page_num = entry
                bookmarks.append({
                    'level': level,
                    'title': title,
                    'page': page_num,
                    'type': 'bookmark'
                })

            # Extract headers by looking for large/bold text
            headers = []
            sections = []

            for page_num in range(doc.page_count):
                page = doc[page_num]

                # Get text with formatting information
                blocks = page.get_text("dict")

                for block in blocks.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                text = span.get("text", "").strip()
                                if text:
                                    font_size = span.get("size", 0)
                                    font_flags = span.get("flags", 0)

                                    # Heuristic for headers: large text or bold
                                    is_bold = bool(
                                        font_flags & 2**4)  # Bold flag
                                    is_large = font_size > 14

                                    if (is_bold or is_large) and len(text) > 3:
                                        headers.append({
                                            'text': text,
                                            'page': page_num + 1,
                                            'font_size': font_size,
                                            'is_bold': is_bold,
                                            'bbox': span.get("bbox", [])
                                        })

            # Create sections from headers and bookmarks
            all_sections = bookmarks + [
                {'level': 1, 'title': h['text'],
                    'page': h['page'], 'type': 'header'}
                for h in headers[:20]  # Limit to first 20 headers
            ]

            # Sort sections by page number
            all_sections.sort(key=lambda x: x['page'])

            return DocumentStructure(
                sections=all_sections,
                headers=headers,
                bookmarks=bookmarks,
                page_labels=[f"Page {i+1}" for i in range(doc.page_count)]
            )

        except Exception as e:
            self.logger.error(f"Error extracting document structure: {e}")
            return DocumentStructure()

    def extract_text_by_pages(
        self,
        doc: Any,
        start_page: int = 1,
        end_page: Optional[int] = None
    ) -> Tuple[str, List[PageMetadata]]:
        """
        Extract text from specified page range.

        Args:
            doc: PyMuPDF Document object
            start_page: Starting page number (1-based)
            end_page: Ending page number (1-based, inclusive)

        Returns:
            Tuple of (extracted_text, page_metadata_list)
        """
        if end_page is None:
            end_page = doc.page_count

        # Validate page range
        if start_page < 1 or start_page > doc.page_count:
            raise PDFProcessingError(f"Invalid start page: {start_page}")

        if end_page is None or end_page < start_page or end_page > doc.page_count:
            raise PDFProcessingError(f"Invalid end page: {end_page}")

        text_parts = []
        page_metadata = []

        for page_num in range(start_page - 1, end_page):  # Convert to 0-based
            try:
                page = doc[page_num]

                # Extract text
                page_text = page.get_text()
                text_parts.append(f"\n--- Page {page_num + 1} ---\n")
                text_parts.append(page_text)

                # Extract page metadata
                metadata = self.extract_page_metadata(page)
                page_metadata.append(metadata)

            except Exception as e:
                self.logger.error(f"Error processing page {page_num + 1}: {e}")
                # Add placeholder for failed page
                text_parts.append(f"\n--- Page {page_num + 1} (ERROR) ---\n")
                text_parts.append(f"Error extracting text: {e}")

        return '\n'.join(text_parts), page_metadata

    def extract_pdf_content(
        self,
        file_path: Union[str, Path],
        start_page: int = 1,
        end_page: Optional[int] = None
    ) -> ExtractedContent:
        """
        Extract comprehensive content from a PDF file.

        Args:
            file_path: Path to the PDF file
            start_page: Starting page number (1-based)
            end_page: Ending page number (1-based, inclusive)

        Returns:
            ExtractedContent object with all extracted information

        Raises:
            PDFProcessingError: If extraction fails
        """
        try:
            # Validate file
            validated_path = self.validate_file(file_path)

            # Open PDF document
            doc = fitz.open(str(validated_path))

            try:
                # Extract document metadata
                metadata = self.extract_document_metadata(doc, validated_path)

                # Extract document structure
                structure = self.extract_document_structure(doc)

                # Extract text and page metadata
                text, page_metadata = self.extract_text_by_pages(
                    doc, start_page, end_page)

                return ExtractedContent(
                    text=text,
                    metadata=metadata,
                    structure=structure,
                    pages=page_metadata
                )

            finally:
                doc.close()

        except fitz.FileDataError as e:
            raise PDFProcessingError(f"Invalid PDF file: {e}")
        except fitz.FileNotFoundError as e:
            raise PDFProcessingError(f"File not found: {e}")
        except Exception as e:
            raise PDFProcessingError(f"Unexpected error processing PDF: {e}")

    def extract_images_metadata(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Extract metadata about images in the PDF.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of image metadata dictionaries
        """
        try:
            validated_path = self.validate_file(file_path)
            doc = fitz.open(str(validated_path))

            images_metadata = []

            try:
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    images = page.get_images()

                    for img_index, img in enumerate(images):
                        # img is a tuple: (xref, smask, width, height, bpc, colorspace, alt, name, filter)
                        xref, smask, width, height, bpc, colorspace, alt, name, filter_type = img

                        images_metadata.append({
                            'page': page_num + 1,
                            'index': img_index,
                            'xref': xref,
                            'width': width,
                            'height': height,
                            'bits_per_component': bpc,
                            'colorspace': colorspace,
                            'name': name,
                            'filter': filter_type
                        })

                return images_metadata

            finally:
                doc.close()

        except Exception as e:
            self.logger.error(f"Error extracting image metadata: {e}")
            return []

    def _parse_pdf_date(self, date_string: str) -> Optional[datetime]:
        """
        Parse PDF date string into datetime object.

        PDF dates have the format: D:YYYYMMDDHHmmSSOHH'mm'
        where O is the timezone offset sign (+ or -)

        Args:
            date_string: PDF date string

        Returns:
            Parsed datetime object or None if parsing fails
        """
        if not date_string:
            return None

        # Remove 'D:' prefix if present
        if date_string.startswith('D:'):
            date_string = date_string[2:]

        # Handle different PDF date formats
        try:
            # Try to parse the most common format: YYYYMMDDHHmmSSOHH'mm'
            if len(date_string) >= 14:
                # Extract date/time components
                year = int(date_string[0:4])
                month = int(date_string[4:6])
                day = int(date_string[6:8])
                hour = int(date_string[8:10])
                minute = int(date_string[10:12])
                second = int(date_string[12:14])

                # Handle timezone offset
                if len(date_string) > 14:
                    tz_part = date_string[14:]
                    # Parse timezone like +00'00' or -05'00'
                    if len(tz_part) >= 6 and tz_part[0] in '+-':
                        sign = 1 if tz_part[0] == '+' else -1
                        tz_hours = int(tz_part[1:3])
                        tz_minutes = int(tz_part[4:6])

                        # Create timezone-aware datetime
                        from datetime import timezone, timedelta
                        tz_offset = timezone(
                            timedelta(hours=sign * tz_hours, minutes=sign * tz_minutes))
                        return datetime(year, month, day, hour, minute, second, tzinfo=tz_offset)

                # Return naive datetime if no timezone info
                return datetime(year, month, day, hour, minute, second)

            # If the format is different, try other approaches
            # Handle simple formats like YYYYMMDD
            elif len(date_string) == 8:
                year = int(date_string[0:4])
                month = int(date_string[4:6])
                day = int(date_string[6:8])
                return datetime(year, month, day)

        except (ValueError, IndexError) as e:
            self.logger.debug(f"Could not parse PDF date '{date_string}': {e}")

        # Fallback: try to clean up the string for ISO format parsing
        try:
            # Remove common PDF date artifacts and try ISO parsing
            cleaned = date_string.replace("'", "").replace("Z", "+00:00")
            # Try to convert to ISO format
            if len(cleaned) >= 14:
                iso_date = f"{cleaned[0:4]}-{cleaned[4:6]}-{cleaned[6:8]}T{cleaned[8:10]}:{cleaned[10:12]}:{cleaned[12:14]}"
                if len(cleaned) > 14:
                    # Add timezone
                    tz_part = cleaned[14:]
                    if len(tz_part) >= 5 and tz_part[0] in '+-':
                        iso_date += f"{tz_part[0:3]}:{tz_part[3:5]}"
                return datetime.fromisoformat(iso_date)

        except (ValueError, IndexError):
            pass

        return None


# Utility functions for common operations
def extract_text_from_pdf(file_path: Union[str, Path], start_page: int = 1, end_page: Optional[int] = None) -> str:
    """
    Convenience function to extract text from a PDF file.

    Args:
        file_path: Path to the PDF file
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based, inclusive)

    Returns:
        Extracted text content
    """
    processor = PDFProcessor()
    content = processor.extract_pdf_content(file_path, start_page, end_page)
    return content.text


def get_pdf_metadata(file_path: Union[str, Path]) -> DocumentMetadata:
    """
    Convenience function to get PDF metadata.

    Args:
        file_path: Path to the PDF file

    Returns:
        DocumentMetadata object
    """
    processor = PDFProcessor()
    content = processor.extract_pdf_content(
        file_path, 1, 1)  # Just first page for metadata
    return content.metadata


def get_pdf_page_count(file_path: Union[str, Path]) -> int:
    """
    Convenience function to get the number of pages in a PDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        Number of pages
    """
    try:
        processor = PDFProcessor()
        validated_path = processor.validate_file(file_path)
        doc = fitz.open(str(validated_path))
        try:
            return doc.page_count
        finally:
            doc.close()
    except Exception as e:
        logger.error(f"Error getting page count: {e}")
        return 0
