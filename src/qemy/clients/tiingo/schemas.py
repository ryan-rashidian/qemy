"""Intermediate structures and validation for Tiingo price data.

Used by TiingoClient.
"""

from datetime import date, datetime
import json

from pydantic import BaseModel, Field, ValidationError

from qemy.exceptions import JSONDecodingError


class PriceData(BaseModel):
    """Container for TiingoClient price data."""
    date: date
    close: float = Field(alias='adjClose')
    high: float = Field(alias='adjHigh')
    low: float = Field(alias='adjLow')
    open: float = Field(alias='adjOpen')
    volume: int = Field(alias='adjVolume')

def decode_prices_json(json_str: str) -> PriceData:
    """Decode price data JSON text into pydantic based container."""
    try:
        return PriceData.model_validate_json(json_str)
    except ValidationError as e:
        raise JSONDecodingError('Error validating prices JSON') from e

class QuoteData(BaseModel):
    """Container for quote data."""
    ticker: str
    timestamp: datetime
    quote: float = Field(alias='tngoLast')

def decode_quotes_json(json_str: str) -> dict[str, QuoteData]:
    """Decode price data JSON text into pydantic based container."""
    try:
        quotes_raw: dict[str, dict] = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise JSONDecodingError('Error decoding quotes JSON') from e

    quotes = {}
    try:
        for ticker, data in quotes_raw.items():
            valid_data = QuoteData.model_validate(data)
            quotes[ticker] = valid_data
        return quotes

    except ValidationError as e:
        raise JSONDecodingError('Error validating quotes JSON') from e

