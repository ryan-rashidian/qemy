"""Commands for Qemy Analytics Scores."""

from qemy.analytics.base import CompanyAnalytics
from qemy.analytics.scores.f_score import PiotroskiFScore
from qemy.cli.commands.help import help_text
from qemy.cli.format.fmt import FormatText
from qemy.cli.format.panels import info_panel, result_panel


def _score_piotroski_f(ticker: str) -> None:
    """Use Qemy PiotroskiFScore from within Qemy CLI."""
    results: CompanyAnalytics = PiotroskiFScore(ticker).calculate()

    company_name = results.entity_name
    ticker_fmt = results.ticker
    result_data = results.results

    info_title = 'Piotroski F-Score'
    info_description = results.description

    components_title = 'Components:'
    components_description = (
        f"Net Income = {result_data['netinc']}\n"
        f"Operating Cash Flow = {result_data['ocf']}\n"
        f"Accruals = {result_data['accruals']}\n"
        f"Return on Assets = {result_data['roa']}\n"
        f"Long Term Debt = {result_data['ldebt']}\n"
        f"Current Ratio = {result_data['cratio']}\n"
        f"Shares Outstanding = {result_data['shares']}\n"
        f"Gross Margin = {result_data['gmargin']}\n"
        f"Asset Turnover = {result_data['asset_turnover']}"
    )

    results_title = f'{company_name} ({ticker_fmt}): F-Score'
    results_description = f"{result_data['f_score']}"

    info_panel(txt=info_description, title=info_title)
    info_panel(txt=components_description, title=components_title)
    result_panel(txt=results_description, title=results_title)

@help_text("""Category: [Selector]
Description: Select and execute an analytics scores.
    - type `scores` to get a list of possible scores with descriptions

Usage: >>> m <SCORE> *<SCORE_PARAMETERS>
""")
def cmd_score(score_type: str, *args: str) -> None:
    """Main score selection command for Qemy CLI."""
    score_type = score_type.strip().lower()
    if score_type == 'f':
        _score_piotroski_f(*args)
    else:
        FormatText(
            f'Score type not found: {score_type}\n'
        ).style('warning').print()

