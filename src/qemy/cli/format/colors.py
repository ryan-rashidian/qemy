"""Initialize CLI colors from TOML."""

import importlib.resources as res
import tomllib
import shutil

from qemy.config.paths import CLI_COLORS_PATH

if not CLI_COLORS_PATH.exists():
    with res.files('qemy.cli.format').joinpath('colors.toml').open('rb') as f:
        with CLI_COLORS_PATH.open('wb') as out:
            shutil.copyfileobj(f, out)

with CLI_COLORS_PATH.open('rb') as f:
    colors: dict = tomllib.load(f)

