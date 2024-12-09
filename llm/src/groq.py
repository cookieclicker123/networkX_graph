import aiohttp
import json
from typing import Dict
from .model import QueryLLM, Query, QueryResult

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
        parsed_triplets = json.loads(content)  # Assuming LLM returns JSON format
        
        return QueryResult(
            query=query,
            response=parsed_triplets
        )
    
    return query_llm