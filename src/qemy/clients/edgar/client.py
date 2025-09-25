"""EDGAR client orchestrator for SEC EDGAR data pipeline.

Handles the process of:
- Fetching data
- Parsing data
- Mapping concepts
- Normalizing data shape
"""

from __future__ import annotations

import pandas as pd

from qemy.clients.edgar import _mappings
from qemy.clients.edgar.fetcher import FactsLoader
from qemy.clients.edgar.parser import ConceptParser
from qemy.clients.edgar.schemas import (
    CompanyFacts, Concept, Facts, ParsedCompanyFacts
)
from qemy.exceptions import ClientParsingError, InvalidArgumentError


class EDGARClient:
    """EDGAR client orchestrator class."""

    def __init__(self, ticker: str):
        """Initialize EDGAR data pipeline for given company.

        Args:
            ticker (str): Company ticker symbol
        """
        raw_companyfacts: CompanyFacts = FactsLoader(ticker).get_companyfacts()
        self.raw_facts: Facts = raw_companyfacts.facts
        self.parser = ConceptParser(self.raw_facts.concepts)
        self.companyfacts = ParsedCompanyFacts(
            ticker = ticker.strip().upper(),
            name = raw_companyfacts.name
        )

    def __repr__(self) -> str:
        return f'EDGARClient({self.companyfacts.ticker})'

    def __str__(self) -> str:
        return f'[EDGAR Client]: {self.companyfacts.ticker}'

    def __bool__(self) -> bool:
        return bool(self.raw_facts)

    def __len__(self) -> int:
        return len(self.companyfacts.concepts)

    def _get_mappings(self, concept: str) -> tuple[str]:
        """Get matching tuple for concept mapping.

        Args:
            concept (str): Key for matching concept tuple

        Returns:
            tuple[str]: Matching concept mapper

        Raises:
            InvalidArgumentError: If undefined concept key is given
        """
        try:
            section, label = _mappings.map_arg[concept.lower()]
            return _mappings.filing_tags[section][label]

        except KeyError as e:
            raise InvalidArgumentError(f'{concept} is undefined') from e

    def get_concept(self, concept: str) -> EDGARClient:
        """Fetches parsed filing data for given concept.

        Args:
            concept (str): Key for matching concept tuple
        """
        if concept not in self.companyfacts.concepts:
            xbrl_mappings = self._get_mappings(concept)
            parsed_data: Concept = self.parser.parse(xbrl_mappings)
            self.companyfacts.concepts[concept] = parsed_data

        return self

    def fill_concepts(self) -> EDGARClient:
        """Fetch and parse all filing data."""
        for concept in _mappings.map_arg.keys():
            if concept not in self.companyfacts.concepts:
                try:
                    xbrl_mappings = self._get_mappings(concept)
                    parsed_data: Concept = self.parser.parse(xbrl_mappings)
                    self.companyfacts.concepts[concept] = parsed_data

                except ClientParsingError:
                    self.companyfacts.concepts[concept] = Concept()

        return self

    def _get_latest_statement(self, section: str) -> list[tuple]:
        """Build a statement from parsed concepts"""
        statement = []
        filed, form = None, None

        for concept, xbrl_mappings in _mappings.filing_tags[section].items():
            try:
                parsed_data: Concept = self.parser.parse(xbrl_mappings)
                latest_filing: dict = parsed_data.filings[-1]
                value = latest_filing.get('val')
                form = latest_filing.get('form')
                filed = latest_filing.get('filed')
                statement.append((concept, value))

            except ClientParsingError:
                statement.append((concept, None))

        statement.append(('Filed', filed))
        statement.append(('Form', form))

        return statement

    def get_balance_sheet_df(self) -> pd.DataFrame:
        """Fetch pandas DataFrame of latest balance sheet."""
        balance_sheet = self._get_latest_statement('Balance Sheet')
        balance_sheet_df = pd.DataFrame(balance_sheet)
        balance_sheet_df.columns = ['Metric', 'val']

        return balance_sheet_df

    def get_cashflow_statement_df(self) -> pd.DataFrame:
        """Fetch pandas DataFrame of lastest cashflow statement."""
        cashflow_statement = self._get_latest_statement('Cash Flow Statement')
        cashflow_statement_df = pd.DataFrame(cashflow_statement)
        cashflow_statement_df.columns = ['Metric', 'val']

        return cashflow_statement_df

    def get_income_statement_df(self) -> pd.DataFrame:
        """Fetch pandas DataFrame of lastest income stament."""
        income_statement = self._get_latest_statement('Income Statement')
        income_statement_df = pd.DataFrame(income_statement)
        income_statement_df.columns = ['Metric', 'val']

        return income_statement_df

