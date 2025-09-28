"""Qemy CLI output formatting and styling.

Using Rich Python library:
- https://github.com/Textualize/rich
"""

from typing import Literal, Self

from numpy import isinf
import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from qemy.cli.format import colors

custom_themes = Theme({
    'info': colors.theme_info,
    'data': colors.theme_data,
    'warning': colors.theme_warning,
    'title': colors.theme_title
})

console = Console(theme=custom_themes)

class FormatText:
    """Format strings of text with Rich."""

    Justify = Literal['default', 'center', 'full', 'left', 'right']

    def __init__(self, text_str: str):
        """Initialize text string."""
        self.text = Text(text_str)

    def justify(self, pos: Justify) -> Self:
        """Justify text position."""
        self.text.justify = pos
        return self

    def style(self, theme: str) -> Self:
        """Stylize text string with theme."""
        self.text.stylize(theme)
        return self

    def get_text(self) -> Text:
        """Get formatted Rich Text Object."""
        return self.text

    def print(self) -> None:
        """Print text string to terminal."""
        console.print(self.text, end='')

class FormatDF:
    """Format pandas DataFrame with Rich."""

    def __init__(self, df: pd.DataFrame, title: str):
        """Initialize formatter.

        Args:
            df (pd.DataFrame): target DataFrame
            title (str): title string for formatted Table
        """
        self.df = df.map(
            lambda x: (
                f'{x:,.2f}' if isinstance(x, float) 
                else f'{x:,d}' if isinstance(x, int)
                else x
            )
        )

        formatter = FormatText(title).justify('center')
        title_fmt = formatter.style('title').get_text()
        self.table = Table(
            title = title_fmt,
            border_style = colors.table_border,
            row_styles = colors.table_row_style,
            box = box.ROUNDED,
            expand = True
        )

    def _df_to_table(self) -> None:
        """Format pandas DataFrame into Rich Table object."""
        for col in self.df:

            if col == 'val':
                self.table.add_column(
                    header = Text(col, justify='center'),
                    header_style = colors.table_val_col_header,
                    style = colors.table_val_col,
                    justify = 'right'
                )
            else:
                self.table.add_column(
                    header = Text(col, justify='center'),
                    header_style = colors.table_def_col_header,
                    style = colors.table_val_col,
                    justify = 'left'
                )

        for _, row in self.df.iterrows():
            self.table.add_row(*[str(x) for x in row.values])

    def get_table(self) -> Table:
        """Get formatted Rich Table object."""
        self._df_to_table()
        return self.table

    def print(self) -> None:
        """Print formatted Rich Table to terminal."""
        self._df_to_table()
        console.print(self.table)

