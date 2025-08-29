"""Main EDGARClient module."""

import logging

import pandas as pd

from qemy.exceptions import InvalidArgumentError, ParseError

from . import _tag_containers as tags
from ._get_facts import get_facts_bulk, get_facts_request
from .parser import SECFiles
from .parser import get_concept as _get_concept

logger = logging.getLogger(__name__)

class EDGARClient:
    """Client for fetching filing data from SEC EDGAR API."""

    def __init__(self, ticker: str, use_requests: bool=False):
        """Initialize EDGAR API.

        Initialize EDGAR User-Agent and request headers.

        Args:
            ticker (str): Company ticker symbol
            use_requests (bool): True makes a request to SEC servers.
        """
        self.ticker = ticker.upper().strip()

        if use_requests:
            self.facts = get_facts_request(self.ticker)
        else:
            self.facts = get_facts_bulk(self.ticker)

        self.company = self.facts.get('entityName', '')

    def __repr__(self) -> str:
        status = "Initialized" if self.facts else "Failed"
        return f"EDGARClient(ticker={self.ticker}) <[{status}]>"

    def __str__(self) -> str:
        status = "Initialized" if self.facts else "Failed"
        return f"[EDGARClient] ticker={self.ticker} <[{status}]>"

    def __bool__(self) -> bool:
        return self.facts is not None

    def _map_concept(self, concept: str) -> tuple[str]:
        """Map concept argument to matching container.

        Args:
            concept (str): User argument parsed from the CLI

        Returns:
            tuple[str]: Matching concept tag container

        Raises:
            InvalidArgumentError: If unknown concept argument
        """
        try:
            section, label = tags.map_arg[concept.lower()]
            return tags.filing_tags[section][label]
        except KeyError as err:
            raise InvalidArgumentError(
                f"Unknown concept argument: {concept}"
            ) from err

    def get_filing(self) -> pd.DataFrame:
        """Fetch all available concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Use Shares Outstanding tags to get reliable meta-data
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=4
            ).data
            filed = shares_df['filed'].iloc[-1]
            form = shares_df['form'].iloc[-1]
        except ParseError:
            filed = None
            form = None

        filing = [
            ('Company', self.company),
            ('Form', form),
            ('Filed', filed),
        ]
        # Filing fields
        for _, metrics in tags.filing_tags.items():
            for key, tag_tuple in metrics.items():
                try:
                    value_df = _get_concept(
                        facts=self.facts,
                        xbrl_tags=tag_tuple,
                        quarters=4
                    ).data
                    value = value_df['val'].iloc[-1]
                except ParseError:
                    value = None
                filing.append((key, value))

        filing_df = pd.DataFrame(filing)
        filing_df.columns = ['Metric', 'Value']
        return filing_df

    def get_balance_sheet(self) -> pd.DataFrame:
        """Fetches Balance Sheet concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Shares Outstanding and filing info
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            ).data
            filed = shares_df['filed'].iloc[-1]
            form = shares_df['form'].iloc[-1]
            shares_outstanding = shares_df['val'].iloc[-1]
        except ParseError:
            filed = None
            form = None
            shares_outstanding = None

        balance_sheet = [
            ('Company', self.company),
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]
        # Balance Sheet fields
        for key, tag_tuple in tags.balance_sheet.items():
            try:
                value_df = _get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                ).data
                value = value_df['val'].iloc[-1]
            except ParseError:
                value = None
            balance_sheet.append((key, value))

        balance_df = pd.DataFrame(balance_sheet)
        balance_df.columns = ['Metric', 'Value']
        return balance_df

    def get_cashflow_statement(self) -> pd.DataFrame:
        """Fetches Cash Flow Statement concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Shares Outstanding and filing info
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            ).data
            filed = shares_df['filed'].iloc[-1]
            form = shares_df['form'].iloc[-1]
            shares_outstanding = shares_df['val'].iloc[-1]
        except ParseError:
            filed = None
            form = None
            shares_outstanding = None

        cashflow_statement = [
            ('Company', self.company),
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]
        # Cash Flow Statement fields
        for key, tag_tuple in tags.cash_flow_statement.items():
            try:
                value_df = _get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                ).data
                value = value_df['val'].iloc[-1]
            except ParseError:
                value = None
            cashflow_statement.append((key, value))

        cashflow_statement_df = pd.DataFrame(cashflow_statement)
        cashflow_statement_df.columns = ['Metric', 'Value']
        return cashflow_statement_df

    def get_income_statement(self) -> pd.DataFrame:
        """Fetches Income Statement concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Shares Outstanding and filing info
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            ).data
            filed = shares_df['filed'].iloc[-1]
            form = shares_df['form'].iloc[-1]
            shares_outstanding = shares_df['val'].iloc[-1]
        except ParseError:
            filed = None
            form = None
            shares_outstanding = None

        income_statement = [
            ('Company', self.company),
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]
        # Income Statement fields
        for key, tag_tuple in tags.income_statement.items():
            try:
                value_df = _get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                ).data
                value = value_df['val'].iloc[-1]
            except ParseError:
                value = None
                income_statement.append((key, value))

        income_statement_df = pd.DataFrame(income_statement)
        income_statement_df.columns = ['Metric', 'Value']
        return income_statement_df

    def get_concept(
        self,
        concept: str,
        quarters: int=10
    ) -> SECFiles:
        """Fetches given concept for given ticker.

        Args:
            cli_arg (str): User argument parsed from the CLI
            quarters (int): Number of quarters to fetch

        Returns:
            DataFrame: with concept data
        """
        xbrl_tags = self._map_concept(concept=concept)
        return _get_concept(
            facts=self.facts,
            xbrl_tags=xbrl_tags,
            quarters=quarters
        )

