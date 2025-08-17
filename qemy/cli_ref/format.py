"""Qemy CLI output formatting and styling.

Using Rich Python library:
- https://github.com/Textualize/rich
"""

import pandas as pd

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def print_df(df: pd.DataFrame, title: str):
    table = Table(
        title=title,
        border_style='cyan',
        row_styles=['dim', ''],
        box=box.ROUNDED
    )
    
    for col in df:
        if col == 'Metric':
            table.add_column(
                col,
                style='plum1',
                header_style='bold plum1'
            )
        elif col == 'Value':
            table.add_column(
                col,
                style='green',
                header_style='bold green'
            )
        else:
            table.add_column(
                col,
                style='magenta',
                header_style='bold magenta'
            )

    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row.values])

    console.print(table)
    
