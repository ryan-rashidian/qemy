"""Command registry for Qemy CLI."""

from qemy.cli_ref.commands.api_edgar import cmd_filing
from qemy.cli_ref.commands.core import cmd_score
from qemy.cli_ref.info.helper import print_help

cmd_reg = {
    'f': cmd_filing,
    's': cmd_score,
    'help': print_help,
    '?': print_help
}
