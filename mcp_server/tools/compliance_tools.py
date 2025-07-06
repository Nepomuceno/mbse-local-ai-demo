"""
Compliance Tools for PYRAMID MCP Server

This module provides access to PYRAMID compliance information, rules, and validation capabilities.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Global processors (will be initialized by server)
pdf_processor: Optional[Any] = None
document_parser: Optional[Any] = None
data_dir: Optional[Path] = None


def initialize_compliance_tools(data_directory: Path, pdf_proc, doc_parser):
    """Initialize the compliance tools with processors and data directory."""
    global pdf_processor, document_parser, data_dir
    pdf_processor = pdf_proc
    document_parser = doc_parser
    data_dir = data_directory


def get_compliance_rules(
    category: Optional[str] = None,
    rule_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve compliance guidance and rules from PYRAMID documents.

    Args:
        category: Category filter (e.g., "Security", "Interoperability", "Data")
        rule_type: Type of rule (e.g., "must", "shall", "should")

    Returns:
        Dict containing compliance rules
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "category": category,
                "rule_type": rule_type,
                "rules": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "category": category,
                "rule_type": rule_type,
                "rules": []
            }

        rules = []

        # Find technical standard documents
        standard_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "Technical_Standard" in pdf_file.name and "Guidance" not in pdf_file.name:
                standard_files.append(pdf_file)

        # Extract rules from each document
        for pdf_file in standard_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Define rule patterns
                rule_patterns = {
                    "must": r'(\b(?:must|MUST)\b[^.!?]*[.!?])',
                    "shall": r'(\b(?:shall|SHALL)\b[^.!?]*[.!?])',
                    "should": r'(\b(?:should|SHOULD)\b[^.!?]*[.!?])',
                    "may": r'(\b(?:may|MAY)\b[^.!?]*[.!?])',
                    "will": r'(\b(?:will|WILL)\b[^.!?]*[.!?])'
                }

                # Search for rules
                for rule_category, pattern in rule_patterns.items():
                    if rule_type and rule_type.lower() != rule_category:
                        continue

                    matches = re.findall(
                        pattern, content.text, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        # Clean up the match
                        cleaned_rule = match.strip()
                        if len(cleaned_rule) > 500:  # Skip very long matches
                            continue

                        # Try to determine context/category
                        context = "General"
                        if any(term in cleaned_rule.lower() for term in ["security", "secure", "encrypt", "authentication"]):
                            context = "Security"
                        elif any(term in cleaned_rule.lower() for term in ["interoperability", "interface", "protocol"]):
                            context = "Interoperability"
                        elif any(term in cleaned_rule.lower() for term in ["data", "information", "metadata"]):
                            context = "Data Management"
                        elif any(term in cleaned_rule.lower() for term in ["system", "component", "architecture"]):
                            context = "System Architecture"
                        elif any(term in cleaned_rule.lower() for term in ["test", "validation", "verification"]):
                            context = "Testing & Validation"

                        # Apply category filter
                        if category and category.lower() not in context.lower():
                            continue

                        rules.append({
                            "rule_text": cleaned_rule,
                            "rule_type": rule_category,
                            "context": context,
                            "source_document": pdf_file.name,
                            "confidence": "high" if rule_category in ["must", "shall"] else "medium"
                        })

            except Exception as e:
                logger.error(f"Error extracting rules from {pdf_file}: {e}")
                continue

        # Sort rules by importance (must/shall first)
        rule_priority = {"must": 1, "shall": 2,
                         "should": 3, "will": 4, "may": 5}
        rules.sort(key=lambda x: rule_priority.get(x["rule_type"], 6))

        return {
            "success": True,
            "category": category,
            "rule_type": rule_type,
            "total_rules": len(rules),
            "rules": rules[:50]  # Limit to first 50 rules
        }

    except Exception as e:
        logger.error(f"Error getting compliance rules: {e}")
        return {
            "error": f"Failed to get compliance rules: {str(e)}",
            "category": category,
            "rule_type": rule_type,
            "rules": []
        }


def search_compliance_requirements(query: str) -> Dict[str, Any]:
    """
    Find specific compliance requirements based on query.

    Args:
        query: Search query for compliance requirements

    Returns:
        Dict containing matching compliance requirements
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "query": query,
                "requirements": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "query": query,
                "requirements": []
            }

        requirements = []

        # Find technical standard documents
        standard_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "Technical_Standard" in pdf_file.name:
                standard_files.append(pdf_file)

        # Search in each document
        for pdf_file in standard_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Search for query in text
                text_lower = content.text.lower()
                query_lower = query.lower()

                # Find matches
                start_pos = 0
                while len(requirements) < 20:  # Limit to 20 requirements
                    pos = text_lower.find(query_lower, start_pos)
                    if pos == -1:
                        break

                    # Extract context around match
                    context_start = max(0, pos - 200)
                    context_end = min(len(content.text),
                                      pos + len(query) + 200)
                    context = content.text[context_start:context_end]

                    # Look for requirement indicators in context
                    requirement_indicators = [
                        "must", "shall", "should", "will", "may", "requirement", "compliance"]
                    has_requirement = any(indicator in context.lower()
                                          for indicator in requirement_indicators)

                    if has_requirement:
                        # Try to extract the full requirement sentence
                        sentences = re.split(r'[.!?]+', context)
                        relevant_sentence = ""
                        for sentence in sentences:
                            if query_lower in sentence.lower():
                                relevant_sentence = sentence.strip()
                                break

                        if relevant_sentence:
                            requirements.append({
                                "requirement_text": relevant_sentence,
                                "context": context,
                                "source_document": pdf_file.name,
                                "match_position": pos,
                                "relevance": "high" if any(term in relevant_sentence.lower() for term in ["must", "shall"]) else "medium"
                            })

                    start_pos = pos + 1

            except Exception as e:
                logger.error(
                    f"Error searching for requirements in {pdf_file}: {e}")
                continue

        # Remove duplicates and sort by relevance
        seen_requirements = set()
        unique_requirements = []
        for req in requirements:
            if req["requirement_text"] not in seen_requirements:
                seen_requirements.add(req["requirement_text"])
                unique_requirements.append(req)

        # Sort by relevance
        unique_requirements.sort(
            key=lambda x: 0 if x["relevance"] == "high" else 1)

        return {
            "success": True,
            "query": query,
            "total_requirements": len(unique_requirements),
            "requirements": unique_requirements[:15]  # Limit to top 15
        }

    except Exception as e:
        logger.error(f"Error searching compliance requirements: {e}")
        return {
            "error": f"Search error: {str(e)}",
            "query": query,
            "requirements": []
        }


