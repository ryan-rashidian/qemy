"""Qemy CLI output formatting and styling.

Using Rich Python library:
- https://github.com/Textualize/rich
"""

import pandas as pd

from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme
from rich import box

custom_themes = Theme({
    'info': 'magenta',
    'data': 'green',
    'warning': 'bold red underline',
})

console = Console(theme=custom_themes)

def print_theme(message: str, theme: str):
    txt = Text(message, style=theme)
    console.print(txt)

def print_markdown(md_text: str, theme: str):
    console.print(Markdown(md_text), style=theme)

def style_text(message: str, color: str):
    text = Text(message, justify='center')
    text.stylize(color)
    return text

def print_prompt():
    console.print('>>> ', style='info', end='')
    
def print_menu():
    return None

def print_panel():
    panel = Panel(
        style_text("Qemy CLI 0.1.1", color='bold magenta'),
        title="Welcome.",
        subtitle=f"Type 'help' or '?' for info",
        border_style="magenta"
    )
    console.print(panel)

def print_df(df: pd.DataFrame, title: str):
    table = Table(
        title=style_text(title, color='bold magenta underline'),
        border_style='magenta',
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
    
