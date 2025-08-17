"""Qemy CLI."""

from qemy.cli_ref.commands.api_edgar import cmd_filing

class QemyCLI():
    def __init__(self):
        self.commands = {
            'quit': self.cmd_quit,
            'f': cmd_filing
        }
        self.running = True

    def cmd_quit(self):
        print('Quiting.')
        self.running = False

    def run(self):
        """Main REPL loop."""
        print('Welcome.')
        while self.running:
            raw = input('qemy> ').strip()
            if not raw:
                continue 
            parts = raw.split()
            cmd, *args = parts
            func = self.commands.get(cmd)
            if func:
                try:
                    func(*args)
                except Exception as e:
                    print(f'Error:\n{e}')
            else:
                print(f'Unknown command: {cmd}')

