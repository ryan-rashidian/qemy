"""Dataclasses representing intermediate structures for SEC filing data."""

from dataclasses import dataclass

import pandas as pd

@dataclass
class Concept:
    tag: str
    label: str
    description: str
    unit: str
    filings: list[dict]

    def to_dataframe(self): # Placeholder/Reminder
        return pd.DataFrame(self.filings)

@dataclass
class CompanyFacts:
    ticker: str
    entity_name: str
    concepts: dict[str, Concept] | None = None

