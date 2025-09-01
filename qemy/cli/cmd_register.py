"""Command registry for Qemy CLI."""

from qemy.cli.commands.api_edgar import (
    cmd_fsync,
    cmd_fc,
    cmd_f,
)
from qemy.cli.commands.aux import cmd_calc, cmd_clear, cmd_rmenv
from qemy.cli.commands.core import cmd_fscore
from qemy.cli.commands.helper import cmd_help, cmd_info

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
