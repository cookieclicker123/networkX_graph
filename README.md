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
pytest llm/tests/test_queryResult.py

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

## LLM workflow

```bash
We should return a list of lists of strings, containing the triplets in the format ["Person", RELATION, ENTITY].
By doing this in strict json, we can prove that the LLM is returning the correct format, and besides we have already proven that once the graph recieves its triplets in the strict
queryResult data structure, it always works.

Thus, in isolation, we have proven that both networkX can easily be queried with graph friendly data model API Queries, and the LLM can easily produce this from natural language, meaning we need only synthesise the two components to build the end to end knowledge graph from here. This spearation of concerns allows us to adhere to the principles of Test Driven Development and move faster.
```



