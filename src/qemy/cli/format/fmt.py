"""Qemy CLI output formatting and styling.

Using Rich Python library:
- https://github.com/Textualize/rich
"""

from __future__ import annotations

from typing import Literal

import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from qemy.cli.format import colors

custom_themes = Theme({
    'info': colors.info,
    'data': colors.data,
    'warning': colors.warning,
    'title': colors.title
})

console = Console(theme=custom_themes)

class FormatText:
    """Format strings of text with Rich."""

    Justify = Literal['default', 'center', 'full', 'left', 'right']

    def __init__(self, text_str: str):
        """Initialize text string."""
        self.text = Text(text_str)

    def justify(self, pos: Justify) -> FormatText:
        """Justify text position."""
        self.text.justify = pos
        return self

    def style(self, theme: str) -> FormatText:
        """Stylize text string with theme."""
        self.text.stylize(theme)
        return self

    def print(self) -> None:
        """Print text string to terminal."""
        console.print(self.text, end='')

class FormatDF:
    """Format pandas DataFrame with Rich."""

    def __init__(self, df: pd.DataFrame, title: str):
        """Initialize pandas DataFrame."""
        self.df = df.map(lambda x: f'{x:,.2f}' if isinstance(x, float) else x)
        self.table = Table(
            title = title,
            title_justify = 'center',
            title_style = 'title',
            border_style = colors.df_border,
            row_styles = colors.row_style,
            box = box.ROUNDED,
            expand = True
        )

    def _df_to_table(self) -> None:
        """Format pandas DataFrame into Rich Table object."""
        for col in self.df:

            if col == 'val':
                self.table.add_column(
                    header = Text(col, justify='center'),
                    header_style = colors.value_col_header,
                    style = colors.value_col,
                    justify = 'right'
                )
            else:
                self.table.add_column(
                    header = Text(col, justify='center'),
                    header_style = colors.default_col_header,
                    style = colors.default_col,
                    justify = 'left'
                )

        for _, row in self.df.iterrows():
            self.table.add_row(*[str(x) for x in row.values])

    def print(self) -> None:
        """Print formatted Rich Table to terminal."""
        self._df_to_table()
        console.print(self.table)

