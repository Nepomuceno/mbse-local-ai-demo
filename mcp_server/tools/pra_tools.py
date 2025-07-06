"""
PRA (PYRAMID Reference Architecture) Tools for PYRAMID MCP Server

This module provides access to PYRAMID Reference Architecture component information, 
interaction views, and deployment patterns.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging

logger = logging.getLogger(__name__)

# Global processors (will be initialized by server)
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

    Args:
        component_type: Type of component (e.g., "Core", "Optional", "Interface")
        category: Category filter (e.g., "Data", "Communication", "Security")

    Returns:
        Dict containing matching PRA components
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "component_type": component_type,
                "category": category,
                "components": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "component_type": component_type,
                "category": category,
                "components": []
            }

        components = []

        # Find PYRAMID documents
        pyramid_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "PYRAMID" in pdf_file.name:
                pyramid_files.append(pdf_file)

        # Search for components in each document
        for pdf_file in pyramid_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Component identification patterns
                component_patterns = [
                    r'(?:component|module|service|element)[:\s]+([A-Z][A-Za-z\s]+?)(?:\n|\.)',
                    r'([A-Z][A-Za-z\s]+?)\s+(?:component|module|service|element)',
                    r'(?:PRA|PYRAMID)\s+([A-Z][A-Za-z\s]+?)\s+(?:component|module)',
                    r'(?:core|optional|interface)\s+([A-Z][A-Za-z\s]+?)(?:\n|\.)',
                ]

                for pattern in component_patterns:
                    matches = re.findall(
                        pattern, content.text, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        component_name = match.strip()
                        if len(component_name) < 5 or len(component_name) > 50:
                            continue  # Skip very short or very long names

                        # Determine component type
                        comp_type = "General"
                        text_around = content.text.lower()
                        if "core" in text_around:
                            comp_type = "Core"
                        elif "optional" in text_around:
                            comp_type = "Optional"
                        elif "interface" in text_around:
                            comp_type = "Interface"
                        elif "integration" in text_around:
                            comp_type = "Integration"

                        # Apply component type filter
                        if component_type and component_type.lower() not in comp_type.lower():
                            continue

                        # Determine category
                        comp_category = "General"
                        if any(term in component_name.lower() for term in ["data", "information", "metadata"]):
                            comp_category = "Data"
                        elif any(term in component_name.lower() for term in ["communication", "network", "protocol"]):
                            comp_category = "Communication"
                        elif any(term in component_name.lower() for term in ["security", "authentication", "authorization"]):
                            comp_category = "Security"
                        elif any(term in component_name.lower() for term in ["user", "interface", "gui", "ui"]):
                            comp_category = "User Interface"
                        elif any(term in component_name.lower() for term in ["management", "control", "monitor"]):
                            comp_category = "Management"

                        # Apply category filter
                        if category and category.lower() not in comp_category.lower():
                            continue

                        # Extract description (text around the component)
                        component_pos = content.text.lower().find(component_name.lower())
                        if component_pos != -1:
                            desc_start = max(0, component_pos - 100)
                            desc_end = min(
                                len(content.text), component_pos + len(component_name) + 200)
                            description = content.text[desc_start:desc_end].strip(
                            )
                        else:
                            description = f"Component found in {pdf_file.name}"

                        components.append({
                            "name": component_name,
                            "type": comp_type,
                            "category": comp_category,
                            "description": description,
                            "source_document": pdf_file.name,
                            "confidence": "medium"
                        })

            except Exception as e:
                logger.error(
                    f"Error searching for components in {pdf_file}: {e}")
                continue

        # Remove duplicates based on component name
        seen_components = set()
        unique_components = []
        for comp in components:
            comp_key = comp["name"].lower()
            if comp_key not in seen_components:
                seen_components.add(comp_key)
                unique_components.append(comp)

        # Sort by type and category
        unique_components.sort(key=lambda x: (
            x["type"], x["category"], x["name"]))

        return {
            "success": True,
            "component_type": component_type,
            "category": category,
            "total_components": len(unique_components),
            "components": unique_components[:25]  # Limit to 25 components
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
    Get detailed information about a specific PRA component.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing detailed component information
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "component_id": component_id,
                "details": {}
            }

        if not pdf_processor or not document_parser:
            return {
                "error": "PDF processor or document parser not initialized",
                "component_id": component_id,
                "details": {}
            }

        component_details = {}
        related_info = []

        # Find PYRAMID documents
        pyramid_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "PYRAMID" in pdf_file.name:
                pyramid_files.append(pdf_file)

        # Search for detailed information about the component
        for pdf_file in pyramid_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Look for the component in the text
                text_lower = content.text.lower()
                component_lower = component_id.lower()

                # Find occurrences of the component
                pos = text_lower.find(component_lower)
                while pos != -1:
                    # Extract extended context around the component
                    context_start = max(0, pos - 300)
                    context_end = min(len(content.text),
                                      pos + len(component_id) + 500)
                    context = content.text[context_start:context_end]

                    # Look for specific types of information
                    info_types = {
                        "purpose": ["purpose", "function", "role", "responsibility"],
                        "interfaces": ["interface", "connection", "protocol", "api"],
                        "requirements": ["requirement", "must", "shall", "should"],
                        "dependencies": ["depend", "require", "need", "prerequisite"],
                        "specifications": ["specification", "standard", "protocol", "format"]
                    }

                    for info_type, keywords in info_types.items():
                        if any(keyword in context.lower() for keyword in keywords):
                            related_info.append({
                                "type": info_type,
                                "content": context,
                                "source_document": pdf_file.name,
                                "relevance": "high"
                            })

                    # Look for next occurrence
                    pos = text_lower.find(component_lower, pos + 1)
                    if len(related_info) >= 10:  # Limit to 10 pieces of information
                        break

                # Look for component in document structure
                structure = document_parser.parse_document_structure(pdf_file)
                for section in structure.sections:
                    if component_lower in section.title.lower() or component_lower in section.text_content.lower():
                        component_details["section"] = {
                            "title": section.title,
                            "content": section.text_content[:500] + "..." if len(section.text_content) > 500 else section.text_content,
                            "page_range": f"{section.page_start}-{section.page_end}",
                            "source_document": pdf_file.name
                        }
                        break

            except Exception as e:
                logger.error(
                    f"Error getting component details from {pdf_file}: {e}")
                continue

        # Analyze collected information
        if related_info:
            # Categorize information
            categorized_info = {}
            for info in related_info:
                info_type = info["type"]
                if info_type not in categorized_info:
                    categorized_info[info_type] = []
                categorized_info[info_type].append(info)

            component_details["information"] = categorized_info

        return {
            "success": True,
            "component_id": component_id,
            "found": len(related_info) > 0,
            "total_references": len(related_info),
            "details": component_details
        }

    except Exception as e:
        logger.error(f"Error getting component details: {e}")
        return {
            "error": f"Failed to get component details: {str(e)}",
            "component_id": component_id,
            "details": {}
        }


def get_interaction_views(scenario_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Access integration examples and interaction scenarios.

    Args:
        scenario_name: Specific scenario name to search for

    Returns:
        Dict containing interaction views and scenarios
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "scenario_name": scenario_name,
                "interactions": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "scenario_name": scenario_name,
                "interactions": []
            }

        interactions = []

        # Find PYRAMID documents
        pyramid_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "PYRAMID" in pdf_file.name:
                pyramid_files.append(pdf_file)

        # Search for interaction patterns
        for pdf_file in pyramid_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Interaction patterns
                interaction_patterns = [
                    r'(?:interaction|integration|interface)\s+(?:view|scenario|example|pattern)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:figure|diagram|table)\s*\d+[:\s]*(?:interaction|integration|interface)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:scenario|use case|example)[:\s]*(?:interaction|integration|interface)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:component|system)\s+(?:to|with)\s+(?:component|system)[\s\S]*?(?:\n\n|\n\s*\n)'
                ]

                for pattern in interaction_patterns:
                    matches = re.findall(
                        pattern, content.text, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        if len(match.strip()) < 50 or len(match) > 800:
                            continue  # Skip very short or very long matches

                        # Apply scenario filter
                        if scenario_name and scenario_name.lower() not in match.lower():
                            continue

                        # Determine interaction type
                        interaction_type = "General"
                        if "data" in match.lower():
                            interaction_type = "Data Exchange"
                        elif "command" in match.lower():
                            interaction_type = "Command & Control"
                        elif "service" in match.lower():
                            interaction_type = "Service Integration"
                        elif "protocol" in match.lower():
                            interaction_type = "Protocol Interaction"
                        elif "interface" in match.lower():
                            interaction_type = "Interface Definition"

                        # Extract participants (components mentioned)
                        participants = []
                        component_pattern = r'([A-Z][A-Za-z\s]+?)\s+(?:component|system|service|module)'
                        component_matches = re.findall(
                            component_pattern, match)
                        for comp in component_matches:
                            if len(comp.strip()) > 3 and comp.strip() not in participants:
                                participants.append(comp.strip())

                        interactions.append({
                            "description": match.strip(),
                            "interaction_type": interaction_type,
                            # Limit to 5 participants
                            "participants": participants[:5],
                            "source_document": pdf_file.name,
                            "relevance": "high" if scenario_name and scenario_name.lower() in match.lower() else "medium"
                        })

            except Exception as e:
                logger.error(
                    f"Error extracting interactions from {pdf_file}: {e}")
                continue

        # Remove duplicates and sort by relevance
        seen_interactions = set()
        unique_interactions = []
        for interaction in interactions:
            # Use first 100 chars as key
            interaction_key = interaction["description"][:100]
            if interaction_key not in seen_interactions:
                seen_interactions.add(interaction_key)
                unique_interactions.append(interaction)

        # Sort by relevance and type
        unique_interactions.sort(key=lambda x: (
            0 if x["relevance"] == "high" else 1, x["interaction_type"]))

        return {
            "success": True,
            "scenario_name": scenario_name,
            "total_interactions": len(unique_interactions),
            # Limit to 20 interactions
            "interactions": unique_interactions[:20]
        }

    except Exception as e:
        logger.error(f"Error getting interaction views: {e}")
        return {
            "error": f"Failed to get interaction views: {str(e)}",
            "scenario_name": scenario_name,
            "interactions": []
        }


def search_component_relationships(component_id: str) -> Dict[str, Any]:
    """
    Find relationships between components.

    Args:
        component_id: Name or identifier of the component

    Returns:
        Dict containing component relationships
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "component_id": component_id,
                "relationships": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "component_id": component_id,
                "relationships": []
            }

        relationships = []

        # Find PYRAMID documents
        pyramid_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "PYRAMID" in pdf_file.name:
                pyramid_files.append(pdf_file)

        # Search for relationships
        for pdf_file in pyramid_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Look for the component in the text
                text_lower = content.text.lower()
                component_lower = component_id.lower()

                # Find occurrences of the component
                pos = text_lower.find(component_lower)
                while pos != -1:
                    # Extract context around the component
                    context_start = max(0, pos - 200)
                    context_end = min(len(content.text),
                                      pos + len(component_id) + 300)
                    context = content.text[context_start:context_end]

                    # Look for relationship patterns
                    relationship_patterns = [
                        r'(?:connect|interface|integrate|interact|communicate)\s+(?:with|to)\s+([A-Z][A-Za-z\s]+)',
                        r'([A-Z][A-Za-z\s]+)\s+(?:connect|interface|integrate|interact|communicate)\s+(?:with|to)',
                        r'(?:depend|require|need)\s+([A-Z][A-Za-z\s]+)',
                        r'(?:provide|supply|offer)\s+(?:to|for)\s+([A-Z][A-Za-z\s]+)',
                        r'(?:use|utilize|employ)\s+([A-Z][A-Za-z\s]+)'
                    ]

                    for pattern in relationship_patterns:
                        matches = re.findall(pattern, context, re.IGNORECASE)

                        for match in matches:
                            related_component = match.strip()
                            if len(related_component) < 5 or len(related_component) > 50:
                                continue  # Skip very short or very long names

                            if related_component.lower() == component_lower:
                                continue  # Skip self-references

                            # Determine relationship type
                            relationship_type = "General"
                            if "connect" in context.lower() or "interface" in context.lower():
                                relationship_type = "Interface"
                            elif "depend" in context.lower() or "require" in context.lower():
                                relationship_type = "Dependency"
                            elif "provide" in context.lower() or "supply" in context.lower():
                                relationship_type = "Provider"
                            elif "use" in context.lower() or "utilize" in context.lower():
                                relationship_type = "Consumer"
                            elif "integrate" in context.lower() or "interact" in context.lower():
                                relationship_type = "Integration"

                            relationships.append({
                                "related_component": related_component,
                                "relationship_type": relationship_type,
                                "context": context,
                                "source_document": pdf_file.name,
                                "confidence": "medium"
                            })

                    # Look for next occurrence
                    pos = text_lower.find(component_lower, pos + 1)
                    if len(relationships) >= 15:  # Limit to 15 relationships
                        break

            except Exception as e:
                logger.error(
                    f"Error searching for relationships in {pdf_file}: {e}")
                continue

        # Remove duplicates based on related component
        seen_relationships = set()
        unique_relationships = []
        for rel in relationships:
            rel_key = (rel["related_component"].lower(),
                       rel["relationship_type"])
            if rel_key not in seen_relationships:
                seen_relationships.add(rel_key)
                unique_relationships.append(rel)

        # Sort by relationship type
        unique_relationships.sort(key=lambda x: x["relationship_type"])

        return {
            "success": True,
            "component_id": component_id,
            "total_relationships": len(unique_relationships),
            # Limit to 12 relationships
            "relationships": unique_relationships[:12]
        }

    except Exception as e:
        logger.error(f"Error searching component relationships: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "component_id": component_id,
            "relationships": []
        }


