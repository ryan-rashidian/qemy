"""Qemy CLI main module."""

import readline

from qemy.cli.cmd_register import cmd_reg
from qemy.cli.fmt import console, welcome_panel
from qemy.utils.env_setup import setup_wizard


def pre_input_hook():
    """Set terminal prompt indicator as pre-input hook."""
    console.print('>>> ', style='info', end='')
    return

class QemyCLI():
    """Qemy CLI."""
    def __init__(self):
        """CLI setup sequence."""
        readline.set_pre_input_hook(pre_input_hook)
        readline.set_history_length(100)
        setup_wizard()
        self.commands = cmd_reg

    def run(self):
        """Main CLI loop."""
        welcome_panel()
        while True:
            raw = input().strip().lower()
            if not raw:
                continue

            parts = raw.split()
            cmd, *args = parts
            if cmd in ('exit', 'quit', 'q'):
                console.print('Exiting.', style='warning')
                break
            func = self.commands.get(cmd)
            if func:
                try:
                    func(*args)
                except Exception as e:
                    console.print(f'Error:\n{e}', style='warning')
            else:
                console.print(f'Unknown command: {cmd}', style='warning')

