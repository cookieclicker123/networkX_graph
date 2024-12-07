from enum import Enum

class CSVColumn(str, Enum):
    ID = "id"
    NAME = "name"
    COMPANY = "company"
    UNIVERSITY = "university"
    LANGUAGES = "languages"
    INDUSTRY = "industry"
    COUNTRY = "country" 