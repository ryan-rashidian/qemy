"""Command registry for Qemy CLI."""

from qemy.cli.commands import (
    cmd_calc,
    cmd_clear,
    cmd_env,
    cmd_f,
    cmd_fc,
    cmd_fsync,
    cmd_rmenv,
)

cmd_registry = {
    'calc': cmd_calc,
    'clear': cmd_clear,
    'cls': cmd_clear,
    'env': cmd_env,
    'f': cmd_f,
    'fc': cmd_fc,
    'fsync': cmd_fsync,
    'rmenv': cmd_rmenv
}

