"""Filesystem paths used by Qemy."""

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOTENV_PATH = PROJECT_ROOT / '.env'
BULK_DATA_DIR = PROJECT_ROOT / 'bulk_data'

