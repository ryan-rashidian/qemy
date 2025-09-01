"""Command registry for Qemy CLI."""

from qemy.cli.commands import (
    cmd_calc,
    cmd_clear,
    cmd_f,
    cmd_fc,
    cmd_fscore,
    cmd_fsync,
    cmd_help,
    cmd_info,
    cmd_rmenv,
)

cmd_reg = {
    'f': cmd_f,
    'fc': cmd_fc,
    'fscore': cmd_fscore,
    'fsync': cmd_fsync,
    'rmenv': cmd_rmenv,
    'calc': cmd_calc,
    'clear': cmd_clear,
    'cls': cmd_clear,
    'help': cmd_help,
    '?': cmd_help,
    'info': cmd_info
}
