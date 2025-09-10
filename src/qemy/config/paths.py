"""Filesystem paths used by Qemy.

Contains constants with pathlib.Path objects pointing to directories.
"""

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROJECT_ROOT: Path = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

DOTENV_PATH: Path = PROJECT_ROOT / '.env'
BULK_DATA_DIR: Path = PROJECT_ROOT / 'bulk_data'

