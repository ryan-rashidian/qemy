"""Intermediate structures and validation for Tiingo price data.

Used by TiingoClient.
"""

import json
from datetime import date, datetime

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

def decode_prices_json(json_str: str) -> list[PriceData]:
    """Decode price data JSON text into pydantic based container."""
    try:
        prices_raw: list[dict] = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise JSONDecodingError('Error decoding prices JSON') from e

    try:
        return [PriceData.model_validate(price) for price in prices_raw]
    except ValidationError as e:
        raise JSONDecodingError('Error validating prices JSON') from e

class QuoteData(BaseModel):
    """Container for quote data."""
    ticker: str
    timestamp: datetime
    quote: float = Field(alias='tngoLast')

def decode_quotes_json(json_str: str) -> list[QuoteData]:
    """Decode price data JSON text into pydantic based container."""
    try:
        quotes_raw: list[dict] = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise JSONDecodingError('Error decoding quotes JSON') from e

    try:
        return [QuoteData.model_validate(quote) for quote in quotes_raw]
    except ValidationError as e:
        raise JSONDecodingError('Error validating quotes JSON') from e

