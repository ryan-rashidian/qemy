from pathlib import Path
from qemy.cli.format import print_markdown

def print_help():
    current_dir = Path(__file__).parent
    help_path = current_dir / "help.md"
    md_text = help_path.read_text()
    print_markdown(md_text, theme='info')

