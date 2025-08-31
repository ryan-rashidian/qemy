"""Help and Info module for Qemy CLI.

Format and print markdown text with Rich library.
"""

from rich.markdown import Markdown

from qemy._config import INFO_DIR
from qemy.cli.fmt.format import console


def print_help():
    help_path = INFO_DIR / "help.md"
    md_text = help_path.read_text()
    console.print(Markdown(md_text), style='info')

def print_info():
    info_path = INFO_DIR / "info.md"
    md_text = info_path.read_text()
    console.print(Markdown(md_text), style='info')

