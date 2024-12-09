"""
Entity Extraction Prompt Templates

This module contains the prompt templates and formatting utilities used by the
entity extraction agent. These templates guide the LLM in identifying and
extracting relevant entities from queries.

Templates:
    ENTITY_PROMPT: Main template for entity extraction
"""

from pathlib import Path
import json
from .model import EntityType, RelationType

ENTITY_DESCRIPTIONS = {str(entity.value): entity.description for entity in EntityType}
RELATION_DESCRIPTIONS = {str(relation.value): relation.description for relation in RelationType}

GRAPH_QUERY_PROMPT = """Convert this natural language query into knowledge graph triplets.
Each triplet represents a relationship in the format: ["Person", RELATION_TYPE, ENTITY_VALUE]

Query: {query}

Available Entity Types:
{entity_descriptions}

Available Relationship Types:
{relation_descriptions}

Examples:
{examples}

CRITICAL INSTRUCTIONS:
1. Output MUST be a JSON array of triplets ONLY
2. Each triplet must be exactly ["Person", RELATION, ENTITY_VALUE]
3. Subject is always "Person"
4. Relations must be one of: WORKS_AT, STUDIED_AT, SPEAKS, WORKS_IN, LIVES_IN
5. Entity values must be the actual names/values from the query that match the relation:
   - WORKS_AT → use actual company name (e.g., "Google", not "company")
   - STUDIED_AT → use actual university name (e.g., "Stanford", not "university")
   - SPEAKS → use actual language name (e.g., "English", not "languages")
   - WORKS_IN → use actual industry name (e.g., "Software", not "industry")
   - LIVES_IN → use actual country name (e.g., "USA", not "country")
6. No explanations or additional text - only the JSON array
7. All conditions in the query must be captured as separate triplets
8. Use exact entity names as they appear in the query
9. Invalid responses will cause system errors
10. The response must be valid JSON and parseable

Example Response Format:
[
    ["Person", "WORKS_AT", "Google"],
    ["Person", "SPEAKS", "English"],
    ["Person", "WORKS_IN", "Software"]
]

<RESPONSE>"""


def load_examples():
    examples_path = Path(__file__).parent / "examples.json"
    with open(examples_path) as f:
        return json.load(f)["examples"]


def create_prompt(query: str) -> str:
    """Creates the graph query prompt with examples."""
    examples = load_examples()
    return GRAPH_QUERY_PROMPT.format(
        query=query,
        entity_descriptions=json.dumps(ENTITY_DESCRIPTIONS, indent=2),
        relation_descriptions=json.dumps(RELATION_DESCRIPTIONS, indent=2),
        examples=json.dumps(examples, indent=2)
    )
