"""Help registry for Qemy CLI."""

from qemy.cli import help

help_reg = {
    'calc': help.help_calc,
    'clear': help.help_clear,
    'f': help.help_f,
    'fc': help.help_fc,
    'fscore': help.help_fscore,
    'fsync': help.help_fsync,
    'rmenv': help.help_rmenv
}

