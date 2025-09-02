"""Qemy CLI output formatting and styling.

Using Rich Python library:
- https://github.com/Textualize/rich
"""

from typing import Literal

import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from qemy.cli.fmt import colors

custom_themes = Theme({
    'info': colors.info,
    'data': colors.data,
    'warning': colors.warning,
    'title': colors.title,
})

console = Console(theme=custom_themes)

Justify = Literal['default', 'center', 'full', 'left', 'right']

def format_text(
    message: str,
    theme: str,
    pos: Justify = 'default'
) -> Text:
    """Format string into formatted rich Text object.

    Args:
        message (str): Raw string
        theme (str): Custom theme name
        pos (Justify): Justify constant

    Returns:
        Text: Formatted rich Text object
    """
    txt = Text(message, justify=pos)
    txt.stylize(theme)
    return txt

def format_df(df: pd.DataFrame, title: str) -> Table:
    """Format pandas.DataFrame into formatted rich Table object.

    Args:
        df (pd.DataFrame): Raw DataFrame
        title (str): Title string for Table

    Returns:
        Table: Formatted rich Table object
    """
    title_fmt = Text(title, justify='center')
    title_fmt.stylize(colors.df_title)
    df = df.map(lambda x: f'{x:,.2f}' if isinstance(x, float) else x)

    table = Table(
        title = title_fmt,
        border_style = colors.df_border,
        row_styles = colors.row_style,
        box = box.ROUNDED,
        expand = True
    )

    for col in df:
        if col == 'Metric':
            table.add_column(
                Text(col, justify='center'),
                style=colors.metric_col,
                header_style=colors.metric_col_header,
                justify='left'
            )
        elif col in ('Value', 'val'):
            table.add_column(
                Text(col, justify='center'),
                style=colors.value_col,
                header_style=colors.value_col_header,
                justify='right'
            )
        else:
            table.add_column(
                Text(col, justify='center'),
                style=colors.default_col,
                header_style=colors.default_col_header
            )

    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row.values])

    return table

