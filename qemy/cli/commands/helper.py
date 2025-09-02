"""Help and Info module for Qemy CLI.

Format and print markdown text with Rich library.
"""

from rich.markdown import Markdown

from qemy._config import INFO_DIR
from qemy.cli.fmt import console, help_panel
from qemy.cli.help_register import help_reg


def cmd_help(cmd: str='help'):
    """Print help information to terminal.

    Args:
        cmd (str): Command to fetch help for
    """
    if cmd == 'help':
        help_path = INFO_DIR / "help.md"
        md_text = help_path.read_text()
        console.print(Markdown(md_text), style='info')
    else:
        help_txt = help_reg.get(cmd)
        if help_txt:
            help_pnl = help_panel(txt=help_txt, title=f'{cmd} - command')
            console.print(help_pnl)
        else:
            console.print(f'{cmd} not found', style='warning')

def cmd_info():
    """Print CLI info to terminal."""
    info_path = INFO_DIR / "info.md"
    md_text = info_path.read_text()
    console.print(Markdown(md_text), style='info')

