"""Panel renderable module for Qemy CLI.

Using Rich library.
"""

from rich.panel import Panel
from rich.text import Text

from qemy.cli.format import console
from qemy.cli import colors


def style_panel_text(message: str):
    text = Text(message, justify='center')
    text.stylize(colors.panel_text)
    return text

def welcome_panel():
    panel = Panel(
        style_panel_text("Qemy CLI 0.1.1"),
        title="Welcome.",
        subtitle=f"Type 'help' or '?' for info",
        border_style=colors.panel_border
    )
    console.print(panel)

