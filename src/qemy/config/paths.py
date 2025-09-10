"""Filesystem paths used by Qemy."""

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

BULK_DATA_DIR = PROJECT_ROOT / 'bulk_data'
BULK_DATA_DIR.mkdir(parents=True, exist_ok=True)

