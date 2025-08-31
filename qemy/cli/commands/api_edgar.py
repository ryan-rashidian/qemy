"""API EDGAR module for Qemy CLI."""

import pandas as pd
from rich.progress import Progress, SpinnerColumn, TextColumn

from qemy.cli.fmt import colors
from qemy.cli.fmt.format import console, format_df, format_text
from qemy.cli.fmt.menus import confirm_menu
from qemy.cli.fmt.panels import description_panel
from qemy.data import EDGARClient, SECFiles
from qemy.data import bulk_refresh as _bulk_refresh


def cmd_filing(ticker: str) -> None:
    """"""
    ticker = ticker.upper().strip()
    filing: pd.DataFrame = EDGARClient(ticker).get_filing()
    filing_fmt = format_df(df=filing, title=f'Latest SEC Filing for: {ticker}')

    console.print(filing_fmt)

def cmd_concept(
    ticker: str,
    concept: str = 'assets',
    quarters: str | int = 8
) -> None:
    """"""
    ticker = ticker.upper().strip()
    concept = concept.lower().strip()
    quarters = int(quarters)

    files: SECFiles = EDGARClient(ticker).get_concept(
        concept = concept,
        quarters = quarters
    )
    files.data['filed'] = files.data['filed'].dt.date
    files.data['end'] = files.data['end'].dt.date
    label = files.label
    unit = files.units

    company = format_text(files.company, theme='title', pos='center')
    concept_df_fmt = format_df(df=files.data, title=f'{company} Filings')
    description_pnl = description_panel(
        description=files.description,
        label=f'{label}, ({unit})'
    )

    console.print(description_pnl)
    console.print(concept_df_fmt)

def cmd_bulk_refresh() -> None:
    """Download SEC bulk data from within Qemy CLI."""
    if not confirm_menu():
        return

    # wrapped with rich loading spinner
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

