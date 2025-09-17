"""Menus for Qemy CLI."""

from qemy.cli.format.fmt import FormatText


def confirm_menu() -> bool:
    """Comfirmation menu (yes/no)

    Returns:
        bool: True for 'y' input and False for else
    """
    FormatText('Are your sure? (y/n): ').style('warning').print()
    comfirmation = input().strip().lower()
    if comfirmation != 'y':
        FormatText('Cancelled.').style('info').print()
        return False
    return True

