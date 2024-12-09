from typing import Callable, List, Tuple, Dict
from pydantic import BaseModel

from enum import Enum

class EntityType(str, Enum):
    COMPANY = "company"
    UNIVERSITY = "university"
    LANGUAGES = "languages"
    INDUSTRY = "industry"
    COUNTRY = "country"

    @property
    def description(self) -> str:
        return {
            EntityType.LANGUAGES: "Languages like English, Spanish, French, etc.",
            EntityType.COMPANY: "Company names like Apple Inc., Alphabet Inc, Tesla, Microsoft, etc.",
            EntityType.UNIVERSITY: "University names like Harvard, MIT, Stanford, etc.",
            EntityType.INDUSTRY: "Industry names like Technology, Finance, software, Healthcare, etc.",
            EntityType.COUNTRY: "Country names like USA, UK, France, etc.",
        }[self]

class RelationType(str, Enum):
    WORKS_AT = "works_at"
    STUDIED_AT = "studied_at"
    SPEAKS = "speaks"
    WORKS_IN = "works_in"
    LIVES_IN = "lives_in"

    @property
    def description(self) -> str:
        return {
            RelationType.WORKS_AT: "Connects a Person to their Company",
            RelationType.STUDIED_AT: "Connects a Person to their University",
            RelationType.SPEAKS: "Connects a Person to Languages they speak",
            RelationType.WORKS_IN: "Connects a Person to their Industry",
            RelationType.LIVES_IN: "Connects a Person to their Country"
        }[self]


class Query(BaseModel):
    conditions: str

class QueryResult(BaseModel):
    query: Query
    response: List[Tuple[str, RelationType, str]]


QueryLLM = Callable[[Query], QueryResult]

    