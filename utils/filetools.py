from pathlib import Path

def get_next_path(base_dir: Path, name="file", ext="png") -> Path:
    i = 1
    while True:
        check = base_dir / f"{name}{i}.{ext}"
        if not check.exists():
            return check
        i += 1

