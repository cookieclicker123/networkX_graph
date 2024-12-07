from src.model import QueryGraph, Query, QueryResult, Person
import networkx as nx
import pandas as pd
from src.schema import CSVColumn

def build_graph(csv_path: str) -> QueryGraph:
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Validate columns using enum
    required_columns = {col.value for col in CSVColumn}
    if set(df.columns) != required_columns:
        raise ValueError(f"Invalid CSV columns. Expected: {[col.value for col in CSVColumn]}")
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Store the original dataframe for looking up full profiles
    people_df = df.copy()

    # Add nodes and edges for each person
    for _, row in df.iterrows():
        person_name = row[CSVColumn.NAME.value]
        
        # Add WORKS_AT relationship (Company)
        if pd.notna(row[CSVColumn.COMPANY.value]):
            G.add_edge(person_name, row[CSVColumn.COMPANY.value], relation='WORKS_AT')
        
        # Add STUDIED_AT relationship (University)
        if pd.notna(row[CSVColumn.UNIVERSITY.value]):
            G.add_edge(person_name, row[CSVColumn.UNIVERSITY.value], relation='STUDIED_AT')
        
        # Add SPEAKS relationships (Languages)
        if pd.notna(row[CSVColumn.LANGUAGES.value]):
            languages = row[CSVColumn.LANGUAGES.value].split('|')
            for lang in languages:
                G.add_edge(person_name, lang, relation='SPEAKS')
        
        # Add WORKS_IN relationship (Industry)
        if pd.notna(row[CSVColumn.INDUSTRY.value]):
            G.add_edge(person_name, row[CSVColumn.INDUSTRY.value], relation='WORKS_IN')
        
        # Add LIVES_IN relationship (Country)
        if pd.notna(row[CSVColumn.COUNTRY.value]):
            G.add_edge(person_name, row[CSVColumn.COUNTRY.value], relation='LIVES_IN')

    

    def query_graph(query: Query) -> QueryResult:
        matching_names = []
            
        for node in G.nodes():
            matches_all = True
            for subject, relation, object in query.conditions:
                edges = list(G.out_edges(node, data=True))
                    
                # General condition matching for triplets
                if not any(edge[1] == object and edge[2]['relation'] == relation for edge in edges):
                    matches_all = False
                    break
                
            if matches_all:
                matching_names.append(node)
            
        # Convert matching names to Person objects
        matches = []
        for name in matching_names:
            person_data = people_df[people_df[CSVColumn.NAME.value] == name].iloc[0]
            matches.append(Person(
                id=person_data[CSVColumn.ID.value],
                name=person_data[CSVColumn.NAME.value],
                company=person_data[CSVColumn.COMPANY.value],
                university=person_data[CSVColumn.UNIVERSITY.value],
                languages=person_data[CSVColumn.LANGUAGES.value].split('|'),
                industry=person_data[CSVColumn.INDUSTRY.value],
                country=person_data[CSVColumn.COUNTRY.value]
            ))
            
        return QueryResult(query=query, matches=matches)
    
    return query_graph


