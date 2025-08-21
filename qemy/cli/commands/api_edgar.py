"""API EDGAR module for Qemy CLI."""

from rich.progress import Progress, SpinnerColumn, TextColumn

from qemy.cli import colors
from qemy.cli.format import print_df
from qemy.cli.menus import confirm_menu
from qemy.data import EDGARClient
from qemy.data import bulk_refresh as _bulk_refresh


def cmd_filing(ticker: str):
    ticker = ticker.upper().strip()
    filing = EDGARClient(ticker).get_filing()
    print_df(df=filing, title=f'Latest SEC Filing for: {ticker}')

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

