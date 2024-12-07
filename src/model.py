from typing import Callable, List
from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str
    company: str
    university: str
    languages: List[str]
    industry: str
    country: str

class Query(BaseModel):
    conditions: list[tuple[str, str, str]]

class QueryResult(BaseModel):
    query: Query
    matches: list[Person]

QueryGraph = Callable[[Query], QueryResult]
