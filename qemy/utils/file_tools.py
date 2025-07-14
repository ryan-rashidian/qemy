"""Module contains functions for file exports."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from qemy import _config as cfg


def _get_next_path(base_dir: Path, name="file", ext="png") -> Path:
    """Default file name sequencing."""
    i = 1
    while True:
        check = base_dir / f"{name}{i}.{ext}"
        if not check.exists():
            return check
        i += 1

def save_to_png(filename):
    """Save plot to PNG file."""
    output_path =  _get_next_path(
        cfg.EXPORT_CHART_DIR,
        name=filename,
        ext='png'
    )
    plt.savefig(output_path)

def save_to_csv(df: pd.DataFrame):
    """Save DataFrame to CSV file."""
    output_path =  _get_next_path(
        cfg.EXPORT_TABLE_DIR,
        name='table',
        ext='csv'
    )
    df.reset_index(inplace=True)
    df.to_csv(output_path, index=False)

