"""Core commands for Qemy CLI."""

from qemy.cli.fmt import console, format_text
from qemy.core.metrics.scores import piotroski_f


def cmd_fscore(ticker: str):
    """Print Piotroski F-Score to terminal.

    Args:
        ticker (str): Company ticker symbol
    """
    d = piotroski_f(ticker)
    score = d['piotroski_f']
    txt_fmt = format_text(f'{ticker} F-Score: {score}', theme='data')
    console.print(txt_fmt)

