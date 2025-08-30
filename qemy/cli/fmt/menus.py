"""Menu module for Qemy CLI."""

from qemy.cli.fmt.format import console


def confirm_menu() -> bool:
    """Confirmation menu. (yes/no)

    Returns:
        bool: True for 'y' input and False for else
    """
    console.print('', style='info')
    console.print('Are you sure? (y/n) ', style='warning', end='')
    confirm = input().strip().lower()
    if confirm != 'y':
        console.print('Cancelled.', style='info')
        return False
    return True
