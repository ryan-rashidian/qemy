from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import config as cfg

def get_next_path(base_dir: Path, name="file", ext="png") -> Path:
    i = 1
    while True:
        check = base_dir / f"{name}{i}.{ext}"
        if not check.exists():
            return check
        i += 1

def save_to_png(filename):
    output_path =  get_next_path(cfg.EXPORT_CHART_DIR, name=filename, ext='png')
    plt.savefig(output_path)

def save_to_csv(df: pd.DataFrame):
    output_path =  get_next_path(cfg.EXPORT_TABLE_DIR, name='table', ext='csv')
    df.reset_index(inplace=True)
    df.to_csv(output_path, index=False)

