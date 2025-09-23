"""Commands for built-in Qemy Models."""

from qemy.analytics.base import CompanyAnalytics
from qemy.analytics.models.dcf import DCFModel
from qemy.cli.commands.help import help_text
from qemy.cli.format.fmt import FormatText
from qemy.cli.format.panels import info_panel, result_panel


def _model_dcf(
    ticker: str,
    years: str = '5',
    discount_rate: str = '0.08',
    terminal_growth: str = '0.03',
) -> None:
    """Use Qemy DCFModel from within Qemy CLI."""
    years_int = int(years)
    discount_rate_f = float(discount_rate)
    terminal_growth_f = float(terminal_growth)

    results: CompanyAnalytics = DCFModel(ticker).calculate(
        years = years_int,
        discount_rate = discount_rate_f,
        terminal_growth = terminal_growth_f
    )

    company_name = results.entity_name
    ticker_fmt = results.ticker
    result_data = results.results['evps']

    info_description = results.description
    info_title = 'Discounted Cash Flow (DCF) Model'

    title = f'{company_name} ({ticker_fmt}): Equity Value Per Share (EVPS)'
    description = f'EVPS: {result_data:.2f}'

    info_panel(txt=info_description, title=info_title)
    result_panel(txt=description, title=title)

@help_text("""Category: [Selector]
Description: Select and execute an analytics model.
    - type `models` to get a list of possible models with descriptions

Usage: >>> m <MODEL> *<MODEL_PARAMETERS>
""")
def cmd_m(model: str, *args: str) -> None:
    """Model selection command for Qemy CLI."""
    model = model.strip().lower()
    if model == 'dcf':
        _model_dcf(*args)
    else:
        FormatText(f'Model not found: {model}\n').style('warning').print()

