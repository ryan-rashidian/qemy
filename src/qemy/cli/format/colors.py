"""Initialize CLI colors from TOML."""

import importlib.resources as res
import shutil
import tomllib

from qemy.config.paths import CLI_COLORS_PATH

if not CLI_COLORS_PATH.exists():
    with res.files('qemy.cli.format').joinpath('colors.toml').open('rb') as f:
        with CLI_COLORS_PATH.open('wb') as out:
            shutil.copyfileobj(f, out)

with CLI_COLORS_PATH.open('rb') as f:
    colors: dict = tomllib.load(f)

theme_info = colors.get('theme', {}).get('info', '')
theme_data = colors.get('theme', {}).get('data', '')
theme_warning = colors.get('theme', {}).get('warning', '')
theme_title = colors.get('theme', {}).get('title', '')

table_border = colors.get('table', {}).get('border', '')
table_row_style = colors.get('table', {}).get('row_style', '')
table_val_col = colors.get('table', {}).get('value_col', '')
table_val_col_header = colors.get('table', {}).get('value_col_header', '')
table_def_col = colors.get('table', {}).get('default_col', '')
table_def_col_header = colors.get('table', {}).get('default_col_header', '')

panel_text = colors.get('panel', {}).get('text', '')
panel_border = colors.get('panel', {}).get('border', '')

misc_load_spinner = colors.get('misc', {}).get('load_spinner', '')

