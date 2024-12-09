import aiohttp
import json
from typing import Dict, List, Tuple
from .model import QueryLLM, Query, QueryResult, EntityType, RelationType

async def make_groq_request(
    url: str, 
    model_name: str, 
    prompt: str, 
    api_key: str, 
    temperature: float = 0.1
) -> Dict:
    """Make a single request to Groq API and return the response"""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "stream": False,  # No streaming needed
            },
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Groq API error (status {response.status}): {error_text}")
            
            return await response.json()

def convert_to_typed_triplet(triplet: List[str]) -> Tuple[str, RelationType, str]:
    """Convert string triplet to typed triplet"""
    # First element is always "Person"
    if triplet[0] != "Person":
        raise ValueError("First element must be 'Person'")
    
    # Convert relation string to RelationType enum (handling uppercase from LLM)
    relation = RelationType(triplet[1].lower())
    
    # Keep the actual entity value from the triplet
    entity_value = triplet[2]
    
    return ("Person", relation, entity_value)

def create_groq_client(
    model_name: str,
    api_key: str,
    url: str = "https://api.groq.com/openai/v1/chat/completions",
    temperature: float = 0.1
) -> QueryLLM:
    """Creates a Groq client that converts natural language to graph queries"""
    
    async def query_llm(query: Query) -> QueryResult:
        response = await make_groq_request(
            url=url,
            model_name=model_name,
            prompt=query.conditions,
            api_key=api_key,
            temperature=temperature
        )
        
        # Extract the response content and parse it into triplets
        content = response['choices'][0]['message']['content']
        raw_triplets = json.loads(content)  # List[List[str]]
        
        # Convert each triplet to proper types
        typed_triplets = [convert_to_typed_triplet(t) for t in raw_triplets]
        
        return QueryResult(
            query=query,
            response=typed_triplets
        )
    
    return query_llm