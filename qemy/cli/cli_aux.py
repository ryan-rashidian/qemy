import sys
from pathlib import Path

def env_reset():
    if getattr(sys, 'frozen', False):
        project_root = Path(sys.executable).resolve().parent
    else:
        project_root = Path(__file__).resolve().parents[2]

    env_path = project_root / '.env'

    confirm = input("Are you sure you want to delete the .env file? This action will also exit qemy. (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Aborted. .env file was not deleted.\n")
        return

    if env_path.exists():
        env_path.unlink()
        print(".env file deleted. Exiting qemy...\n")
        sys.exit()
    else:
        print("No .env file found. Nothing to delete.\n")
        return

