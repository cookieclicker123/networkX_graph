from typing import Callable, List, Tuple, Dict
from pydantic import BaseModel

from enum import Enum

class EntityType(str, Enum):
    COMPANY = "company"
    UNIVERSITY = "university"
    LANGUAGES = "languages"
    INDUSTRY = "industry"
    COUNTRY = "country"

class RelationType(str, Enum):
    WORKS_AT = "works_at"
    STUDIED_AT = "studied_at"
    SPEAKS = "speaks"
    WORKS_IN = "works_in"
    LIVES_IN = "lives_in"


class Query(BaseModel):
    conditions: str

class QueryResult(BaseModel):
    query: Query
    response: List[Tuple[EntityType, RelationType, EntityType]]


QueryLLM = Callable[[Query], QueryResult]

    