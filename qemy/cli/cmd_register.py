"""Command registry for Qemy CLI."""

from qemy.cli.commands.api_edgar import cmd_filing
from qemy.cli.commands.core import cmd_score
from qemy.cli.info.helper import print_help

cmd_reg = {
    'f': cmd_filing,
    's': cmd_score,
    'help': print_help,
    '?': print_help
}
