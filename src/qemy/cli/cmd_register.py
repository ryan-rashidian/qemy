"""Command registry for Qemy CLI."""

from qemy.cli.commands import (
    cmd_calc,
    cmd_clear,
    cmd_env,
    cmd_f,
    cmd_fsync,
    cmd_help,
    cmd_m,
    cmd_rmenv,
    cmd_s,
)

cmd_registry = {
    'calc': cmd_calc,
    'clear': cmd_clear,
    'cls': cmd_clear,
    'env': cmd_env,
    'f': cmd_f,
    'fsync': cmd_fsync,
    'help': cmd_help, '?': cmd_help,
    'm': cmd_m,
    'rmenv': cmd_rmenv,
    's': cmd_s
}

