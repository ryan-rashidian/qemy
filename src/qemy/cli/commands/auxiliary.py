"""Auxiliary commands for Qemy CLI."""

from qemy.cli.commands.help import help_text
from qemy.cli.format.fmt import FormatText, console
from qemy.cli.menus import confirm_menu
from qemy.config.credentials import remove_credential, write_credential


@help_text("""\nCategory: [Auxiliary]
Description: Clear terminal.
""")
def cmd_clear() -> None:
    """CLI clear screen command."""
    console.clear()

@help_text("""\nCategory: [Auxiliary]
Description: Calculator with Python syntax.

Usage: >>> calc <EXPRESSION>
""")
def cmd_calc(*expr_args: str) -> None:
    """CLI calculator using Python builtins."""
    expr = ''.join(expr_args)
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        FormatText(f'{str(result)}\n').style('data').print()
    except Exception as e:
        warning = FormatText(f'Invalid expression: {expr}\n{e}\n')
        warning.style('warning').print()

def _env_var_mapper(client: str) -> str | None:
    """Map CLI argument to environment variable."""
    if client == 'edgar':
        env_var = 'EDGAR_USER_AGENT'
    elif client == 'fred':
        env_var = 'FRED_API_KEY'
    elif client == 'tiingo':
        env_var = 'TIINGO_API_KEY'

    else:
        FormatText(f'{client.upper()} not found\n').style('warning').print()
        return

    return env_var

@help_text("""\nCategory: [Auxiliary]
Description: Activate a Qemy Client with API credentials.

Clients: EDGAR, FRED, TIINGO
Usage: >>> env <CLIENT>
""")
def cmd_env(client: str) -> None:
    """Add selected user credentials from Qemy CLI."""
    client = client.lower()
    env_var = _env_var_mapper(client)
    if not env_var:
        return

    if not confirm_menu():
        return

    FormatText('Enter API credentials.\n').style('info').print()
    FormatText(f'[{client.upper()}]: ').style('info').print()
    credentials = input().strip()

    write_credential(env_var=env_var, value=credentials)
    FormatText(f'[{client.upper()}] Client enabled.\n').style('info').print()
    FormatText('This was a triumph.\n').style('info').print()
    FormatText("Note: 'Huge success.'\n").style('info').print()

@help_text("""\nCategory: [Auxiliary]
Description: Deactivate a Qemy Client and remove API credentials.

Clients: EDGAR, FRED, TIINGO
Usage: >>> rmenv <CLIENT>
""")
def cmd_rmenv(client: str) -> None:
    """Remove selected user credential from Qemy APIs."""
    client = client.lower()
    env_var = _env_var_mapper(client)
    if not env_var:
        return

    if not confirm_menu():
        return

    removed, _ = remove_credential(env_var)
    if removed is None:
        FormatText(
            f'[{client.upper()}] No credentials to remove.'
        ).style('warning').print()

    FormatText(f'[{client.upper()}] Client disabled.\n').style('info').print()
    FormatText('Credentials removed.\n').style('info').print()

