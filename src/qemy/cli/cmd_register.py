"""Command registry for Qemy CLI."""

from qemy.cli.commands import (
    cmd_calc,
    cmd_clear
)

cmd_registry = {
    'calc': cmd_calc,
    'clear': cmd_clear,
    'cls': cmd_clear
}

