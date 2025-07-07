#!/usr/bin/env python3
"""
Test script to verify PDF date parsing is working correctly.
"""

from mcp_server.utils.pdf_processor import PDFProcessor
import sys
from pathlib import Path

# Add the mcp_server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "mcp_server"))


def test_date_parsing():
    """Test the PDF date parsing functionality."""
    processor = PDFProcessor()

    # Test date strings that were causing issues
    test_dates = [
        "D:20250309111411+00'00'",
        "D:20250309111411-05'00'",
        "D:20250309111411Z",
        "D:20250309111411",
        "D:20250309",
        "20250309111411+00'00'",
        "20250309111411",
        "20250309",
    ]

    print("Testing PDF date parsing:")
    print("-" * 50)

    for date_str in test_dates:
        try:
            result = processor._parse_pdf_date(date_str)
            if result:
                print(f"✓ '{date_str}' -> {result}")
            else:
                print(f"✗ '{date_str}' -> None")
        except Exception as e:
            print(f"✗ '{date_str}' -> Error: {e}")

    print("-" * 50)
    print("Date parsing test completed")


if __name__ == "__main__":
    test_date_parsing()
