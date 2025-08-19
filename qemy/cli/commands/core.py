from qemy.cli.format import print_theme
from qemy.core.metrics.scores import piotroski_f


def cmd_score(ticker: str):
    d = piotroski_f(ticker)
    score = d['piotroski_f']
    print_theme(f'{ticker} F-Score: {score}', theme='data')

