#!/usr/bin/env python3
"""
Test script to verify PDF metadata extraction works with real PDF files.
"""

from mcp_server.utils.pdf_processor import PDFProcessor
import sys
from pathlib import Path

# Add the mcp_server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "mcp_server"))


def test_pdf_metadata():
    """Test PDF metadata extraction with real files."""
    processor = PDFProcessor()

    # Test with actual PDF files in the data directory
    data_dir = Path(__file__).parent / "mcp_server" / "data"
    pdf_files = list(data_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data directory")
        return

    print(f"Testing PDF metadata extraction with {len(pdf_files)} files:")
    print("-" * 60)

    for pdf_file in pdf_files[:2]:  # Test first 2 files
        try:
            print(f"\nProcessing: {pdf_file.name}")
            content = processor.extract_pdf_content(
                pdf_file, 1, 1)  # Just first page for testing

            print(f"  Title: {content.metadata.title}")
            print(f"  Author: {content.metadata.author}")
            print(f"  Creation Date: {content.metadata.creation_date}")
            print(f"  Modification Date: {content.metadata.modification_date}")
            print(f"  Pages: {content.metadata.page_count}")
            print(f"  File Size: {content.metadata.file_size} bytes")

        except Exception as e:
            print(f"  Error processing {pdf_file.name}: {e}")

    print("-" * 60)
    print("PDF metadata test completed")


if __name__ == "__main__":
    test_pdf_metadata()
