"""Qemy CLI."""

import readline

from qemy.utils.env_setup import setup_wizard
from qemy.cli.cmd_register import cmd_reg
from qemy.cli.format import console
from qemy.cli.panels import welcome_panel

def pre_input_hook():
    console.print('>>> ', style='info', end='')
    return

class QemyCLI():
    def __init__(self):
        readline.set_pre_input_hook(pre_input_hook)
        readline.set_history_length(100)
        setup_wizard()
        self.commands = cmd_reg

    def run(self):
        """Main REPL loop."""
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
                    print(f'Error:\n{e}')
            else:
                print(f'Unknown command: {cmd}')

