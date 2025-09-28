"""Filesystem paths used by Qemy.

Contains constants with pathlib.Path objects pointing to directories.
"""

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOTENV_PATH: Path = PROJECT_ROOT / '.env'

BULK_DATA_DIR: Path = PROJECT_ROOT / 'bulk_data'
COMPANYFACTS_ZIP: Path = BULK_DATA_DIR / 'companyfacts.zip'
COMPANYFACTS_UNZIPPED: Path = BULK_DATA_DIR / 'companyfacts'
COMPANY_TICKERS_JSON: Path = BULK_DATA_DIR / 'company_tickers.json'

PLUGINS_DIR: Path = PROJECT_ROOT / 'plugins'

CLI_COLORS_PATH: Path = PROJECT_ROOT / 'qemy_colors.toml'

