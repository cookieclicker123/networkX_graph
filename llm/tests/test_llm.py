import pytest
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.groq import make_groq_request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@pytest.mark.asyncio
async def test_groq_connectivity():
    """Test 1: Simply verify we can connect to Groq API"""
    try:
        response = await make_groq_request(
            url="https://api.groq.com/openai/v1/chat/completions",
            model_name="llama-3.3-70b-versatile",
            prompt="Hello",
            api_key=GROQ_API_KEY
        )
        assert response is not None
        assert 'choices' in response
    except Exception as e:
        pytest.fail(f"Failed to connect to Groq API: {str(e)}")

@pytest.mark.asyncio
async def test_groq_response():
    """Test 2: Verify we get a proper response string back"""
    response = await make_groq_request(
        url="https://api.groq.com/openai/v1/chat/completions",
        model_name="llama-3.3-70b-versatile",
        prompt="Say 'test successful'",
        api_key=GROQ_API_KEY
    )
    
    content = response['choices'][0]['message']['content']
    assert isinstance(content, str)
    assert len(content) > 0