from qemy.cli.format import console, format_text
from qemy.core.metrics.scores import piotroski_f


def cmd_score(ticker: str):
    d = piotroski_f(ticker)
    score = d['piotroski_f']
    txt_fmt = format_text(f'{ticker} F-Score: {score}', theme='data')
    console.print(txt_fmt)

