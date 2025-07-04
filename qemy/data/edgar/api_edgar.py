"""Edgar API module.

This module requests company concepts data from local download or SEC servers.
Uses CIK##########.json files from companyfacts.
XBRL taxonomy for concept tags.
"""

import logging
import pandas as pd

from . import _tag_containers as tags
from ._parse_filing import get_concept
from ._get_facts import get_facts_bulk, get_facts_request

logger = logging.getLogger(__name__)

class EDGARClient:
    """Client for fetching filing data from SEC EDGAR API."""

    def __init__(self, ticker: str, use_requests: bool=False):
        """Initialize EDGAR API. 

        Initialize EDGAR User-Agent and request headers.
        
        Args:
            ticker (str): Company ticker symbol
            use_requests (bool): Requests from SEC servers. False = no request.
        """
        self.ticker = ticker.upper().strip()
        self.facts = None

        try:
            if use_requests:
                self.facts = get_facts_request(self.ticker)
            else:
                self.facts = get_facts_bulk(self.ticker)

            if self.facts is None:
                logger.error(f"Facts not found: {self.ticker}")

        except Exception as e:
            logger.exception(f"Exception:\n{e}")

    def __repr__(self):
        status = "Initialized" if self.facts else "Failed"
        return f"<EDGARClient ticker={self.ticker} [{status}]>"

    def __bool__(self):
        return self.facts is not None

    def _map_concept(self, concept: str) -> tuple[str]:
        """Map concept argument to matching container.

        Args:
            concept (str): User argument parsed from the CLI

        Returns:
            tuple[str]: Matching concept tag container 
        """
        try:
            section, label = tags.map_arg[concept.lower()]
            return tags.filing_tags[section][label]
        except KeyError:
            raise ValueError(f"Unknown concept argument: {concept}")

    def get_filing(self) -> pd.DataFrame | None:
        """Fetch all available concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
            None: If class fails to initialize filing data
        """
        if self.facts is None:
            logger.warning(f"EDGARClient({self.ticker}) - failed to init")
            return None

        # Use Shares Outstanding tags to get filing date and type
        shares_df = get_concept(
            facts=self.facts,
            xbrl_tags=tags.tag_shares_outstanding,
            quarters=10
        )
        if isinstance(shares_df, pd.DataFrame):
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]
        else:
            logger.warning("get_concept() filing info not found")
            form = None
            filed = None

        # Filing fields
        filing = [
            ('Form', form),
            ('Filed', filed),
        ]

        for _, metrics in tags.filing_tags.items():
            for key, tag_tuple in metrics.items():
                value = get_concept(
                    facts=self.facts,
                    xbrl_tags=tag_tuple,
                    latest=True
                )
                if isinstance(value, float):
                    filing.append((key, value))
                else:
                    filing.append((key, value))
                    logger.warning(f"get_concept() failed for: {key}")

        filing_df = pd.DataFrame(
            filing, 
            columns=['Metric:', self.ticker]
        )
        filing_df.set_index('Metric:', inplace=True)

        return filing_df
        
    def get_balance_sheet(self) -> pd.DataFrame | None:
        """Fetches Balance Sheet concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
            None: If class fails to initialize filing data
        """
        if self.facts is None:
            logger.warning(f"EDGARClient({self.ticker}) - failed to init")
            return None

        # Shares Outstanding and filing info
        shares_df = get_concept(
            facts=self.facts,
            xbrl_tags=tags.tag_shares_outstanding,
            quarters=10
        )
        if isinstance(shares_df, pd.DataFrame):
            shares_outstanding = shares_df['val'].iloc[-1]
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]
        else:
            logger.warning("get_concept() filing info not found")
            shares_outstanding = None
            form = None
            filed = None

        # Balance Sheet fields
        balance_sheet = [
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]

        for key, tag_tuple in tags.balance_sheet.items():
            value = get_concept(
                facts=self.facts,
                xbrl_tags=tag_tuple,
                latest=True
            )
            if isinstance(value, float):
                balance_sheet.append((key, value))
            else:
                balance_sheet.append((key, value))
                logger.warning(f"get_concept() failed for: {key}")

        balance_df = pd.DataFrame(
            balance_sheet, 
            columns=['Metric:', self.ticker]
        )
        balance_df.set_index('Metric:', inplace=True)

        return balance_df

    def get_cashflow_statement(self) -> pd.DataFrame | None:
        """Fetches Cash Flow Statement concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
            None: If class fails to initialize filing data
        """
        if self.facts is None:
            logger.warning(f"EDGARClient({self.ticker}) - failed to init")
            return None

        # Shares Outstanding and filing info
        shares_df = get_concept(
            facts=self.facts,
            xbrl_tags=tags.tag_shares_outstanding,
            quarters=10
        )
        if isinstance(shares_df, pd.DataFrame):
            shares_outstanding = shares_df['val'].iloc[-1]
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]
        else:
            logger.warning("get_concept() filing info not found")
            shares_outstanding = None
            form = None
            filed = None

        # Cash Flow Statement fields
        cashflow_statement = [
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]

        for key, tag_tuple in tags.cash_flow_statement.items():
            value = get_concept(
                facts=self.facts,
                xbrl_tags=tag_tuple,
                latest=True
            )
            if isinstance(value, float):
                cashflow_statement.append((key, value))
            else:
                cashflow_statement.append((key, value))
                logger.warning(f"get_concept() failed for: {key}")

        cashflow_statement_df = pd.DataFrame(
            cashflow_statement, 
            columns=['Metric:', self.ticker]
        )
        cashflow_statement_df.set_index('Metric:', inplace=True)

        return cashflow_statement_df

    def get_income_statement(self) -> pd.DataFrame | None:
        """Fetches Income Statement concepts for given ticker.

        Returns:
            pd.DataFrame: with concepts split into rows
            None: If class fails to initialize filing data
        """
        if self.facts is None:
            logger.warning(f"EDGARClient({self.ticker}) - failed to init")
            return None

        # Shares Outstanding and filing info
        shares_df = get_concept(
            facts=self.facts,
            xbrl_tags=tags.tag_shares_outstanding,
            quarters=10
        )
        if isinstance(shares_df, pd.DataFrame):
            shares_outstanding = shares_df['val'].iloc[-1]
            filed = shares_df['form'].iloc[-1]
            form = shares_df['filed'].iloc[-1]
        else:
            logger.warning("get_concept() filing info not found")
            shares_outstanding = None
            form = None
            filed = None

        # Income Statement fields
        income_statement = [
            ('Form', form),
            ('Filed', filed),
            ('Shares Outstanding', shares_outstanding)
        ]

        for key, tag_tuple in tags.income_statement.items():
            value = get_concept(
                facts=self.facts,
                xbrl_tags=tag_tuple,
                latest=True
            )
            if isinstance(value, float):
                income_statement.append((key, value))
            else:
                income_statement.append((key, value))
                logger.warning(f"get_concept() failed for: {key}")

        income_statement_df = pd.DataFrame(
            income_statement, 
            columns=['Metric:', self.ticker]
        )
        income_statement_df.set_index('Metric:', inplace=True)

        return income_statement_df

    def get_concept(
            self, 
            concept: str, 
            quarters: int=10
    ) -> pd.DataFrame | None:
        """Fetches given concept for given ticker.

        Args:
            cli_arg (str): User argument parsed from the CLI
            quarters (int): Number of quarters to fetch

        Returns:
            pd.DataFrame: Quarterly rows with 'val' column for concept
            None: If class fails to initialize filing data
        """
        if self.facts is None:
            logger.warning(f"EDGARClient({self.ticker}) - failed to init")
            return None

        xbrl_tags = self._map_concept(concept=concept)
        
        concept_df = get_concept(
            facts=self.facts,
            xbrl_tags=xbrl_tags,
            quarters=quarters
        )        

        if isinstance(concept_df, pd.DataFrame):
            return concept_df
        else:
            logger.error(f"Error: get_concept({concept}) failed\n{xbrl_tags}")
            return None

