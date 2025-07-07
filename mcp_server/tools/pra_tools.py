"""
PRA (PYRAMID Reference Architecture) Tools for PYRAMID MCP Server

This module provides access to PYRAMID Reference Architecture component information, 
interaction views, and deployment patterns.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

pdf_processor: Optional[Any] = None
document_parser: Optional[Any] = None
data_dir: Optional[Path] = None


def initialize_pra_tools(data_directory: Path, pdf_proc, doc_parser):
    """Initialize the PRA tools with processors and data directory."""
    global pdf_processor, document_parser, data_dir
    pdf_processor = pdf_proc
    document_parser = doc_parser
    data_dir = data_directory


def search_pra_components(
    component_type: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find PRA components by type and category.

    MOCK VERSION: Returns sample PRA components for testing.

    Args:
        component_type: Type of component (e.g., "Core", "Optional", "Interface")
        category: Category filter (e.g., "Data", "Communication", "Security")

    Returns:
        Dict containing matching PRA components
    """
    try:
        # Mock PRA components data
        mock_components = [
            {
                "name": "Data Management Service",
                "type": "Core",
                "category": "Data",
                "description": "Core service responsible for managing data ingestion, storage, and retrieval across the PYRAMID architecture.",
                "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                "confidence": "high"
            },
            {
                "name": "Security Authentication Module",
                "type": "Core",
                "category": "Security",
                "description": "Essential security component that handles user authentication and authorization for all PYRAMID services.",
                "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                "confidence": "high"
            },
            {
                "name": "Communication Protocol Handler",
                "type": "Interface",
                "category": "Communication",
                "description": "Interface component that manages communication protocols between different PYRAMID components.",
                "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
                "confidence": "medium"
            },
            {
                "name": "User Interface Gateway",
                "type": "Interface",
                "category": "User Interface",
                "description": "Gateway component that provides standardized user interface access to PYRAMID services.",
                "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                "confidence": "medium"
            },
            {
                "name": "System Monitor",
                "type": "Optional",
                "category": "Management",
                "description": "Optional monitoring component that tracks system performance and health metrics.",
                "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
                "confidence": "medium"
            },
            {
                "name": "Data Exchange Broker",
                "type": "Core",
                "category": "Data",
                "description": "Core component that facilitates secure data exchange between different systems and organizations.",
                "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                "confidence": "high"
            },
            {
                "name": "Network Security Filter",
                "type": "Optional",
                "category": "Security",
                "description": "Optional security component that provides additional network-level filtering and protection.",
                "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
                "confidence": "medium"
            },
            {
                "name": "Integration Bus",
                "type": "Core",
                "category": "Communication",
                "description": "Core integration component that enables seamless communication between various PYRAMID services.",
                "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                "confidence": "high"
            },
            {
                "name": "Configuration Manager",
                "type": "Optional",
                "category": "Management",
                "description": "Management component that handles configuration settings and deployment parameters.",
                "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
                "confidence": "medium"
            },
            {
                "name": "Audit Trail Processor",
                "type": "Optional",
                "category": "Security",
                "description": "Security component that maintains comprehensive audit trails for compliance and monitoring.",
                "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                "confidence": "medium"
            }
        ]

        # Filter by component type if specified
        filtered_components = mock_components
        if component_type:
            filtered_components = [
                comp for comp in filtered_components
                if component_type.lower() in comp["type"].lower()
            ]

        # Filter by category if specified
        if category:
            filtered_components = [
                comp for comp in filtered_components
                if category.lower() in comp["category"].lower()
            ]

        # Sort by type and category
        filtered_components.sort(key=lambda x: (
            x["type"], x["category"], x["name"]))

        return {
            "success": True,
            "component_type": component_type,
            "category": category,
            "total_components": len(filtered_components),
            "components": filtered_components
        }

    except Exception as e:
        logger.error(f"Error in mock PRA components search: {e}")
        return {
            "error": f"Mock search error: {str(e)}",
            "component_type": component_type,
            "category": category,
            "components": []
        }


