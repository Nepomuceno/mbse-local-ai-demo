"""
Mock PYRAMID Knowledge Graph Data

This module contains a centralized mock knowledge graph for PYRAMID PRA components,
including component definitions, relationships, and ownership information.
Based on the PYRAMID Technical Standard documentation.
"""

from typing import Dict, Any

# Mock PRA Component Knowledge Graph
PYRAMID_KNOWLEDGE_GRAPH = {
    "components": {
        # Core Components - Data Management
        "Data Management Service": {
            "type": "Core",
            "category": "Data",
            "description": "Core service responsible for managing data ingestion, storage, and retrieval across the PYRAMID architecture.",
            "responsibilities": [
                "To capture and manage data requirements across system lifecycle",
                "To ensure data consistency, integrity, and availability",
                "To provide unified interface for data operations",
                "To support both structured and unstructured data",
                "To manage data retention and archival policies"
            ],
            "interfaces": [
                "Data Ingestion API",
                "Data Retrieval API",
                "Data Storage Interface",
                "Metadata Management Interface"
            ],
            "dependencies": [
                "Security Authentication Module",
                "Storage",
                "Information Brokerage"
            ],
            "provides_to": [
                "Data Fusion",
                "Information Brokerage",
                "Data Distribution"
            ],
            "specifications": [
                "ISO/IEC 11179 for metadata management",
                "GDPR compliance for data protection",
                "Defence Standard 00-970 for airworthiness"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "high"
        },

        "Security Authentication Module": {
            "type": "Core",
            "category": "Security",
            "description": "Essential security component that handles user authentication and authorization for all PYRAMID services.",
            "responsibilities": [
                "To provide centralized authentication services",
                "To manage user authorization and access control",
                "To enforce security policies across components",
                "To log all authentication attempts",
                "To support multi-factor authentication"
            ],
            "interfaces": [
                "Authentication API",
                "Authorization Interface",
                "Security Policy Interface",
                "Audit Trail Interface"
            ],
            "dependencies": [
                "User Directory Service",
                "Cryptographic Materials",
                "Audit Trail Processor"
            ],
            "provides_to": [
                "Data Management Service",
                "User Accounts",
                "User Roles"
            ],
            "specifications": [
                "NIST SP 800-63B guidelines",
                "OAuth2 protocol support",
                "SAML protocol support"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "high"
        },

        "Integration Bus": {
            "type": "Core",
            "category": "Communication",
            "description": "Core integration component that enables seamless communication between various PYRAMID services.",
            "responsibilities": [
                "To provide unified communication infrastructure",
                "To manage inter-component message routing",
                "To ensure reliable message delivery",
                "To support various communication protocols",
                "To handle message transformation and validation"
            ],
            "interfaces": [
                "Message Routing Interface",
                "Protocol Adapter Interface",
                "Service Discovery Interface",
                "Communication Management Interface"
            ],
            "dependencies": [
                "Communication Links",
                "Networks",
                "Network Routes"
            ],
            "provides_to": [
                "Data Management Service",
                "Information Brokerage",
                "Communication Protocol Handler"
            ],
            "specifications": [
                "DDS (Data Distribution Service) compliance",
                "STANAG 4586 for UCS interoperability",
                "MIL-STD-6016H for tactical data links"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "high"
        },

        "Data Exchange Broker": {
            "type": "Core",
            "category": "Data",
            "description": "Core component that facilitates secure data exchange between different systems and organizations.",
            "responsibilities": [
                "To manage secure data exchange protocols",
                "To handle data format conversions",
                "To enforce data sharing policies",
                "To manage cross-domain data transfers",
                "To ensure data integrity during exchange"
            ],
            "interfaces": [
                "Data Exchange API",
                "Format Conversion Interface",
                "Policy Enforcement Interface",
                "Cross-Domain Interface"
            ],
            "dependencies": [
                "Security Authentication Module",
                "Cryptographic Methods",
                "Data Management Service"
            ],
            "provides_to": [
                "Information Brokerage",
                "Data Distribution",
                "External Systems"
            ],
            "specifications": [
                "NATO STANAG data exchange standards",
                "GDPR compliance for data transfers",
                "Military security classifications"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "high"
        },

        # Interface Components
        "Communication Protocol Handler": {
            "type": "Interface",
            "category": "Communication",
            "description": "Interface component that manages communication protocols between different PYRAMID components.",
            "responsibilities": [
                "To handle protocol-specific communication",
                "To manage protocol negotiations",
                "To provide protocol abstraction layer",
                "To ensure protocol compatibility",
                "To monitor communication quality"
            ],
            "interfaces": [
                "Protocol Management Interface",
                "Communication Quality Interface",
                "Protocol Negotiation Interface"
            ],
            "dependencies": [
                "Integration Bus",
                "Communication Links",
                "Networks"
            ],
            "provides_to": [
                "External Communication Systems",
                "Legacy Systems",
                "Third-party Applications"
            ],
            "specifications": [
                "TCP/IP protocol suite",
                "Military communication standards",
                "NATO interoperability requirements"
            ],
            "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
            "confidence": "medium"
        },

        "User Interface Gateway": {
            "type": "Interface",
            "category": "User Interface",
            "description": "Gateway component that provides standardized user interface access to PYRAMID services.",
            "responsibilities": [
                "To provide unified user interface access",
                "To manage user session state",
                "To handle user interface events",
                "To ensure consistent user experience",
                "To support multiple interface types"
            ],
            "interfaces": [
                "User Interface API",
                "Session Management Interface",
                "Event Handling Interface",
                "Multi-modal Interface"
            ],
            "dependencies": [
                "Security Authentication Module",
                "User Accounts",
                "HMI Dialogue"
            ],
            "provides_to": [
                "Human Interaction",
                "Information Presentation",
                "User Applications"
            ],
            "specifications": [
                "ARINC 661-6 for cockpit displays",
                "Web accessibility standards",
                "Military HMI requirements"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "medium"
        },

        # Optional Components
        "System Monitor": {
            "type": "Optional",
            "category": "Management",
            "description": "Optional monitoring component that tracks system performance and health metrics.",
            "responsibilities": [
                "To monitor system performance metrics",
                "To detect system anomalies",
                "To generate system health reports",
                "To provide real-time monitoring",
                "To support predictive maintenance"
            ],
            "interfaces": [
                "Performance Monitoring Interface",
                "Health Metrics Interface",
                "Alert Management Interface",
                "Reporting Interface"
            ],
            "dependencies": [
                "Health Assessment",
                "Anomaly Detection",
                "Data Management Service"
            ],
            "provides_to": [
                "Configuration Manager",
                "Maintenance Systems",
                "Operational Staff"
            ],
            "specifications": [
                "ISO 13374 for condition monitoring",
                "SNMP for network monitoring",
                "Military system monitoring standards"
            ],
            "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
            "confidence": "medium"
        },

        "Network Security Filter": {
            "type": "Optional",
            "category": "Security",
            "description": "Optional security component that provides additional network-level filtering and protection.",
            "responsibilities": [
                "To filter network traffic based on security policies",
                "To detect and prevent network intrusions",
                "To monitor network security events",
                "To provide network access control",
                "To support security incident response"
            ],
            "interfaces": [
                "Network Filtering Interface",
                "Intrusion Detection Interface",
                "Security Event Interface",
                "Access Control Interface"
            ],
            "dependencies": [
                "Security Authentication Module",
                "Networks",
                "Cyber Defence"
            ],
            "provides_to": [
                "Network Security Services",
                "Security Operations Center",
                "Incident Response Team"
            ],
            "specifications": [
                "NIST Cybersecurity Framework",
                "NATO security standards",
                "Military network protection requirements"
            ],
            "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
            "confidence": "medium"
        },

        "Configuration Manager": {
            "type": "Optional",
            "category": "Management",
            "description": "Management component that handles configuration settings and deployment parameters.",
            "responsibilities": [
                "To manage system configuration settings",
                "To handle deployment parameters",
                "To support configuration versioning",
                "To ensure configuration consistency",
                "To provide configuration validation"
            ],
            "interfaces": [
                "Configuration Management Interface",
                "Deployment Interface",
                "Version Control Interface",
                "Validation Interface"
            ],
            "dependencies": [
                "Storage",
                "Security Authentication Module",
                "Data Management Service"
            ],
            "provides_to": [
                "System Components",
                "Deployment Services",
                "System Administrators"
            ],
            "specifications": [
                "ITIL configuration management",
                "DevOps configuration practices",
                "Military configuration control"
            ],
            "source_document": "PYRAMID_Technical_Standard_Guidance_V1.pdf",
            "confidence": "medium"
        },

        "Audit Trail Processor": {
            "type": "Optional",
            "category": "Security",
            "description": "Security component that maintains comprehensive audit trails for compliance and monitoring.",
            "responsibilities": [
                "To record all system activities",
                "To maintain audit trail integrity",
                "To support compliance reporting",
                "To provide audit trail analysis",
                "To ensure non-repudiation"
            ],
            "interfaces": [
                "Audit Logging Interface",
                "Compliance Reporting Interface",
                "Trail Analysis Interface",
                "Integrity Verification Interface"
            ],
            "dependencies": [
                "Security Authentication Module",
                "Storage",
                "Cryptographic Methods"
            ],
            "provides_to": [
                "Compliance Officers",
                "Security Analysts",
                "Audit Systems"
            ],
            "specifications": [
                "ISO 27001 audit requirements",
                "GDPR audit trail requirements",
                "Military audit standards"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "medium"
        },

        # Additional Core Components based on PYRAMID Technical Standard
        "Data Fusion": {
            "type": "Core",
            "category": "Data",
            "description": "Core component that combines data from multiple sources to create comprehensive situational awareness.",
            "responsibilities": [
                "To fuse data from multiple sensors and sources",
                "To resolve data conflicts and inconsistencies",
                "To provide unified situational picture",
                "To support multi-level data fusion",
                "To maintain data provenance"
            ],
            "interfaces": [
                "Data Fusion API",
                "Source Integration Interface",
                "Fusion Results Interface",
                "Confidence Assessment Interface"
            ],
            "dependencies": [
                "Data Management Service",
                "Sensor Data Interpretation",
                "Information Brokerage"
            ],
            "provides_to": [
                "Tactical Objects",
                "Situational Awareness Systems",
                "Decision Support Systems"
            ],
            "specifications": [
                "JDL Data Fusion Model",
                "NATO STANAG fusion standards",
                "Multi-source data fusion algorithms"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "high"
        },

        "Information Brokerage": {
            "type": "Core",
            "category": "Data",
            "description": "Core component that manages information discovery, access, and distribution across the system.",
            "responsibilities": [
                "To provide information discovery services",
                "To manage information access rights",
                "To broker information requests",
                "To optimize information distribution",
                "To maintain information catalogs"
            ],
            "interfaces": [
                "Information Discovery Interface",
                "Access Control Interface",
                "Brokerage API",
                "Catalog Management Interface"
            ],
            "dependencies": [
                "Security Authentication Module",
                "Data Management Service",
                "Integration Bus"
            ],
            "provides_to": [
                "Information Consumers",
                "Decision Support Systems",
                "External Information Systems"
            ],
            "specifications": [
                "Service-oriented architecture patterns",
                "Information sharing standards",
                "Military information exchange requirements"
            ],
            "source_document": "PYRAMID_Technical_Standard_V1.pdf",
            "confidence": "high"
        }
    },

    # Component Ownership and Responsibility
    "component_ownership": {
        "Data Management Service": {
            "primary_owner": "Data Architecture Team",
            "technical_lead": "Sarah Johnson",
            "business_owner": "Information Management Division",
            "development_team": "Core Data Team",
            "sectors": ["Defence", "Aviation", "System Integration"],
            "stakeholders": [
                {"name": "Chief Data Officer", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Michael Chen", "role": "Technical Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Emma Thompson", "role": "Data Governance Lead",
                    "organization": "Information Management Division"},
                {"name": "James Wilson", "role": "Integration Specialist",
                    "organization": "System Integration Team"}
            ],
            "contact_info": {
                "email": "data-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Data Management Core"
            }
        },

        "Security Authentication Module": {
            "primary_owner": "Security Architecture Team",
            "technical_lead": "David Rodriguez",
            "business_owner": "Cybersecurity Division",
            "development_team": "Security Core Team",
            "sectors": ["Defence", "Cybersecurity", "Identity Management"],
            "stakeholders": [
                {"name": "Chief Security Officer", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Alice Parker", "role": "Security Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Robert Brown", "role": "Identity Management Lead",
                    "organization": "Cybersecurity Division"},
                {"name": "Lisa Anderson", "role": "Security Operations Manager",
                    "organization": "Security Operations Center"}
            ],
            "contact_info": {
                "email": "security-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Security Core"
            }
        },

        "Integration Bus": {
            "primary_owner": "Integration Architecture Team",
            "technical_lead": "Maria Garcia",
            "business_owner": "System Integration Division",
            "development_team": "Integration Core Team",
            "sectors": ["Defence", "System Integration", "Communications"],
            "stakeholders": [
                {"name": "Chief Integration Officer", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Kevin Liu", "role": "Integration Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Jennifer Davis", "role": "Communications Lead",
                    "organization": "System Integration Division"},
                {"name": "Thomas Miller", "role": "Middleware Specialist",
                    "organization": "Integration Core Team"}
            ],
            "contact_info": {
                "email": "integration-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Integration Core"
            }
        },

        "Data Exchange Broker": {
            "primary_owner": "Data Exchange Team",
            "technical_lead": "Amanda White",
            "business_owner": "Interoperability Division",
            "development_team": "Data Exchange Core Team",
            "sectors": ["Defence", "Interoperability", "Data Exchange"],
            "stakeholders": [
                {"name": "Interoperability Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Paul Martinez", "role": "Data Exchange Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Catherine Taylor", "role": "Standards Compliance Lead",
                    "organization": "Interoperability Division"},
                {"name": "Steven Clark", "role": "Protocol Specialist",
                    "organization": "Data Exchange Core Team"}
            ],
            "contact_info": {
                "email": "dataexchange-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Data Exchange Core"
            }
        },

        "Communication Protocol Handler": {
            "primary_owner": "Communications Team",
            "technical_lead": "Brian Johnson",
            "business_owner": "Communications Division",
            "development_team": "Communications Interface Team",
            "sectors": ["Defence", "Communications", "Protocol Management"],
            "stakeholders": [
                {"name": "Communications Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Helen Zhang", "role": "Communications Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Peter Wilson", "role": "Protocol Standards Lead",
                    "organization": "Communications Division"},
                {"name": "Rachel Green", "role": "Network Integration Specialist",
                    "organization": "Communications Interface Team"}
            ],
            "contact_info": {
                "email": "comms-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Communications Interface"
            }
        },

        "User Interface Gateway": {
            "primary_owner": "User Experience Team",
            "technical_lead": "Jessica Adams",
            "business_owner": "Human Factors Division",
            "development_team": "UI/UX Core Team",
            "sectors": ["Defence", "Human Factors", "User Experience"],
            "stakeholders": [
                {"name": "Human Factors Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Mark Thompson", "role": "UX Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Sophie Evans", "role": "Human Factors Lead",
                    "organization": "Human Factors Division"},
                {"name": "Daniel Moore", "role": "Interface Design Specialist",
                    "organization": "UI/UX Core Team"}
            ],
            "contact_info": {
                "email": "ux-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "UI/UX Core"
            }
        },

        "System Monitor": {
            "primary_owner": "System Management Team",
            "technical_lead": "Christopher Lee",
            "business_owner": "Operations Division",
            "development_team": "System Management Team",
            "sectors": ["Defence", "System Management", "Operations"],
            "stakeholders": [
                {"name": "Operations Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Angela Foster", "role": "System Management Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Marcus Turner", "role": "Operations Lead",
                    "organization": "Operations Division"},
                {"name": "Karen Phillips", "role": "Monitoring Specialist",
                    "organization": "System Management Team"}
            ],
            "contact_info": {
                "email": "sysmanagement-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "System Management"
            }
        },

        "Network Security Filter": {
            "primary_owner": "Network Security Team",
            "technical_lead": "Michelle Roberts",
            "business_owner": "Network Security Division",
            "development_team": "Network Security Core Team",
            "sectors": ["Defence", "Network Security", "Cybersecurity"],
            "stakeholders": [
                {"name": "Network Security Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. George Kumar", "role": "Network Security Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Linda Wright", "role": "Network Security Lead",
                    "organization": "Network Security Division"},
                {"name": "Anthony Scott", "role": "Network Protection Specialist",
                    "organization": "Network Security Core Team"}
            ],
            "contact_info": {
                "email": "netsec-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Network Security Core"
            }
        },

        "Configuration Manager": {
            "primary_owner": "Configuration Management Team",
            "technical_lead": "Patricia Martinez",
            "business_owner": "Configuration Management Division",
            "development_team": "Configuration Core Team",
            "sectors": ["Defence", "Configuration Management", "DevOps"],
            "stakeholders": [
                {"name": "Configuration Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Ryan Campbell", "role": "Configuration Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Michelle Baker", "role": "Configuration Lead",
                    "organization": "Configuration Management Division"},
                {"name": "Joseph King", "role": "Configuration Specialist",
                    "organization": "Configuration Core Team"}
            ],
            "contact_info": {
                "email": "config-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Configuration Core"
            }
        },

        "Audit Trail Processor": {
            "primary_owner": "Audit and Compliance Team",
            "technical_lead": "Edward Nelson",
            "business_owner": "Compliance Division",
            "development_team": "Audit Core Team",
            "sectors": ["Defence", "Compliance", "Audit"],
            "stakeholders": [
                {"name": "Compliance Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Victoria Hall", "role": "Audit Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Andrew Cooper", "role": "Compliance Lead",
                    "organization": "Compliance Division"},
                {"name": "Diana Lewis", "role": "Audit Specialist",
                    "organization": "Audit Core Team"}
            ],
            "contact_info": {
                "email": "audit-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Audit Core"
            }
        },

        "Data Fusion": {
            "primary_owner": "Data Fusion Team",
            "technical_lead": "Gregory Walker",
            "business_owner": "Intelligence Division",
            "development_team": "Data Fusion Core Team",
            "sectors": ["Defence", "Intelligence", "Data Fusion"],
            "stakeholders": [
                {"name": "Intelligence Director", "role": "Executive Sponsor",
                    "organization": "Ministry of Defence"},
                {"name": "Dr. Nicole Perry", "role": "Data Fusion Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Benjamin Carter", "role": "Intelligence Lead",
                    "organization": "Intelligence Division"},
                {"name": "Sharon Hughes", "role": "Fusion Algorithm Specialist",
                    "organization": "Data Fusion Core Team"}
            ],
            "contact_info": {
                "email": "datafusion-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Data Fusion Core"
            }
        },

        "Information Brokerage": {
            "primary_owner": "Information Brokerage Team",
            "technical_lead": "Sandra Richardson",
            "business_owner": "Information Services Division",
            "development_team": "Information Brokerage Core Team",
            "sectors": ["Defence", "Information Services", "Data Brokerage"],
            "stakeholders": [
                {"name": "Information Services Director",
                    "role": "Executive Sponsor", "organization": "Ministry of Defence"},
                {"name": "Dr. Jonathan Ward", "role": "Information Brokerage Architect",
                    "organization": "PYRAMID Programme"},
                {"name": "Rebecca Morgan", "role": "Information Services Lead",
                    "organization": "Information Services Division"},
                {"name": "Kenneth Ross", "role": "Information Broker Specialist",
                    "organization": "Information Brokerage Core Team"}
            ],
            "contact_info": {
                "email": "infobrokerage-team@pyramid.mod.gov.uk",
                "phone": "+44 20 7218 xxxx",
                "teams_channel": "Information Brokerage Core"
            }
        }
    },

    # Relationship mappings
    "relationships": {
        "depends_on": {
            "Data Management Service": ["Security Authentication Module", "Storage", "Information Brokerage"],
            "Security Authentication Module": ["User Directory Service", "Cryptographic Materials", "Audit Trail Processor"],
            "Integration Bus": ["Communication Links", "Networks", "Network Routes"],
            "Data Exchange Broker": ["Security Authentication Module", "Cryptographic Methods", "Data Management Service"],
            "Communication Protocol Handler": ["Integration Bus", "Communication Links", "Networks"],
            "User Interface Gateway": ["Security Authentication Module", "User Accounts", "HMI Dialogue"],
            "System Monitor": ["Health Assessment", "Anomaly Detection", "Data Management Service"],
            "Network Security Filter": ["Security Authentication Module", "Networks", "Cyber Defence"],
            "Configuration Manager": ["Storage", "Security Authentication Module", "Data Management Service"],
            "Audit Trail Processor": ["Security Authentication Module", "Storage", "Cryptographic Methods"],
            "Data Fusion": ["Data Management Service", "Sensor Data Interpretation", "Information Brokerage"],
            "Information Brokerage": ["Security Authentication Module", "Data Management Service", "Integration Bus"]
        },

        "provides_to": {
            "Data Management Service": ["Data Fusion", "Information Brokerage", "Data Distribution"],
            "Security Authentication Module": ["Data Management Service", "User Accounts", "User Roles"],
            "Integration Bus": ["Data Management Service", "Information Brokerage", "Communication Protocol Handler"],
            "Data Exchange Broker": ["Information Brokerage", "Data Distribution", "External Systems"],
            "Communication Protocol Handler": ["External Communication Systems", "Legacy Systems", "Third-party Applications"],
            "User Interface Gateway": ["Human Interaction", "Information Presentation", "User Applications"],
            "System Monitor": ["Configuration Manager", "Maintenance Systems", "Operational Staff"],
            "Network Security Filter": ["Network Security Services", "Security Operations Center", "Incident Response Team"],
            "Configuration Manager": ["System Components", "Deployment Services", "System Administrators"],
            "Audit Trail Processor": ["Compliance Officers", "Security Analysts", "Audit Systems"],
            "Data Fusion": ["Tactical Objects", "Situational Awareness Systems", "Decision Support Systems"],
            "Information Brokerage": ["Information Consumers", "Decision Support Systems", "External Information Systems"]
        }
    },

    # Metadata about the knowledge graph
    "metadata": {
        "version": "1.0",
        "created_date": "2025-07-07",
        "last_updated": "2025-07-07",
        "source": "PYRAMID Technical Standard V1.0",
        "total_components": 12,
        "component_types": {
            "Core": 6,
            "Interface": 2,
            "Optional": 4
        },
        "categories": {
            "Data": 4,
            "Security": 3,
            "Communication": 2,
            "Management": 2,
            "User Interface": 1
        },
        "notes": "This is a mock knowledge graph based on PYRAMID Technical Standard documentation. In a real implementation, this would be populated from parsed PDF documents and maintained in a proper graph database."
    }
}


def query_knowledge_graph(query_type: str, **kwargs) -> Dict[str, Any]:
    """
    Query the mock PYRAMID knowledge graph.

    Args:
        query_type: Type of query ('component', 'relationship', 'ownership', 'search')
        **kwargs: Additional query parameters

    Returns:
        Query results
    """
    graph = PYRAMID_KNOWLEDGE_GRAPH

    if query_type == "component":
        component_id = kwargs.get("component_id")
        if component_id in graph["components"]:
            return {
                "success": True,
                "component": graph["components"][component_id]
            }
        return {"success": False, "error": "Component not found"}

    elif query_type == "relationship":
        component_id = kwargs.get("component_id")
        rel_type = kwargs.get("relationship_type", "all")

        if component_id not in graph["components"]:
            return {"success": False, "error": "Component not found"}

        relationships = []

        if rel_type in ["all", "depends_on"]:
            deps = graph["relationships"]["depends_on"].get(component_id, [])
            for dep in deps:
                relationships.append({
                    "related_component": dep,
                    "relationship_type": "Dependency",
                    "context": f"{component_id} depends on {dep}",
                    "confidence": "high"
                })

        if rel_type in ["all", "provides_to"]:
            provides = graph["relationships"]["provides_to"].get(
                component_id, [])
            for prov in provides:
                relationships.append({
                    "related_component": prov,
                    "relationship_type": "Provider",
                    "context": f"{component_id} provides services to {prov}",
                    "confidence": "high"
                })

        return {
            "success": True,
            "relationships": relationships
        }

    elif query_type == "ownership":
        component_id = kwargs.get("component_id")
        if component_id in graph["component_ownership"]:
            return {
                "success": True,
                "ownership": graph["component_ownership"][component_id]
            }
        return {"success": False, "error": "Ownership information not found"}

    elif query_type == "search":
        component_type = kwargs.get("component_type")
        category = kwargs.get("category")

        components = []
        for comp_id, comp_data in graph["components"].items():
            if component_type and component_type.lower() not in comp_data["type"].lower():
                continue
            if category and category.lower() not in comp_data["category"].lower():
                continue

            components.append({
                "name": comp_id,
                **comp_data
            })

        return {
            "success": True,
            "components": components
        }

    return {"success": False, "error": "Invalid query type"}


def get_all_component_owners() -> Dict[str, Any]:
    """Get all component ownership information."""
    return {
        "success": True,
        "ownership_data": PYRAMID_KNOWLEDGE_GRAPH["component_ownership"],
        "total_components": len(PYRAMID_KNOWLEDGE_GRAPH["component_ownership"])
    }


def get_component_by_owner(owner_name: str) -> Dict[str, Any]:
    """Get components owned by a specific person or team."""
    components = []

    for comp_id, ownership in PYRAMID_KNOWLEDGE_GRAPH["component_ownership"].items():
        if (owner_name.lower() in ownership["primary_owner"].lower() or
            owner_name.lower() in ownership["technical_lead"].lower() or
                owner_name.lower() in ownership["business_owner"].lower()):
            components.append({
                "component": comp_id,
                "ownership": ownership
            })

    return {
        "success": True,
        "components": components,
        "total_found": len(components)
    }


def get_components_by_sector(sector: str) -> Dict[str, Any]:
    """Get components associated with a specific sector."""
    components = []

    for comp_id, ownership in PYRAMID_KNOWLEDGE_GRAPH["component_ownership"].items():
        if any(sector.lower() in s.lower() for s in ownership["sectors"]):
            components.append({
                "component": comp_id,
                "ownership": ownership
            })

    return {
        "success": True,
        "components": components,
        "total_found": len(components)
    }
