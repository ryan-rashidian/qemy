"""Qemy CLI."""

import readline

from qemy.cli_ref.cmd_register import cmd_reg
from qemy.cli_ref.format import print_panel, print_prompt, print_theme

readline.set_history_length(100)

class QemyCLI():
    def __init__(self):
        self.commands = cmd_reg

    def run(self):
        """Main REPL loop."""
        print_panel()
        while True:
            print_prompt()
            raw = input().strip().lower()
            if not raw:
                continue 

            parts = raw.split()
            cmd, *args = parts
            if cmd in ('exit', 'quit', 'q'):
                print_theme('Exiting.', theme='warning')
                break
            func = self.commands.get(cmd)
            if func:
                try:
                    func(*args)
                except Exception as e:
                    print(f'Error:\n{e}')
            else:
                print(f'Unknown command: {cmd}')

