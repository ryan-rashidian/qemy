"""API EDGAR module for Qemy CLI."""

import pandas as pd

from rich.progress import Progress, SpinnerColumn, TextColumn

from qemy.cli import colors
from qemy.cli.format import console, format_df
from qemy.cli.menus import confirm_menu
from qemy.data import EDGARClient, SECFiles
from qemy.data import bulk_refresh as _bulk_refresh


def cmd_filing(ticker: str):
    ticker = ticker.upper().strip()
    filing: pd.DataFrame = EDGARClient(ticker).get_filing()
    filing_fmt = format_df(df=filing, title=f'Latest SEC Filing for: {ticker}')
    console.print(filing_fmt)

def cmd_concept(ticker: str, concept: str = 'assets', quarters: int=4):
    ticker = ticker.upper().strip()
    files: SECFiles = EDGARClient(ticker).get_concept(
        concept = concept,
        quarters = quarters
    )

def cmd_bulk_refresh() -> None:
    """Download SEC bulk data from within Qemy CLI."""
    if not confirm_menu():
        return

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}')
    ) as progress:
        task = progress.add_task(
            f'[{colors.load_spinner}]Downloading SEC bulk data...',
            total=None
        )
        _bulk_refresh()
        progress.update(
            task,
            description=f'[{colors.load_spinner}]Download complete.'
        )