def get_component_details(component_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific PRA component.

    MOCK VERSION: Returns sample component details for testing.
    In a real scenario, this would query a database populated from PYRAMID documents.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing detailed component information
    """
    try:
        # Mock component details data
        mock_details = {
            "Data Management Service": {
                "section": {
                    "title": "Data Management Service",
                    "content": "The Data Management Service is responsible for managing data ingestion, storage, and retrieval across the PYRAMID architecture. It ensures data consistency, integrity, and availability for all core services.",
                    "page_range": "12-15",
                    "source_document": "PYRAMID_Technical_Standard_V1.pdf"
                },
                "information": {
                    "purpose": [
                        {
                            "type": "purpose",
                            "content": "The primary purpose of the Data Management Service is to provide a unified interface for data operations, supporting both structured and unstructured data.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "high"
                        }
                    ],
                    "interfaces": [
                        {
                            "type": "interfaces",
                            "content": "Exposes RESTful APIs and supports integration with the Integration Bus for data exchange.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ],
                    "requirements": [
                        {
                            "type": "requirements",
                            "content": "Must support high availability and data encryption at rest and in transit.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ],
                    "dependencies": [
                        {
                            "type": "dependencies",
                            "content": "Depends on the Security Authentication Module for access control.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ],
                    "specifications": [
                        {
                            "type": "specifications",
                            "content": "Compliant with ISO/IEC 11179 for metadata management.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ]
                }
            },
            "Security Authentication Module": {
                "section": {
                    "title": "Security Authentication Module",
                    "content": "Handles user authentication and authorization for all PYRAMID services, ensuring secure access and compliance with security policies.",
                    "page_range": "16-18",
                    "source_document": "PYRAMID_Technical_Standard_V1.pdf"
                },
                "information": {
                    "purpose": [
                        {
                            "type": "purpose",
                            "content": "Provides centralized authentication and authorization services.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "high"
                        }
                    ],
                    "interfaces": [
                        {
                            "type": "interfaces",
                            "content": "Supports OAuth2 and SAML protocols for secure integration.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ],
                    "requirements": [
                        {
                            "type": "requirements",
                            "content": "Shall log all authentication attempts and support multi-factor authentication.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ],
                    "dependencies": [
                        {
                            "type": "dependencies",
                            "content": "Requires access to the User Directory Service.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ],
                    "specifications": [
                        {
                            "type": "specifications",
                            "content": "Follows NIST SP 800-63B guidelines.",
                            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                            "relevance": "medium"
                        }
                    ]
                }
            }
            # Add more mock components as needed
        }

        details = mock_details.get(component_id)
        if not details:
            return {
                "success": False,
                "component_id": component_id,
                "found": False,
                "total_references": 0,
                "details": {},
                "note": "This is a mock response. In a real scenario, this would query a database populated from PYRAMID documents."
            }

        total_references = sum(len(v)
                               for v in details.get("information", {}).values())
        return {
            "success": True,
            "component_id": component_id,
            "found": True,
            "total_references": total_references,
            "details": details,
            "note": "This is a mock response. In a real scenario, this would query a database populated from PYRAMID documents."
        }

    except Exception as e:
        logger.error(f"Error getting component details: {e}")
        return {
            "error": f"Failed to get component details: {str(e)}",
            "component_id": component_id,
            "details": {}
        }


def search_component_relationships(component_id: str) -> Dict[str, Any]:
    """
    Find relationships between components.

    MOCK VERSION: Returns sample relationships for testing.
    In a real scenario, this would query a database or knowledge graph populated from PYRAMID documents.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing component relationships
    """
    try:
        # Mock relationships data
        mock_relationships = {
            "Data Management Service": [
                {
                    "related_component": "Security Authentication Module",
                    "relationship_type": "Dependency",
                    "context": "The Data Management Service depends on the Security Authentication Module for access control and secure data operations.",
                    "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                    "confidence": "high"
                },
                {
                    "related_component": "Integration Bus",
                    "relationship_type": "Interface",
                    "context": "The Data Management Service interfaces with the Integration Bus to enable seamless data exchange across services.",
                    "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                    "confidence": "medium"
                }
            ],
            "Security Authentication Module": [
                {
                    "related_component": "User Directory Service",
                    "relationship_type": "Dependency",
                    "context": "The Security Authentication Module requires access to the User Directory Service for user validation.",
                    "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                    "confidence": "medium"
                },
                {
                    "related_component": "Data Management Service",
                    "relationship_type": "Provider",
                    "context": "The Security Authentication Module provides authentication services to the Data Management Service.",
                    "source_document": "PYRAMID_Technical_Standard_V1.pdf",
                    "confidence": "medium"
                }
            ]
            # Add more mock relationships as needed
        }

        relationships = mock_relationships.get(component_id, [])

        return {
            "success": True,
            "component_id": component_id,
            "total_relationships": len(relationships),
            "relationships": relationships,
            "note": "This is a mock response. In a real scenario, this would query a database or knowledge graph populated from PYRAMID documents."
        }

    except Exception as e:
        logger.error(f"Error searching component relationships: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "component_id": component_id,
            "relationships": []
        }


# Export functions
__all__ = [
    'initialize_pra_tools',
    'search_pra_components',
    'get_component_details',
    'search_component_relationships',
]
