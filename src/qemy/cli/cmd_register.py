"""Command registry for Qemy CLI."""

from qemy.cli.commands import (
    cmd_calc,
    cmd_clear,
    cmd_f,
    cmd_fc,
    cmd_fsync
)

cmd_registry = {
    'calc': cmd_calc,
    'clear': cmd_clear,
    'cls': cmd_clear,
    'f': cmd_f,
    'fc': cmd_fc,
    'fsync': cmd_fsync
}

