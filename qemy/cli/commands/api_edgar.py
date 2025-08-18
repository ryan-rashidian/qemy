"""API EDGAR module for Qemy CLI."""

from qemy.data import EDGARClient, bulk_refresh
from qemy.cli.format import print_df

cmd_bulk_refresh = bulk_refresh

def cmd_filing(ticker: str):
    ticker = ticker.upper().strip()
    filing = EDGARClient(ticker).get_filing()
    print_df(df=filing, title=f'Latest SEC Filing for: {ticker}')


