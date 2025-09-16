"""Auxiliary commands for Qemy CLI."""

from qemy.cli.format.fmt import console, FormatText

def cmd_clear() -> None:
    """CLI clear screen command."""
    console.clear()

def cmd_calc(*expr_args: str) -> None:
    """CLI calculator using Python builtins."""
    expr = ''.join(expr_args)
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        FormatText(f'{str(result)}\n').style('data').print()
    except Exception as e:
        warning = FormatText(f'Invalid expression: {expr}\n{e}\n')
        warning.style('warning').print()







