"""Help and info commands for Qemy CLI."""

import importlib.resources as res

from qemy.cli.format.fmt import FormatText
from qemy.cli.format.panels import info_panel, markdown_panel

help_registry: dict[str, str] = {}

def help_text(txt: str):
    def decorator(func):
        func._help_text = txt
        help_registry[func.__name__] = txt
        return func
    return decorator

def _load_markdown(filename: str) -> str:
    """Load markdown files into Python."""
    return res.files('qemy.cli.man').joinpath(filename).read_text()

def cmd_help(cmd: str='help') -> None:
    """Help command for Qemy CLI."""
    cmd = cmd.strip().lower()

    if cmd in ('help', '?'):
        md_txt = _load_markdown('help.md')
        markdown_panel(txt=md_txt, title='Qemy Help Menu')

    else:
        help_txt = help_registry.get(f'cmd_{cmd}')
        if help_txt:
            info_panel(txt=help_txt, title=f'Command: {cmd}')
        else:
            FormatText(f'{cmd} not found').style('warning').print()

