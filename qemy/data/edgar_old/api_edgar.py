"""Edgar API module.

This module requests company concepts data from local download or SEC servers.
Uses CIK##########.json files from companyfacts.
XBRL taxonomy for concept tags.
"""

import logging

import pandas as pd

from qemy.exceptions import InvalidArgumentError, ParseError

from . import _tag_containers as tags
from ._get_facts import get_facts_bulk, get_facts_request
from ._parse_filing import get_concept as _get_concept

logger = logging.getLogger(__name__)

class EDGARClient:
    """Client for fetching filing data from SEC EDGAR API."""

    def __init__(self, ticker: str, use_requests: bool=False):
        """Initialize EDGAR API.

        Initialize EDGAR User-Agent and request headers.

        Args:
            ticker (str): Company ticker symbol
            use_requests (bool): Requests from SEC servers. False = no request
        """
        self.ticker = ticker.upper().strip()

        if use_requests:
            self.facts = get_facts_request(self.ticker)
        else:
            self.facts = get_facts_bulk(self.ticker)

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
        # Use Shares Outstanding tags to get filing date and type
        form = None
        filed = None
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            )
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]
        except ParseError as e:
            logger.warning(e)

        # Filing fields
        filing = [
            ('Form', form),
            ('Filed', filed),
        ]

        for _, metrics in tags.filing_tags.items():

            for key, tag_tuple in metrics.items():
                value = None
                try:
                    value_df = _get_concept(
                        facts=self.facts,
                        xbrl_tags=tag_tuple,
                        latest=True
                    )
                    value = value_df['val']

                except ParseError as e:
                    logger.warning(e)

                filing.append((key, value))

        filing_df = pd.DataFrame(filing)
        filing_df.columns = ['Metric:', self.ticker]
        filing_df.set_index('Metric:', inplace=True)

        return filing_df

    def get_balance_sheet(self) -> pd.DataFrame:
        """Fetches Balance Sheet concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Shares Outstanding and filing info
        shares_outstanding = None
        form = None
        filed = None
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            )
            shares_outstanding = shares_df['val'].iloc[-1]
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]

        except ParseError as e:
            logger.warning(e)

        # Balance Sheet fields
        balance_sheet = [
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]

        for key, tag_tuple in tags.balance_sheet.items():
            value = None
            try:
                value_df = _get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                    latest=True
                )
                value = value_df['val']

            except ParseError as e:
                logger.warning(e)

            balance_sheet.append((key, value))

        balance_df = pd.DataFrame(balance_sheet)
        balance_df.columns = ['Metric:', self.ticker]
        balance_df.set_index('Metric:', inplace=True)

        return balance_df

    def get_cashflow_statement(self) -> pd.DataFrame:
        """Fetches Cash Flow Statement concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Shares Outstanding and filing info
        shares_outstanding = None
        form = None
        filed = None
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            )
            shares_outstanding = shares_df['val'].iloc[-1]
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]

        except ParseError as e:
            logger.warning(e)

        # Cash Flow Statement fields
        cashflow_statement = [
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]

        for key, tag_tuple in tags.cash_flow_statement.items():
            value = None
            try:
                value_df = _get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                    latest=True
                )
                value = value_df['val']
            except ParseError as e:
                    logger.warning(e)

            cashflow_statement.append((key, value))

        cashflow_statement_df = pd.DataFrame(cashflow_statement)
        cashflow_statement_df.columns = ['Metric:', self.ticker]
        cashflow_statement_df.set_index('Metric:', inplace=True)

        return cashflow_statement_df

    def get_income_statement(self) -> pd.DataFrame:
        """Fetches Income Statement concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
        """
        # Shares Outstanding and filing info
        shares_outstanding = None
        form = None
        filed = None
        try:
            shares_df = _get_concept(
                facts=self.facts,
                xbrl_tags=tags.tag_shares_outstanding,
                quarters=10
            )
            shares_outstanding = shares_df['val'].iloc[-1]
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]

        except ParseError as e:
            logger.warning(e)

        # Income Statement fields
        income_statement = [
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]

        for key, tag_tuple in tags.income_statement.items():
            value = None
            try:
                value_df = _get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                    latest=True
                )
                value = value_df['val']
            except ParseError as e:
                logger.warning(e)

            income_statement.append((key, value))

        income_statement_df = pd.DataFrame(income_statement)
        income_statement_df.columns = ['Metric:', self.ticker]
        income_statement_df.set_index('Metric:', inplace=True)

        return income_statement_df

    def get_concept(
            self,
            concept: str,
            quarters: int=10
    ) -> pd.DataFrame:
        """Fetches given concept for given ticker.

        Args:
            cli_arg (str): User argument parsed from the CLI
            quarters (int): Number of quarters to fetch

        Returns:
            pd.DataFrame: Quarterly rows with 'val' column for concept
        """

        xbrl_tags = self._map_concept(concept=concept)

        concept_df = _get_concept(
            facts=self.facts,
            xbrl_tags=xbrl_tags,
            quarters=quarters
        )

        return concept_df

