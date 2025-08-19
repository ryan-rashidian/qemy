"""Command registry for Qemy CLI."""

from qemy.cli.commands.api_edgar import cmd_bulk_refresh, cmd_filing
from qemy.cli.commands.aux import cmd_clear, cmd_rmenv, cmd_calc
from qemy.cli.commands.core import cmd_score
from qemy.cli.info.helper import print_help

cmd_reg = {
    'f': cmd_filing,
    's': cmd_score,
    'fsync': cmd_bulk_refresh,
    'rmenv': cmd_rmenv,
    'calc': cmd_calc,
    'clear': cmd_clear,
    'cls': cmd_clear,
    'help': print_help,
    '?': print_help
}
