"""Commands for EDGARClient in Qemy CLI."""

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from qemy.cli.format.fmt import FormatDF, FormatText
from qemy.cli.format import colors
from qemy.cli.menus import confirm_menu
from qemy.clients import EDGARClient
from qemy.clients.edgar import (
    delete_bulk_data,
    download_cik_mapping,
    download_companyfacts_zip,
    unzip_companyfacts,
)
from qemy.exceptions import ClientParsingError


def cmd_f(ticker: str) -> None:
    """Print a summary of the latest filing for a given ticker."""
    client = EDGARClient(ticker)
    balance_sheet_df = client.get_balance_sheet_df()
    cashflow_statement_df = client.get_cashflow_statement_df()
    income_statement_df = client.get_income_statement_df()
    FormatDF(balance_sheet_df, 'Balance Sheet').print()
    FormatDF(cashflow_statement_df, 'Cash Flow Statement').print()
    FormatDF(income_statement_df, 'Income Statement').print()

# REMINDER: This is an unfinished placeholder
def cmd_fc(ticker: str, concept: str) -> None:
    """Print historical filing data for given ticker, concept to terminal."""
    try:
        client = EDGARClient(ticker).get_concept(concept)
        client.companyfacts.concepts.get(concept)
    except ClientParsingError:
        FormatText(f'{concept} not found.').style('warning').print()
        return

def cmd_fsync() -> None:
    """Download SEC bulk data from within Qemy CLI."""
    if not confirm_menu():
        return

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        BarColumn()
    ) as progress:
        task = progress.add_task(
            f'{colors.load_spinner}[Downloading SEC bulk data...]',
            total = 4
        )

        delete_bulk_data()
        progress.advance(task)
        download_cik_mapping()
        progress.advance(task)
        download_companyfacts_zip()
        progress.advance(task)
        unzip_companyfacts()
        progress.advance(task)

