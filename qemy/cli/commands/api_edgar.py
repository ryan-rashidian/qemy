"""API EDGAR module for Qemy CLI."""

import pandas as pd
from rich.progress import Progress, SpinnerColumn, TextColumn

from qemy.cli.fmt import colors
from qemy.cli.fmt.format import console, format_df, format_text
from qemy.cli.fmt.layout import concept_layout
from qemy.cli.fmt.menus import confirm_menu
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
    company = format_text(files.company, theme='info')
    concept_df_fmt = format_df(df=files.data, title=f'{company} SEC Filing')
    description = format_text(files.description, theme='info')
    label = files.label
    unit = files.units
    label_full = format_text(f'{label} ({unit})', theme='info')
    layout = concept_layout(
        company = company,
        data = concept_df_fmt,
        label = label_full,
        description = description
    )
    console.print(layout)

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

