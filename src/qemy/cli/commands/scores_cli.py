"""Commands for Qemy Analytics Scores."""

from qemy.analytics.base import CompanyAnalytics
from qemy.analytics.scores.f_score import PiotroskiFScore
from qemy.cli.format.fmt import FormatText
from qemy.cli.format.panels import info_panel, result_panel


def _score_piotroski_f(ticker: str) -> None:
    """Use Qemy PiotroskiFScore from within Qemy CLI."""
    results: CompanyAnalytics = PiotroskiFScore(ticker).calculate()

    company_name = results.entity_name
    ticker_fmt = results.ticker
    result_data = results.results['f_score']

    info_description = results.description
    info_title = 'Piotroski F-Score'

    title = f'{company_name} ({ticker_fmt}): F-Score'
    description = f'Score: {result_data:.0f}'

    info_panel(txt=info_description, title=info_title)
    result_panel(txt=description, title=title)

def cmd_score(score_type: str, *args: str) -> None:
    """Main score selection command for Qemy CLI."""
    score_type = score_type.strip().lower()
    if score_type == 'f':
        _score_piotroski_f(*args)
    else:
        FormatText(
            f'Score type not found: {score_type}\n'
        ).style('warning').print()

