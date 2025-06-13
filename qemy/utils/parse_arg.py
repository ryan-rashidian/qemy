import shlex
import argparse

ARGUMENTS = {
    'save':          lambda p: p.add_argument('-s', '--save', action='store_true', help="Placeholder"),
    'period':        lambda p: p.add_argument('-p', '--period', default='1Y', help="Placeholder"),
    'units':         lambda p: p.add_argument('-u', '--units', help="Placeholder"),
    'ticker':        lambda p: p.add_argument('ticker', help="Stock ticker symbol"),
    'ticker_flag':   lambda p: p.add_argument('-t', '--ticker', required=True, help="Stock ticker symbol"),
    'num':           lambda p: p.add_argument('-n', '--num', default=1000, help="Placeholder"),
    'quarter':       lambda p: p.add_argument('-q', '--quarter', default='20', help="Placeholder"),
    'metric':        lambda p: p.add_argument('-m', '--metric', default='eps', help="Placeholder"),
    'model':         lambda p: p.add_argument('model', help="Placeholder"),
    'plot':          lambda p: p.add_argument('-plt', '--plot', action='store_true', help="Placeholder"),
}

def parse_args(arg_str, expected_args, prog_name='command'):
    parser = argparse.ArgumentParser(prog=prog_name)
    for arg in expected_args:
        if arg not in ARGUMENTS:
            raise ValueError(f"Unknown arg type: {arg}")
        ARGUMENTS[arg](parser)

    try:
        args = parser.parse_args(shlex.split(arg_str))
        result = []
        for arg in expected_args:
            if arg == 'ticker_flag':
                val = getattr(args, 'ticker', None)
            else:
                val = getattr(args, arg, None)

            if isinstance(val, str) and arg in ('ticker', 'ticker_flag', 'metric', 'save'):
                val = val.upper()

            if arg in ('num',) and val is not None:
                try:
                    val = int(val)
                except (ValueError, TypeError):
                    val = None

            result.append(val)
        return tuple(result)

    except SystemExit:
        return (None,) * len(expected_args)

