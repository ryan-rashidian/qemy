"""Help and Info module for Qemy CLI.

Format and print markdown text with Rich library.
"""

from rich.markdown import Markdown

from qemy._config import INFO_DIR
from qemy.cli.fmt.format import console
from qemy.cli.fmt.panels import help_panel
from qemy.cli.help.help_register import help_reg


def print_help(cmd: str='help'):
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

def print_info():
    info_path = INFO_DIR / "info.md"
    md_text = info_path.read_text()
    console.print(Markdown(md_text), style='info')

