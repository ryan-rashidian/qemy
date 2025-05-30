import pandas as pd
from pathlib import Path
from utils.filetools import get_next_path

def save_to_csv(df: pd.DataFrame):
    project_root = Path(__file__).resolve().parents[1]
    export_dir = project_root / "exports" / "tables"
    export_dir.mkdir(parents=True, exist_ok=True)
    output_path =  get_next_path(export_dir, name='table', ext='csv')
    df.reset_index(inplace=True)
    df.to_csv(output_path, index=False)
