import shlex
import argparse

ARGUMENTS = {
    'save':     lambda p: p.add_argument('-s', '--save', default='NO', help="Placeholder"),
    'period':   lambda p: p.add_argument('-p', '--period', default='1Y', help="Placeholder"),
    'units':    lambda p: p.add_argument('-u', '--units', help="Placeholder"),
    'ticker':   lambda p: p.add_argument('ticker', help="Stock ticker symbol"),
    'num':      lambda p: p.add_argument('-n', '--num', default=1000, help="Placeholder"),
    'quarter':  lambda p: p.add_argument('-q', '--quarter', default='20', help="Placeholder"),
    'metric':   lambda p: p.add_argument('-m', '--metric', default='eps', help="Placeholder"),
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
            val = getattr(args, arg)
            if isinstance(val, str) and arg in ('ticker', 'metric', 'save'):
                val = val.upper()
            result.append(val)
        return tuple(result)

    except SystemExit:
        return (None,) * len(expected_args)

