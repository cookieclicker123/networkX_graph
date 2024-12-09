import pytest
import os
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.groq import create_groq_client
from src.model import Query, QueryResult, EntityType, RelationType
from src.prompt import create_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def save_llm_response(query: str, response: dict, output_dir: str = "llm/test_outputs"):
    """Save LLM response to a JSON file"""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Create filename from first few words of query
    filename = "_".join(query.lower().split()[:5]).replace("'", "").replace('"', "")
    output_path = Path(output_dir) / f"{filename}.json"
    
    # Save response with query for context
    output_data = {
        "query": query,
        "response": response
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    return output_path

@pytest.mark.asyncio
async def test_graph_query():
    """Test that we can convert a natural language query into graph triplets"""
    # Arrange
    client = create_groq_client(
        model_name="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY
    )
    
    # Test query that should generate multiple triplets
    test_query = "Find me software engineers who work at Google and speak English"
    query = Query(conditions=create_prompt(test_query))
    
    # Act
    result = await client(query)
    
    # Save raw LLM response before conversion to typed objects
    raw_response = {
        "query": query.model_dump(),  # Updated from dict() to model_dump()
        "response": [list(t) for t in result.response]
    }
    response_path = save_llm_response(
        query=test_query,
        response=raw_response
    )
    print(f"\nLLM response saved to: {response_path}")
    
    # Assert
    assert isinstance(result, QueryResult)
    assert len(result.response) > 0
    
    # Verify triplet structure
    for triplet in result.response:
        assert len(triplet) == 3
        assert triplet[0] == "Person"  # Subject must be "Person"
        assert isinstance(triplet[1], RelationType)  # Relation must be a RelationType
        assert isinstance(triplet[2], str)  # Entity should be a string value 