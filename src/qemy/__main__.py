"""Qemy CLI entry point."""

import logging

from qemy.cli.cli_main import QemyCLI
from qemy.config.logger import set_log_level


def main() -> None:
    """Run Qemy CLI."""
    # Logging off by default in CLI
    set_log_level(logging.CRITICAL + 1)

    QemyCLI().run()

if __name__ == '__main__':
    main()

