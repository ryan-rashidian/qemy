"""Commands for EDGARClient in Qemy CLI."""

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from qemy.cli.commands.help import help_text
from qemy.cli.format.colors import colors
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


def _f_concept(client: EDGARClient) -> None:
    """CLI Filings: Concept search."""
    ticker_fmt = client.companyfacts.ticker.upper()
    info_description = (
        'Enter a valid concept and and number of quarters to fetch\n'
        "For a list of valid concepts, enter `help` or `?`\n\n"
        f'Usage: ({ticker_fmt}) (CONCEPTS) >>> <CONCEPT> <#QUARTERS>'
    )
    info_title = 'Concept Search.'
    info_panel(txt=info_description, title=info_title)
    concept, quarters = input(f'({ticker_fmt}) (CONCEPTS) ').split()

    try:
        client.fetch_concept(concept)
        concept_data = client.companyfacts.concepts.get(concept, Concept())
    except ClientParsingError:
        FormatText(f'{concept} not found.\n').style('warning').print()
        return

    description = concept_data.description
    label = concept_data.label
    unit = concept_data.unit
    company = client.companyfacts.name
    ticker_fmt = client.companyfacts.ticker
    title = f'{company} ({ticker_fmt}): {label} ({unit})'

    quarters_int = int(quarters)
    concept_df = concept_data.to_dataframe().tail(quarters_int)
    concept_df.drop(columns=['fy', 'frame', 'end', 'accn'], inplace=True)

    info_panel(txt=description, title=title)
    FormatDF(concept_df, f'{concept}').print()

def _f_balance_sheet(client: EDGARClient) -> None:
    """CLI Filings: Balance Sheet"""
    description = 'Balance Sheet'
    company_name = client.companyfacts.name
    ticker_fmt = client.companyfacts.ticker
    title = f'{company_name} ({ticker_fmt})'

    balance_sheet_df = client.get_balance_sheet_df()

    title_panel(txt=description, title=title)
    FormatDF(balance_sheet_df, description).print()

def _f_cashflow_statement(client: EDGARClient) -> None:
    """CLI Filings: Cash Flow Statement"""
    description = 'Cash Flow Statement'
    company_name = client.companyfacts.name
    ticker_fmt = client.companyfacts.ticker
    title = f'{company_name} ({ticker_fmt})'

    balance_sheet_df = client.get_cashflow_statement_df()

    title_panel(txt=description, title=title)
    FormatDF(balance_sheet_df, description).print()

def _f_income_statement(client: EDGARClient) -> None:
    """CLI Filings: Income Statement"""
    description = 'Income Statement'
    company_name = client.companyfacts.name
    ticker_fmt = client.companyfacts.ticker
    title = f'{company_name} ({ticker_fmt})'

    balance_sheet_df = client.get_income_statement_df()

    title_panel(txt=description, title=title)
    FormatDF(balance_sheet_df, description).print()

@help_text("""\nCategory: [EDGAR]
Description: Fetch SEC 10K/10Q filing data.

Usage: >>> f <TICKER>
""")
def cmd_f(ticker: str) -> None:
    """CLI command for SEC filings."""
    client = EDGARClient(ticker)

    menu_description = 'SEC 10K/10Q filings.'
    company_name = client.companyfacts.name
    ticker_fmt = client.companyfacts.ticker.upper()
    menu_title = f'{company_name} ({ticker_fmt})'
    choices = (
        '1. Concepts\n'
        '2. Balance Sheet\n'
        '3. Cash Flow Statment\n'
        '4. Income Statement\n'
        '5. Back'
    )
    info_title = 'Options:'

    title_panel(txt=menu_description, title=menu_title)
    while True:
        info_panel(txt=choices, title=info_title)
        choice = input(f'({ticker_fmt}) ').strip()
        if choice == '1':
            _f_concept(client)
        elif choice == '2':
            _f_balance_sheet(client)
        elif choice == '3':
            _f_cashflow_statement(client)
        elif choice == '4':
            _f_income_statement(client)
        elif choice == '5':
            break

@help_text("""\nCategory: [EDGAR]
Description: Download SEC bulk filing data for use within Qemy CLI.
- Overwrites previous downloads
- Files are downloaded into the root directory of Qemy
    <QEMY_ROOT>/bulk_data/
- Required space: 20GB
- Filing data is refreshed by the SEC daily

Usage: >>> fsync
       Are you sure? (y/n): y
""")
def cmd_fsync() -> None:
    """Download SEC bulk data from within Qemy CLI."""
    if not confirm_menu():
        return

    color = colors['misc']['load_spinner']
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        BarColumn()
    ) as progress:
        task = progress.add_task(
            f'[{color}]Downloading SEC bulk data...[/{colors}]',
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

