"""Auxiliary commands for Qemy CLI."""

import sys

from qemy import _config as cfg
from qemy.cli.fmt.format import console
from qemy.cli.fmt.menus import confirm_menu


def cmd_clear() -> None:
    """CLI clear screen command."""
    console.clear()

def cmd_rmenv() -> None:
    """CLI command for deleting .env file."""
    env_path = cfg.PROJECT_ROOT / '.env'

    if not confirm_menu():
        return

    if env_path.exists():
        env_path.unlink()
        console.print(
            'API credentials deleted. Exiting Qemy...',
            style='info'
        )
        sys.exit()
    else:
        console.print(
            'No credentials found. Nothing to delete.',
            style='info'
        )
        return

def cmd_calc(*expr_args: str) -> None:
    """CLI calculator using Python builtins."""
    expr = ''.join(expr_args)
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        console.print(result, style='data')
    except Exception as e:
        console.print(f'Invalid expression: {expr}\n{e}', style='warning')

