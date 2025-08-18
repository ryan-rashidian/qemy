"""API EDGAR module for Qemy CLI."""

from qemy.data import EDGARClient
from qemy.cli.format import print_df

def cmd_filing(ticker: str):
    ticker = ticker.upper().strip()
    filing = EDGARClient(ticker).get_filing()
    print_df(df=filing, title=f'Latest SEC Filing for: {ticker}')

