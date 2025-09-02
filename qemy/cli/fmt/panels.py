"""Panel renderable module for Qemy CLI."""

from rich.panel import Panel
from rich.text import Text

from qemy.cli.fmt import colors
from qemy.cli.fmt.format import console, format_text


def welcome_panel():
    """Qemy CLI welcome panel."""
    welcome_txt = Text('Qemy CLI 0.1.1', justify='center')
    welcome_txt.stylize(colors.panel_text)
    panel = Panel(
        welcome_txt,
        title='Welcome.',
        subtitle="Type 'help' or '?' for info",
        border_style=colors.panel_border
    )
    console.print(panel)

def description_panel(description: str, label: str) -> Panel:
    """Qemy CLI description panel."""
    description_fmt = format_text(description, theme='info')
    label_fmt = format_text(label, theme='title', pos='center')
    panel = Panel(
        description_fmt,
        title = label_fmt,
        border_style = colors.panel_border,
        padding = 3,
    )
    return panel

def help_panel(txt: str, title: str) -> Panel:
    """Qemy CLI help panel."""
    txt_fmt = format_text(txt, theme='info')
    title_fmt = format_text(title, theme='title', pos='center')
    panel = Panel(
        txt_fmt,
        title = title_fmt,
        border_style = colors.panel_border,
        padding = 3
    )
    return panel

