"""Intermediate structures and validation for FRED observations data.

Used by FREDClient.
"""

from datetime import date

from pydantic import BaseModel, Field, ValidationError

from qemy.exceptions import JSONDecodingError


class ObsData(BaseModel):
    """Container for observations data."""
    date: date
    value: float

class Observations(BaseModel):
    """Container for FREDClient observations."""
    count: int
    date_start: date = Field(alias='observation_start')
    date_end: date = Field(alias='observation_end')
    obs_data: list[ObsData] = Field(alias='observations')
    sort_order: str
    units: str

    def __len__(self) -> int:
        return len(self.obs_data)

def decode_observations_json(json_str: str) -> Observations:
    """Decode observations JSON text into pydantic based container."""
    try:
        return Observations.model_validate_json(json_str)
    except ValidationError as e:
        raise JSONDecodingError('Error validating observations JSON') from e

