"""Commands for EDGARClient in Qemy CLI."""

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from qemy.cli.format import colors
from qemy.cli.format.fmt import FormatDF, FormatText
from qemy.cli.format.panels import info_panel, title_panel
from qemy.cli.menus import confirm_menu
from qemy.clients import EDGARClient
from qemy.clients.edgar import (
    delete_bulk_data,
    download_cik_mapping,
    download_companyfacts_zip,
    unzip_companyfacts,
)
from qemy.clients.edgar.schemas import Concept
from qemy.exceptions import ClientParsingError


def cmd_f(ticker: str) -> None:
    """Print a summary of the latest filing for a given ticker."""
    client = EDGARClient(ticker)

    description = 'Latest Filings Summary'
    company = client.companyfacts.entity_name
    ticker_fmt = client.companyfacts.ticker
    title = f'{company} ({ticker_fmt})'

    balance_sheet_df = client.get_balance_sheet_df()
    cashflow_statement_df = client.get_cashflow_statement_df()
    income_statement_df = client.get_income_statement_df()

    title_panel(txt=description, title=title)
    FormatDF(balance_sheet_df, 'Balance Sheet').print()
    FormatDF(cashflow_statement_df, 'Cash Flow Statement').print()
    FormatDF(income_statement_df, 'Income Statement').print()

def cmd_fc(ticker: str, concept: str, quarters: str='8') -> None:
    """Print historical filing data for given ticker, concept to terminal."""
    quarters_int = int(quarters)
    try:
        client = EDGARClient(ticker).get_concept(concept)
        concept_data = client.companyfacts.concepts.get(concept, Concept())
        if not concept_data.filings:
            FormatText(f'No data for: {concept}\n').style('warning').print()

        description = concept_data.description
        label = concept_data.label
        unit = concept_data.unit
        company = client.companyfacts.entity_name
        ticker_fmt = client.companyfacts.ticker
        title = f'{company} ({ticker_fmt}): {label} ({unit})'

        concept_df = concept_data.to_dataframe().tail(quarters_int)
        concept_df.drop(columns=['fy', 'frame', 'end', 'accn'], inplace=True)

        info_panel(txt=description, title=title)
        FormatDF(concept_df, f'{concept}').print()

    except ClientParsingError:
        FormatText(f'{concept} not found.\n').style('warning').print()
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

