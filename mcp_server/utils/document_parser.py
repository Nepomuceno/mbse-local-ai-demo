"""
Document Parser for PYRAMID MCP Server

This module provides document structure analysis capabilities,
including section detection, header hierarchy, and content organization.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum
import fitz
import logging

from mcp_server.utils.pdf_processor import PDFProcessor, ExtractedContent, PDFProcessingError

# Configure logging
logger = logging.getLogger(__name__)


class SectionType(str, Enum):
    """Types of document sections."""
    TITLE = "title"
    CHAPTER = "chapter"
    SECTION = "section"
    SUBSECTION = "subsection"
    SUBSUBSECTION = "subsubsection"
    APPENDIX = "appendix"
    REFERENCE = "reference"
    GLOSSARY = "glossary"
    INDEX = "index"
    UNKNOWN = "unknown"


class HeaderLevel(int, Enum):
    """Document header levels."""
    TITLE = 0
    CHAPTER = 1
    SECTION = 2
    SUBSECTION = 3
    SUBSUBSECTION = 4
    PARAGRAPH = 5


class DocumentSection(BaseModel):
    """Represents a document section with metadata."""
    title: str = Field(..., description="Section title")
    section_type: SectionType = Field(..., description="Type of section")
    level: int = Field(..., description="Hierarchical level (0-5)")
    page_start: int = Field(..., description="Starting page number")
    page_end: Optional[int] = Field(None, description="Ending page number")
    text_content: str = Field(default="", description="Section text content")
    subsections: List['DocumentSection'] = Field(
        default_factory=list, description="Child sections")
    section_number: Optional[str] = Field(
        None, description="Section number (e.g., '1.2.3')")
    parent_section: Optional[str] = Field(
        None, description="Parent section title")

    class Config:
        # Allow forward references for recursive model
        arbitrary_types_allowed = True


class DocumentOutline(BaseModel):
    """Complete document outline with hierarchical structure."""
    sections: List[DocumentSection] = Field(
        default_factory=list, description="Top-level sections")
    total_sections: int = Field(
        default=0, description="Total number of sections")
    max_depth: int = Field(default=0, description="Maximum nesting depth")
    section_numbering_scheme: str = Field(
        default="numeric", description="Numbering scheme used")

    def get_section_by_title(self, title: str) -> Optional[DocumentSection]:
        """Find a section by its title."""
        def search_sections(sections: List[DocumentSection], target: str) -> Optional[DocumentSection]:
            for section in sections:
                if section.title.lower() == target.lower():
                    return section
                # Search in subsections
                found = search_sections(section.subsections, target)
                if found:
                    return found
            return None

        return search_sections(self.sections, title)

    def get_sections_by_page(self, page_num: int) -> List[DocumentSection]:
        """Get all sections that contain a specific page."""
        def search_by_page(sections: List[DocumentSection], page: int) -> List[DocumentSection]:
            matching = []
            for section in sections:
                if section.page_start <= page <= (section.page_end or float('inf')):
                    matching.append(section)
                    # Also search subsections
                    matching.extend(search_by_page(section.subsections, page))
            return matching

        return search_by_page(self.sections, page_num)


class DocumentParser:
    """
    Advanced document parser for extracting hierarchical structure.

    This class analyzes PDF documents to identify sections, headers,
    and create a structured representation of the document.
    """

    def __init__(self):
        """Initialize the document parser."""
        self.logger = logging.getLogger(__name__)
        self.pdf_processor = PDFProcessor()

        # Common section patterns for technical documents
        self.section_patterns = [
            # Numbered sections: "1.", "1.1", "1.1.1", etc.
            r'^(\d+(?:\.\d+)*)\.\s*(.+)$',
            # Lettered sections: "A.", "A.1", etc.
            r'^([A-Z](?:\.\d+)*)\.\s*(.+)$',
            # Roman numerals: "I.", "II.", etc.
            r'^([IVX]+)\.\s*(.+)$',
            # Bullet points or dashes
            r'^[•\-\*]\s*(.+)$',
            # Appendix patterns
            r'^(Appendix\s+[A-Z])\s*[\-\:]\s*(.+)$',
            # Chapter patterns
            r'^(Chapter\s+\d+)\s*[\-\:]\s*(.+)$',
        ]

        # Keywords that indicate section types
        self.section_keywords = {
            SectionType.TITLE: ['title', 'executive summary', 'abstract'],
            SectionType.CHAPTER: ['chapter'],
            SectionType.APPENDIX: ['appendix', 'annex'],
            SectionType.REFERENCE: ['references', 'bibliography', 'citations'],
            SectionType.GLOSSARY: ['glossary', 'definitions', 'terminology'],
            SectionType.INDEX: ['index', 'contents'],
        }

    def _classify_section_type(self, title: str) -> SectionType:
        """
        Classify a section based on its title.

        Args:
            title: Section title

        Returns:
            SectionType enum value
        """
        title_lower = title.lower().strip()

        for section_type, keywords in self.section_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return section_type

        # Default classification based on position and content
        if title_lower.startswith('chapter'):
            return SectionType.CHAPTER
        elif title_lower.startswith('appendix'):
            return SectionType.APPENDIX
        elif any(word in title_lower for word in ['reference', 'bibliography']):
            return SectionType.REFERENCE
        elif any(word in title_lower for word in ['glossary', 'definition']):
            return SectionType.GLOSSARY
        elif 'index' in title_lower:
            return SectionType.INDEX
        else:
            return SectionType.SECTION

    def _extract_section_number(self, title: str) -> Tuple[Optional[str], str, int]:
        """
        Extract section number and level from title.

        Args:
            title: Section title

        Returns:
            Tuple of (section_number, clean_title, level)
        """
        for pattern in self.section_patterns:
            match = re.match(pattern, title.strip())
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    section_num, clean_title = groups
                    # Determine level based on dots in section number
                    if '.' in section_num:
                        level = len(section_num.split('.'))
                    else:
                        level = 1
                    return section_num, clean_title.strip(), level
                elif len(groups) == 1:
                    # Single group (e.g., bullet point)
                    clean_title = groups[0]
                    return None, clean_title.strip(), 1
                else:
                    # No groups, use the entire match
                    return None, title.strip(), 1

        # No pattern matched
        return None, title.strip(), 1

    def _detect_headers_from_formatting(self, content: ExtractedContent) -> List[Dict[str, Any]]:
        """
        Detect headers based on text formatting (font size, boldness).

        Args:
            content: Extracted PDF content

        Returns:
            List of header dictionaries
        """
        headers = []

        try:
            # Re-open document to get formatting info
            doc = fitz.open(content.metadata.file_path)

            try:
                for page_num in range(doc.page_count):
                    page = doc[page_num]

                    # Get text with formatting information
                    blocks = page.get_text("dict")  # type: ignore

                    for block in blocks.get("blocks", []):
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line.get("spans", []):
                                    text = span.get("text", "").strip()
                                    if text and len(text) > 3:
                                        font_size = span.get("size", 0)
                                        font_flags = span.get("flags", 0)
                                        font_name = span.get("font", "")

                                        # Check for header characteristics
                                        is_bold = bool(
                                            font_flags & 2**4)  # Bold flag
                                        is_italic = bool(
                                            font_flags & 2**1)  # Italic flag
                                        is_large = font_size > 12

                                        # Heuristic for headers
                                        if (is_bold and is_large) or font_size > 16:
                                            headers.append({
                                                'text': text,
                                                'page': page_num + 1,
                                                'font_size': font_size,
                                                'font_name': font_name,
                                                'is_bold': is_bold,
                                                'is_italic': is_italic,
                                                'bbox': span.get("bbox", []),
                                                'confidence': self._calculate_header_confidence(
                                                    text, font_size, is_bold, is_italic
                                                )
                                            })

                return headers

            finally:
                doc.close()

        except Exception as e:
            self.logger.error(f"Error detecting headers from formatting: {e}")
            return []

    def _calculate_header_confidence(self, text: str, font_size: float, is_bold: bool, is_italic: bool) -> float:
        """
        Calculate confidence score for header detection.

        Args:
            text: Header text
            font_size: Font size
            is_bold: Whether text is bold
            is_italic: Whether text is italic

        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 0.0

        # Font size factor
        if font_size > 16:
            score += 0.4
        elif font_size > 14:
            score += 0.3
        elif font_size > 12:
            score += 0.2

        # Bold text factor
        if is_bold:
            score += 0.3

        # Text characteristics
        if re.match(r'^\d+(?:\.\d+)*\.\s*', text):  # Numbered section
            score += 0.2

        if any(keyword in text.lower() for keyword in ['chapter', 'section', 'appendix']):
            score += 0.1

        # Short, title-like text
        if len(text.split()) <= 8 and len(text) > 5:
            score += 0.1

        # Capitalization patterns
        if text.isupper():
            score += 0.1
        elif text.istitle():
            score += 0.05

        return min(score, 1.0)

    def _build_section_hierarchy(self, headers: List[Dict[str, Any]]) -> List[DocumentSection]:
        """
        Build hierarchical section structure from headers.

        Args:
            headers: List of header dictionaries

        Returns:
            List of top-level DocumentSection objects
        """
        sections = []
        section_stack = []  # Stack to track current hierarchy

        for header in headers:
            try:
                text = header.get('text', '')
                page = header.get('page', 1)
                confidence = header.get('confidence', 0.5)

                # Skip headers with low confidence or empty text
                if confidence < 0.3 or not text.strip():
                    continue

                # Extract section information
                section_num, clean_title, level = self._extract_section_number(
                    text)
                section_type = self._classify_section_type(clean_title)

                # Create section object
                section = DocumentSection(
                    title=clean_title,
                    section_type=section_type,
                    level=level,
                    page_start=page,
                    page_end=None,
                    section_number=section_num,
                    parent_section=None
                )

                # Determine where to place this section in hierarchy
                self._place_section_in_hierarchy(
                    section, sections, section_stack)

            except Exception as e:
                self.logger.error(f"Error processing header '{header}': {e}")
                continue

        return sections

    def _place_section_in_hierarchy(
        self,
        section: DocumentSection,
        sections: List[DocumentSection],
        section_stack: List[DocumentSection]
    ):
        """
        Place a section in the correct position in the hierarchy.

        Args:
            section: Section to place
            sections: Top-level sections list
            section_stack: Current hierarchy stack
        """
        # Pop sections from stack that are at same or higher level
        while section_stack and section_stack[-1].level >= section.level:
            section_stack.pop()

        # Add section to appropriate parent
        if section_stack:
            parent = section_stack[-1]
            parent.subsections.append(section)
            section.parent_section = parent.title
        else:
            sections.append(section)

        # Add current section to stack
        section_stack.append(section)

    def _extract_section_content(self, section: DocumentSection, content: ExtractedContent) -> str:
        """
        Extract text content for a specific section.

        Args:
            section: Section to extract content for
            content: Full document content

        Returns:
            Section text content
        """
        # This is a simplified implementation
        # In a real implementation, you'd want to extract text between
        # the section start and the next section at the same or higher level

        try:
            # Extract text from the section's page range
            if section.page_end:
                pages_text = []
                for page_meta in content.pages:
                    if section.page_start <= page_meta.page_number <= section.page_end:
                        # This is a simplified approach - in reality you'd want
                        # to extract just the relevant portion of each page
                        pages_text.append(
                            f"[Content from page {page_meta.page_number}]")
                return "\n".join(pages_text)
            else:
                return f"[Content starting from page {section.page_start}]"

        except Exception as e:
            self.logger.error(f"Error extracting section content: {e}")
            return ""

    def parse_document_structure(self, file_path: Union[str, Path]) -> DocumentOutline:
        """
        Parse complete document structure from PDF.

        Args:
            file_path: Path to PDF file

        Returns:
            DocumentOutline with hierarchical structure

        Raises:
            PDFProcessingError: If parsing fails
        """
        try:
            # Extract full document content
            content = self.pdf_processor.extract_pdf_content(file_path)

            # Detect headers using multiple methods
            formatting_headers = self._detect_headers_from_formatting(content)
            bookmark_headers = self._extract_bookmark_headers(content)

            # Combine and deduplicate headers
            all_headers = self._combine_headers(
                formatting_headers, bookmark_headers)

            # Build section hierarchy
            sections = self._build_section_hierarchy(all_headers)

            # Update section end pages
            self._update_section_end_pages(sections)

            # Extract content for each section
            for section in sections:
                section.text_content = self._extract_section_content(
                    section, content)
                self._extract_subsection_content(section, content)

            # Calculate outline statistics
            total_sections = self._count_total_sections(sections)
            max_depth = self._calculate_max_depth(sections)

            return DocumentOutline(
                sections=sections,
                total_sections=total_sections,
                max_depth=max_depth,
                section_numbering_scheme=self._detect_numbering_scheme(
                    all_headers)
            )

        except Exception as e:
            raise PDFProcessingError(
                f"Failed to parse document structure: {e}")

    def _extract_bookmark_headers(self, content: ExtractedContent) -> List[Dict[str, Any]]:
        """Extract headers from PDF bookmarks."""
        headers = []

        try:
            for bookmark in content.structure.bookmarks:
                if bookmark and 'title' in bookmark and 'page' in bookmark:
                    headers.append({
                        'text': bookmark['title'],
                        'page': bookmark['page'],
                        'font_size': 14,  # Default
                        'font_name': 'Unknown',
                        'is_bold': True,
                        'is_italic': False,
                        'bbox': [],
                        'confidence': 0.8,  # High confidence for bookmarks
                        'source': 'bookmark'
                    })
        except Exception as e:
            self.logger.error(f"Error extracting bookmark headers: {e}")

        return headers

    def _combine_headers(self, formatting_headers: List[Dict[str, Any]], bookmark_headers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Combine headers from different sources and remove duplicates."""
        try:
            all_headers = formatting_headers + bookmark_headers

            # Filter out any None or invalid headers
            all_headers = [
                h for h in all_headers if h and 'text' in h and 'page' in h]

            if not all_headers:
                return []

            # Sort by page number and position
            all_headers.sort(key=lambda x: (
                x.get('page', 1), x.get('bbox', [0, 0, 0, 0])[1] if x.get('bbox') else 0))

            # Remove near-duplicates (same page, similar text)
            unique_headers = []
            for header in all_headers:
                is_duplicate = False
                for existing in unique_headers:
                    if (existing.get('page') == header.get('page') and
                            self._text_similarity(existing.get('text', ''), header.get('text', '')) > 0.8):
                        is_duplicate = True
                        # Keep the one with higher confidence
                        if header.get('confidence', 0) > existing.get('confidence', 0):
                            unique_headers.remove(existing)
                            unique_headers.append(header)
                        break

                if not is_duplicate:
                    unique_headers.append(header)

            return unique_headers
        except Exception as e:
            self.logger.error(f"Error combining headers: {e}")
            return []

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings."""
        # Simple similarity based on common words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _update_section_end_pages(self, sections: List[DocumentSection]):
        """Update end pages for all sections."""
        try:
            for i, section in enumerate(sections):
                if i < len(sections) - 1:
                    section.page_end = sections[i + 1].page_start - 1

                # Update subsections recursively
                self._update_section_end_pages(section.subsections)
        except Exception as e:
            self.logger.error(f"Error updating section end pages: {e}")

    def _extract_subsection_content(self, section: DocumentSection, content: ExtractedContent):
        """Extract content for subsections recursively."""
        try:
            for subsection in section.subsections:
                subsection.text_content = self._extract_section_content(
                    subsection, content)
                self._extract_subsection_content(subsection, content)
        except Exception as e:
            self.logger.error(f"Error extracting subsection content: {e}")

    def _count_total_sections(self, sections: List[DocumentSection]) -> int:
        """Count total number of sections including subsections."""
        total = len(sections)
        for section in sections:
            total += self._count_total_sections(section.subsections)
        return total

    def _calculate_max_depth(self, sections: List[DocumentSection]) -> int:
        """Calculate maximum nesting depth."""
        if not sections:
            return 0

        max_depth = 1
        for section in sections:
            if section.subsections:
                depth = 1 + self._calculate_max_depth(section.subsections)
                max_depth = max(max_depth, depth)

        return max_depth

    def _detect_numbering_scheme(self, headers: List[Dict[str, Any]]) -> str:
        """Detect the numbering scheme used in the document."""
        schemes = {
            'numeric': 0,
            'alphabetic': 0,
            'roman': 0,
            'mixed': 0
        }

        for header in headers:
            text = header['text']
            if re.match(r'^\d+(?:\.\d+)*\.', text):
                schemes['numeric'] += 1
            elif re.match(r'^[A-Z](?:\.\d+)*\.', text):
                schemes['alphabetic'] += 1
            elif re.match(r'^[IVX]+\.', text):
                schemes['roman'] += 1
            else:
                schemes['mixed'] += 1

        return max(schemes.keys(), key=lambda k: schemes[k])


# Utility functions
def parse_pdf_structure(file_path: Union[str, Path]) -> DocumentOutline:
    """
    Convenience function to parse PDF document structure.

    Args:
        file_path: Path to PDF file

    Returns:
        DocumentOutline with hierarchical structure
    """
    parser = DocumentParser()
    return parser.parse_document_structure(file_path)


def get_document_sections(file_path: Union[str, Path]) -> List[DocumentSection]:
    """
    Convenience function to get document sections.

    Args:
        file_path: Path to PDF file

    Returns:
        List of DocumentSection objects
    """
    outline = parse_pdf_structure(file_path)
    return outline.sections


def find_section_by_title(file_path: Union[str, Path], title: str) -> Optional[DocumentSection]:
    """
    Find a section by title in the document.

    Args:
        file_path: Path to PDF file
        title: Section title to search for

    Returns:
        DocumentSection if found, None otherwise
    """
    outline = parse_pdf_structure(file_path)
    return outline.get_section_by_title(title)
