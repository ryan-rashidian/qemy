"""Help and Info module for Qemy CLI.

Format and print markdown text with Rich library.
"""

from pathlib import Path

from qemy.cli.format import console

from rich.markdown import Markdown

def print_help():
    current_dir = Path(__file__).parent
    help_path = current_dir / "help.md"
    md_text = help_path.read_text()
    console.print(Markdown(md_text), style='info')

