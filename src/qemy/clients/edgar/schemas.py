"""Dataclasses representing intermediate structures of SEC filing data.

These classes provide containers for companyfacts and concepts.
Used by EDGARClient and ConceptParser within the EDGAR client.
"""

from dataclasses import dataclass, field
import json

import pandas as pd
from pydantic import BaseModel, Field, ValidationError

from qemy.utils.dataframes import normalize_financial_df
from qemy.exceptions import InvalidArgumentError, JSONDecodingError


class CompanyCIK(BaseModel):
    """Container for company CIK data."""
    cik: int = Field(alias='cik_str')
    ticker: str
    title: str

    def __repr__(self) -> str:
        return f"CompanyFacts(ticker='{self.ticker}')"

def decode_cik_json(json_str: str, ticker: str) -> CompanyCIK:
    """Decode CIK JSON text into pydantic based container."""
    ticker_lower = ticker.lower()

    try:
        raw: dict[str, dict] = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise JSONDecodingError('Error decoding CIK JSON') from e

    for entry in raw.values():
        if entry.get('ticker', '').lower() == ticker_lower:
            try:
                return CompanyCIK.model_validate(entry)
            except ValidationError as e:
                raise JSONDecodingError('Error validating CIK JSON') from e

    raise InvalidArgumentError(f'{ticker} Not found in CIK mapping data')

class Facts(BaseModel):
    """Raw EDGAR filing data."""
    concepts: dict = Field(alias='us-gaap')

    def __len__(self) -> int:
        return len(self.concepts)

class CompanyFacts(BaseModel):
    """Container for pre-parsed data from EDGAR API.
    
    Ensures type and shape of EDGAR API JSON reponse with pydantic.
    """
    cik: int
    name: str = Field(alias='entityName')
    facts: Facts

    def __repr__(self) -> str:
        return f"CompanyFacts(name='{self.name}')"

def decode_companyfacts_json(json_str: str) -> CompanyFacts:
    """Decode companyfacts JSON text into pydantic based container."""
    try:
        return CompanyFacts.model_validate_json(json_str)
    except ValidationError as e:
        raise JSONDecodingError('Error validating companyfacts JSON') from e

@dataclass
class Concept:
    """Container for parsed filings and metadata."""
    label: str = ''
    description: str = ''
    unit: str = ''
    filings: list[dict] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Concept(label='{self.label}', unit='{self.unit}')"

    def __len__(self) -> int:
        return len(self.filings)

    def to_dataframe(self) -> pd.DataFrame:
        """Format Concept filings into pandas DataFrame.

        Returns:
            pd.DataFrame: of Concept filings
        """
        concept_df = pd.DataFrame(self.filings)
        return normalize_financial_df(
            df = concept_df,
            value_col = 'val',
            date_col = 'filed'
        )

@dataclass
class ParsedCompanyFacts:
    """Container for parsed and sorted companyfacts data."""
    ticker: str
    name: str
    concepts: dict[str, Concept] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"CompanyFacts(ticker='{self.ticker}')"

    def __len__(self) -> int:
        return len(self.concepts)

