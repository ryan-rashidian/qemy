"""Rich panel renders for Qemy CLI."""

from rich.panel import Panel

from qemy.cli.format import colors
from qemy.cli.format.fmt import FormatText, console


def welcome_panel() -> None:
    """Qemy CLI welcome panel."""
    welcome_text = FormatText(
        'Qemy CLI 0.2.0'
    ).justify('center').style(colors.panel_text).get_text()

    panel = Panel(
        welcome_text,
        title = 'Welcome.',
        subtitle = "Type 'help' or '?' for info",
        border_style = colors.panel_border,
        padding = 3
    )

    console.print(panel)

def info_panel(txt: str, title: str) -> None:
    """Qemy CLI info panel.

    Args:
        txt (str): Body of the panel
        title (str): Title of the panel
    """
    txt_fmt = FormatText(txt).style('info').get_text()
    title_fmt = FormatText(title).justify('center').style('title').get_text()

    panel = Panel(
        txt_fmt,
        title = title_fmt,
        border_style = colors.panel_border,
        padding = 3
    )

    console.print(panel)

