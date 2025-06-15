import shlex
import argparse

ARGUMENTS = {
    'save':          lambda p: p.add_argument('-s', '--save', action='store_true'),
    'period':        lambda p: p.add_argument('-p', '--period', default='1Y'),
    'units':         lambda p: p.add_argument('-u', '--units'),
    'ticker':        lambda p: p.add_argument('ticker'),
    'ticker_flag':   lambda p: p.add_argument('-t', '--ticker'),
    'num':           lambda p: p.add_argument('-n', '--num', default=1000),
    'quarter':       lambda p: p.add_argument('-q', '--quarter', default='20'),
    'metric':        lambda p: p.add_argument('-m', '--metric', default='eps'),
    'model':         lambda p: p.add_argument('model'),
    'plot':          lambda p: p.add_argument('-plt', '--plot', action='store_true'),
    'help':          lambda p: p.add_argument('-h', '--help', action='store_true')
}

def parse_args(arg_str, expected_args, prog_name='command'):
    parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
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

    except (SystemExit, ValueError) as e:
        print(f"Invalid Command, Error:\n{e}")
        return (None,) * len(expected_args)

