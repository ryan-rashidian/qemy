"""Commands for EDGARClient in Qemy CLI."""

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from qemy.cli.format import colors
from qemy.cli.menus import confirm_menu
from qemy.clients.edgar import (
    delete_bulk_data,
    download_cik_mapping,
    download_companyfacts_zip,
    unzip_companyfacts,
)


def cmd_fsync() -> None:
    """Download SEC bulk data from within Qemy CLI."""
    if not confirm_menu():
        return

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        BarColumn()
    ) as progress:
        task = progress.add_task(
            f'{colors.load_spinner}[Downloading SEC bulk data...]',
            total = 4
        )

        delete_bulk_data()
        progress.advance(task)
        download_cik_mapping()
        progress.advance(task)
        download_companyfacts_zip()
        progress.advance(task)
        unzip_companyfacts()
        progress.advance(task)

