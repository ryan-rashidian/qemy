"""Command registry for Qemy CLI."""

from qemy.cli.commands.api_edgar import cmd_filing, cmd_bulk_refresh
from qemy.cli.commands.core import cmd_score
from qemy.cli.commands.aux import cmd_clear, cmd_rmenv
from qemy.cli.info.helper import print_help

cmd_reg = {
    'f': cmd_filing,
    's': cmd_score,
    'fsync': cmd_bulk_refresh,
    'rmenv': cmd_rmenv,
    'clear': cmd_clear,
    'cls': cmd_clear,
    'help': print_help,
    '?': print_help
}
