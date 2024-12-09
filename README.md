# Knowledge Graph POC
This repo is for trying out solutions to search a knowledge graph for nodes that match a query.

## Installation

```bash
git clone git@github.com:cookieclicker123/networkX_graph.git
cd networkX_graph
```

### Virtual Environment Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Graph Test

```bash
# Run individual test suites
pytest tests/test_graph.py

# Or run all tests
pytest test/
```

## Running the LLM Test

```bash
#Retrieve free API key from Groq console by signing up
touch .env
echo "GROQ_API_KEY=<your-api-key>" >> .env

# Run individual test suites
pytest llm/tests/test_llm.py

# Or run all tests
pytest llm/tests/
```

## Technical Details

### Graph Structure

Using the CSV test data in clean_data.csv creates a knowledge graph with the following types of Nodes:

- Person
- University
- Company
- Language (Note that languages need to be split out from the languages column)
- Industry
- Country

With the following Edges:

- Person -> University (STUDIED_AT)
- Person -> Language (SPEAKS)
- Person -> Industry (WORKS_IN)
- Person -> Country (LIVES_IN)
- Person -> Company (WORKS_AT)