def get_deployment_patterns(use_case: Optional[str] = None) -> Dict[str, Any]:
    """
    Get common deployment configurations and patterns.

    Args:
        use_case: Specific use case to filter patterns

    Returns:
        Dict containing deployment patterns
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "use_case": use_case,
                "patterns": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "use_case": use_case,
                "patterns": []
            }

        patterns = []

        # Find PYRAMID documents
        pyramid_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "PYRAMID" in pdf_file.name:
                pyramid_files.append(pdf_file)

        # Search for deployment patterns
        for pdf_file in pyramid_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Deployment pattern keywords
                deployment_patterns = [
                    r'(?:deployment|configuration|setup|installation|implementation)\s+(?:pattern|example|scenario|approach)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:architecture|topology|structure)\s+(?:for|in|of)\s+(?:deployment|implementation)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:distributed|centralized|hybrid|cloud|on-premise)\s+(?:deployment|configuration)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:figure|diagram|table)\s*\d+[:\s]*(?:deployment|configuration|architecture)[\s\S]*?(?:\n\n|\n\s*\n)'
                ]

                for pattern in deployment_patterns:
                    matches = re.findall(
                        pattern, content.text, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        if len(match.strip()) < 50 or len(match) > 800:
                            continue  # Skip very short or very long matches

                        # Apply use case filter
                        if use_case and use_case.lower() not in match.lower():
                            continue

                        # Determine pattern type
                        pattern_type = "General"
                        if "distributed" in match.lower():
                            pattern_type = "Distributed"
                        elif "centralized" in match.lower():
                            pattern_type = "Centralized"
                        elif "hybrid" in match.lower():
                            pattern_type = "Hybrid"
                        elif "cloud" in match.lower():
                            pattern_type = "Cloud"
                        elif "on-premise" in match.lower():
                            pattern_type = "On-Premise"
                        elif "federated" in match.lower():
                            pattern_type = "Federated"

                        # Extract key components mentioned
                        components = []
                        component_pattern = r'([A-Z][A-Za-z\s]+?)\s+(?:component|system|service|module)'
                        component_matches = re.findall(
                            component_pattern, match)
                        for comp in component_matches:
                            if len(comp.strip()) > 3 and comp.strip() not in components:
                                components.append(comp.strip())

                        patterns.append({
                            "description": match.strip(),
                            "pattern_type": pattern_type,
                            # Limit to 5 components
                            "components": components[:5],
                            "source_document": pdf_file.name,
                            "relevance": "high" if use_case and use_case.lower() in match.lower() else "medium"
                        })

            except Exception as e:
                logger.error(
                    f"Error extracting deployment patterns from {pdf_file}: {e}")
                continue

        # Remove duplicates and sort by relevance
        seen_patterns = set()
        unique_patterns = []
        for pattern in patterns:
            # Use first 100 chars as key
            pattern_key = pattern["description"][:100]
            if pattern_key not in seen_patterns:
                seen_patterns.add(pattern_key)
                unique_patterns.append(pattern)

        # Sort by relevance and type
        unique_patterns.sort(key=lambda x: (
            0 if x["relevance"] == "high" else 1, x["pattern_type"]))

        return {
            "success": True,
            "use_case": use_case,
            "total_patterns": len(unique_patterns),
            "patterns": unique_patterns[:15]  # Limit to 15 patterns
        }

    except Exception as e:
        logger.error(f"Error getting deployment patterns: {e}")
        return {
            "error": f"Failed to get deployment patterns: {str(e)}",
            "use_case": use_case,
            "patterns": []
        }


# Export functions
__all__ = [
    'initialize_pra_tools',
    'search_pra_components',
    'get_component_details',
    'get_interaction_views',
    'search_component_relationships',
    'get_deployment_patterns'
]
