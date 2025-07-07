"""
PRA (PYRAMID Reference Architecture) Tools for PYRAMID MCP Server

This module provides access to PYRAMID Reference Architecture component information, 
interaction views, and deployment patterns using a centralized mock knowledge graph.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging
from mcp_server.data.mock_pyramid_knowledge_graph import (
    query_knowledge_graph,
    get_all_component_owners,
    get_component_by_owner,
    get_components_by_sector
)

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
    Find PRA components by type and category using the centralized knowledge graph.

    Args:
        component_type: Type of component (e.g., "Core", "Optional", "Interface")
        category: Category filter (e.g., "Data", "Communication", "Security")

    Returns:
        Dict containing matching PRA components
    """
    try:
        # Query the centralized knowledge graph
        result = query_knowledge_graph(
            "search",
            component_type=component_type,
            category=category
        )

        if result["success"]:
            components = result["components"]
            # Sort by type and category
            components.sort(key=lambda x: (
                x["type"], x["category"], x["name"]))

            return {
                "success": True,
                "component_type": component_type,
                "category": category,
                "total_components": len(components),
                "components": components,
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "component_type": component_type,
                "category": category,
                "components": []
            }

    except Exception as e:
        logger.error(f"Error searching PRA components: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "component_type": component_type,
            "category": category,
            "components": []
        }


def get_component_details(component_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific PRA component using the centralized knowledge graph.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing detailed component information
    """
    try:
        # Query the centralized knowledge graph for component details
        result = query_knowledge_graph("component", component_id=component_id)

        if result["success"]:
            component_data = result["component"]

            # Structure the response to match the expected format
            return {
                "success": True,
                "component_id": component_id,
                "found": True,
                "total_references": len(component_data.get("responsibilities", [])),
                "details": {
                    "section": {
                        "title": component_id,
                        "content": component_data.get("description", ""),
                        "source_document": component_data.get("source_document", ""),
                        "confidence": component_data.get("confidence", "medium")
                    },
                    "information": {
                        "responsibilities": component_data.get("responsibilities", []),
                        "interfaces": component_data.get("interfaces", []),
                        "dependencies": component_data.get("dependencies", []),
                        "provides_to": component_data.get("provides_to", []),
                        "specifications": component_data.get("specifications", []),
                        "type": component_data.get("type", "Unknown"),
                        "category": component_data.get("category", "Unknown")
                    }
                },
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }
        else:
            return {
                "success": False,
                "component_id": component_id,
                "found": False,
                "total_references": 0,
                "details": {},
                "error": result.get("error", "Component not found"),
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
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
    Find relationships between components using the centralized knowledge graph.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing component relationships
    """
    try:
        # Query the centralized knowledge graph for relationships
        result = query_knowledge_graph(
            "relationship", component_id=component_id)

        if result["success"]:
            relationships = result["relationships"]

            return {
                "success": True,
                "component_id": component_id,
                "total_relationships": len(relationships),
                "relationships": relationships,
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }
        else:
            return {
                "success": False,
                "component_id": component_id,
                "total_relationships": 0,
                "relationships": [],
                "error": result.get("error", "Component not found"),
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }

    except Exception as e:
        logger.error(f"Error searching component relationships: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "component_id": component_id,
            "relationships": []
        }


def get_component_owners(component_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get component ownership and responsibility information.

    Args:
        component_id: Specific component to get ownership for, or None for all components

    Returns:
        Dict containing component ownership information
    """
    try:
        if component_id:
            # Get ownership for a specific component
            result = query_knowledge_graph(
                "ownership", component_id=component_id)

            if result["success"]:
                return {
                    "success": True,
                    "component_id": component_id,
                    "ownership": result["ownership"],
                    "note": "Data retrieved from centralized PYRAMID knowledge graph"
                }
            else:
                return {
                    "success": False,
                    "component_id": component_id,
                    "error": result.get("error", "Ownership information not found"),
                    "note": "Data retrieved from centralized PYRAMID knowledge graph"
                }
        else:
            # Get all component ownership information
            result = get_all_component_owners()

            if result["success"]:
                return {
                    "success": True,
                    "total_components": result["total_components"],
                    "ownership_data": result["ownership_data"],
                    "note": "Data retrieved from centralized PYRAMID knowledge graph"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to retrieve ownership data"),
                    "note": "Data retrieved from centralized PYRAMID knowledge graph"
                }

    except Exception as e:
        logger.error(f"Error getting component owners: {e}")
        return {
            "error": f"Failed to get component owners: {str(e)}",
            "component_id": component_id
        }


def get_components_by_responsible_person(person_name: str) -> Dict[str, Any]:
    """
    Get components associated with a specific person (owner, lead, etc.).

    Args:
        person_name: Name of the person to search for

    Returns:
        Dict containing components associated with the person
    """
    try:
        result = get_component_by_owner(person_name)

        if result["success"]:
            return {
                "success": True,
                "person_name": person_name,
                "total_components": result["total_found"],
                "components": result["components"],
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }
        else:
            return {
                "success": False,
                "person_name": person_name,
                "error": result.get("error", "No components found for this person"),
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }

    except Exception as e:
        logger.error(f"Error getting components by person: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "person_name": person_name,
            "components": []
        }


def get_components_by_sector(sector: str) -> Dict[str, Any]:
    """
    Get components associated with a specific sector.

    Args:
        sector: Name of the sector to search for

    Returns:
        Dict containing components associated with the sector
    """
    try:
        result = get_components_by_sector(sector)

        if result["success"]:
            return {
                "success": True,
                "sector": sector,
                "total_components": result["total_found"],
                "components": result["components"],
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }
        else:
            return {
                "success": False,
                "sector": sector,
                "error": result.get("error", "No components found for this sector"),
                "note": "Data retrieved from centralized PYRAMID knowledge graph"
            }

    except Exception as e:
        logger.error(f"Error getting components by sector: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "sector": sector,
            "components": []
        }


# Export functions
__all__ = [
    'initialize_pra_tools',
    'search_pra_components',
    'get_component_details',
    'search_component_relationships',
    'get_component_owners',
    'get_components_by_responsible_person',
    'get_components_by_sector',
]
