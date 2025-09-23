"""Rich panel renders for Qemy CLI."""

from rich.panel import Panel
from rich.markdown import Markdown

from qemy.cli.format import colors
from qemy.cli.format.fmt import FormatText, console


def info_panel(txt: str, title: str) -> None:
    """Qemy CLI info panel."""
    txt_fmt = FormatText(txt).style('info').get_text()
    title_fmt = FormatText(title).justify('center').style('title').get_text()

    panel = Panel(
        txt_fmt,
        title = title_fmt,
        border_style = colors.panel_border,
        padding = 1
    )

    console.print(panel)

def title_panel(txt: str, title: str) -> None:
    """Qemy CLI title panel."""
    txt_fmt = FormatText(txt).justify('center').style('title').get_text()
    title_fmt = FormatText(title).justify('center').style('title').get_text()

    panel = Panel(
        txt_fmt,
        title = title_fmt,
        border_style = colors.panel_border,
        padding = 1
    )

    console.print(panel)

def markdown_panel(txt: str, title: str) -> None:
    """Qemy CLI markdown panel."""
    md_txt = Markdown(txt)
    title_fmt = FormatText(title).justify('center').style('title').get_text()
    panel = Panel(
        md_txt,
        title = title_fmt,
        border_style = colors.panel_border,
        padding = 1
    )

    console.print(panel, style='info')

def result_panel(txt: str, title: str) -> None:
    """Qemy CLI result panel."""
    txt_fmt = FormatText(txt).justify('center').style('data').get_text()
    title_fmt = FormatText(title).justify('center').style('title').get_text()

    panel = Panel(
        txt_fmt,
        title = title_fmt,
        border_style = colors.panel_border,
        padding = 1
    )

    console.print(panel)

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