def get_compliance_checklist(system_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate compliance checklists for different system types.

    Args:
        system_type: Type of system (e.g., "Command and Control", "Intelligence", "Logistics")

    Returns:
        Dict containing compliance checklist
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "system_type": system_type,
                "checklist": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "system_type": system_type,
                "checklist": []
            }

        checklist_items = []

        # Find guidance documents
        guidance_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "Guidance" in pdf_file.name:
                guidance_files.append(pdf_file)

        # Extract checklist items from guidance documents
        for pdf_file in guidance_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Look for checklist patterns
                checklist_patterns = [
                    r'(?:checklist|check list|verification|validation)[\s\S]*?(?:\n\s*[-•*]\s*[^\n]+)+',
                    r'(?:requirements|criteria|steps)[\s\S]*?(?:\n\s*\d+\.\s*[^\n]+)+',
                    r'(?:must|shall|should)[\s\S]*?(?:verify|validate|ensure|confirm)'
                ]

                for pattern in checklist_patterns:
                    matches = re.findall(
                        pattern, content.text, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        if len(match) > 1000:  # Skip very long matches
                            continue

                        # Extract individual checklist items
                        items = re.findall(r'[-•*]\s*([^\n]+)', match)
                        if not items:
                            items = re.findall(r'\d+\.\s*([^\n]+)', match)

                        for item in items:
                            if len(item.strip()) > 10:  # Skip very short items
                                # Determine category
                                category = "General"
                                if any(term in item.lower() for term in ["security", "encrypt", "authentication"]):
                                    category = "Security"
                                elif any(term in item.lower() for term in ["interface", "protocol", "interoperability"]):
                                    category = "Interoperability"
                                elif any(term in item.lower() for term in ["data", "information", "metadata"]):
                                    category = "Data Management"
                                elif any(term in item.lower() for term in ["test", "validation", "verification"]):
                                    category = "Testing"

                                # Apply system type filter
                                if system_type and system_type.lower() not in item.lower():
                                    continue

                                checklist_items.append({
                                    "item": item.strip(),
                                    "category": category,
                                    "priority": "high" if any(term in item.lower() for term in ["must", "shall", "critical"]) else "medium",
                                    "source_document": pdf_file.name
                                })

            except Exception as e:
                logger.error(
                    f"Error extracting checklist from {pdf_file}: {e}")
                continue

        # Remove duplicates
        seen_items = set()
        unique_items = []
        for item in checklist_items:
            if item["item"] not in seen_items:
                seen_items.add(item["item"])
                unique_items.append(item)

        # Sort by priority and category
        unique_items.sort(key=lambda x: (
            0 if x["priority"] == "high" else 1, x["category"]))

        # Group by category
        checklist_by_category = {}
        for item in unique_items:
            category = item["category"]
            if category not in checklist_by_category:
                checklist_by_category[category] = []
            checklist_by_category[category].append(item)

        return {
            "success": True,
            "system_type": system_type,
            "total_items": len(unique_items),
            "checklist_by_category": checklist_by_category,
            "checklist": unique_items[:30]  # Limit to 30 items
        }

    except Exception as e:
        logger.error(f"Error generating compliance checklist: {e}")
        return {
            "error": f"Failed to generate checklist: {str(e)}",
            "system_type": system_type,
            "checklist": []
        }


def validate_compliance_claim(claim_text: str) -> Dict[str, Any]:
    """
    Check compliance statements against PYRAMID requirements.

    Args:
        claim_text: Text of the compliance claim to validate

    Returns:
        Dict containing validation results
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "claim_text": claim_text,
                "validation_result": "unknown"
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "claim_text": claim_text,
                "validation_result": "unknown"
            }

        validation_results = []
        potential_issues = []
        supporting_evidence = []

        # Find technical standard documents
        standard_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "Technical_Standard" in pdf_file.name:
                standard_files.append(pdf_file)

        # Search for related requirements
        for pdf_file in standard_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Extract key terms from claim
                claim_lower = claim_text.lower()
                key_terms = re.findall(r'\b[a-z]{4,}\b', claim_lower)

                # Look for relevant requirements
                for term in key_terms:
                    if term in ["with", "that", "this", "from", "have", "will", "been", "they", "them"]:
                        continue  # Skip common words

                    # Search for requirements containing this term
                    text_lower = content.text.lower()

                    # Find sentences with both the term and requirement indicators
                    sentences = re.split(r'[.!?]+', content.text)
                    for sentence in sentences:
                        sentence_lower = sentence.lower()
                        if term in sentence_lower and any(req in sentence_lower for req in ["must", "shall", "should"]):
                            # Check if this contradicts or supports the claim
                            if len(sentence.strip()) > 20:
                                supporting_evidence.append({
                                    "requirement": sentence.strip(),
                                    "source_document": pdf_file.name,
                                    "relevance": "high" if term in sentence_lower else "medium"
                                })

            except Exception as e:
                logger.error(f"Error validating against {pdf_file}: {e}")
                continue

        # Analyze compliance claim
        compliance_indicators = ["compliant", "compliance",
                                 "meets", "satisfies", "conforms", "adheres"]
        has_compliance_claim = any(indicator in claim_text.lower()
                                   for indicator in compliance_indicators)

        # Look for potential issues
        if not has_compliance_claim:
            potential_issues.append(
                "Claim does not explicitly state compliance")

        if not supporting_evidence:
            potential_issues.append(
                "No supporting evidence found in PYRAMID documents")

        # Determine validation result
        if supporting_evidence and not potential_issues:
            validation_result = "supported"
        elif supporting_evidence and potential_issues:
            validation_result = "partially_supported"
        elif not supporting_evidence and potential_issues:
            validation_result = "unsupported"
        else:
            validation_result = "unclear"

        return {
            "success": True,
            "claim_text": claim_text,
            "validation_result": validation_result,
            # Limit to 10 pieces of evidence
            "supporting_evidence": supporting_evidence[:10],
            "potential_issues": potential_issues,
            "confidence": "high" if len(supporting_evidence) > 3 else "medium"
        }

    except Exception as e:
        logger.error(f"Error validating compliance claim: {e}")
        return {
            "error": f"Validation error: {str(e)}",
            "claim_text": claim_text,
            "validation_result": "error"
        }


def get_compliance_examples(scenario: Optional[str] = None) -> Dict[str, Any]:
    """
    Access compliance examples and use cases.

    Args:
        scenario: Specific scenario type (e.g., "data exchange", "system integration")

    Returns:
        Dict containing compliance examples
    """
    try:
        if not data_dir or not data_dir.exists():
            return {
                "error": "Data directory not found",
                "scenario": scenario,
                "examples": []
            }

        if not pdf_processor:
            return {
                "error": "PDF processor not initialized",
                "scenario": scenario,
                "examples": []
            }

        examples = []

        # Find guidance documents
        guidance_files = []
        for pdf_file in data_dir.glob("*.pdf"):
            if "Guidance" in pdf_file.name:
                guidance_files.append(pdf_file)

        # Extract examples from guidance documents
        for pdf_file in guidance_files:
            try:
                content = pdf_processor.extract_pdf_content(pdf_file)

                # Look for example patterns
                example_patterns = [
                    r'(?:example|for example|use case|case study|scenario)[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:figure|table|diagram)\s*\d+[\s\S]*?(?:\n\n|\n\s*\n)',
                    r'(?:implementation|deployment|configuration)[\s\S]*?(?:\n\n|\n\s*\n)'
                ]

                for pattern in example_patterns:
                    matches = re.findall(
                        pattern, content.text, re.IGNORECASE | re.MULTILINE)

                    for match in matches:
                        if len(match.strip()) < 50 or len(match) > 1000:
                            continue  # Skip very short or very long matches

                        # Determine example type
                        example_type = "General"
                        if "data" in match.lower():
                            example_type = "Data Exchange"
                        elif "system" in match.lower():
                            example_type = "System Integration"
                        elif "interface" in match.lower():
                            example_type = "Interface"
                        elif "security" in match.lower():
                            example_type = "Security"
                        elif "test" in match.lower():
                            example_type = "Testing"

                        # Apply scenario filter
                        if scenario and scenario.lower() not in match.lower():
                            continue

                        examples.append({
                            "example_text": match.strip(),
                            "example_type": example_type,
                            "source_document": pdf_file.name,
                            "relevance": "high" if scenario and scenario.lower() in match.lower() else "medium"
                        })

            except Exception as e:
                logger.error(f"Error extracting examples from {pdf_file}: {e}")
                continue

        # Remove duplicates and sort by relevance
        seen_examples = set()
        unique_examples = []
        for example in examples:
            # Use first 100 chars as key
            example_key = example["example_text"][:100]
            if example_key not in seen_examples:
                seen_examples.add(example_key)
                unique_examples.append(example)

        # Sort by relevance
        unique_examples.sort(
            key=lambda x: 0 if x["relevance"] == "high" else 1)

        return {
            "success": True,
            "scenario": scenario,
            "total_examples": len(unique_examples),
            "examples": unique_examples[:15]  # Limit to 15 examples
        }

    except Exception as e:
        logger.error(f"Error getting compliance examples: {e}")
        return {
            "error": f"Failed to get examples: {str(e)}",
            "scenario": scenario,
            "examples": []
        }


# Export functions
__all__ = [
    'initialize_compliance_tools',
    'get_compliance_rules',
    'search_compliance_requirements',
    'get_compliance_checklist',
    'validate_compliance_claim',
    'get_compliance_examples'
]
