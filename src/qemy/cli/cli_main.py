"""Qemy CLI main module."""

import readline

from qemy.cli.format.fmt import FormatText
from qemy.cli.cmd_register import cmd_registry

def pre_input_hook() -> None:
    """Set terminal prompt indicator as pre-input hook."""
    FormatText('>>> ').style(theme='info').print()

class QemyCLI:
    """Qemy CLI manager."""

    def __init__(self):
        """CLI initialization sequence."""
        readline.set_pre_input_hook(pre_input_hook)
        readline.set_history_length(100)
        self.commands: dict = cmd_registry
        self.running = False

    def stop(self):
        """Halt main CLI loop."""
        self.running = False

    def prompt_cmd(self) -> list[str]:
        """Prompt for user input and split commands."""
        cmd_raw = input().strip().lower()
        return cmd_raw.split()

    def handle_cmd(self, cmd: str, *args: str):
        """Handle execution of CLI commands."""
        if cmd in ('exit', 'quit', 'q'):
            self.stop()
            return

        func = self.commands.get(cmd)
        if func:
            try:
                func(*args)
            except Exception as e:
                FormatText(f'Error\n{e}').style('warning').print()
        else:
            FormatText(f'Unknown command: {cmd}').style('warning').print()

    def run(self):
        """Start main CLI loop."""
        self.running = True
        while self.running:
            cmd, *args = self.prompt_cmd()
            if not cmd:
                continue
            self.handle_cmd(cmd, *args)

