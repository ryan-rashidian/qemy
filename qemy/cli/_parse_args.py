import shlex
import argparse

ARGUMENTS = {
    'save':          lambda p: p.add_argument('-s', '--save', action='store_true'),
    'period':        lambda p: p.add_argument('-p', '--period', default='1Y'),
    'units':         lambda p: p.add_argument('-u', '--units'),
    'ticker':        lambda p: p.add_argument('ticker'),
    'ticker_flag':   lambda p: p.add_argument('-t', '--ticker'),
    'num':           lambda p: p.add_argument('-n', '--num', default=1000),
    'quarter':       lambda p: p.add_argument('-q', '--quarter', default='10'),
    'metric':        lambda p: p.add_argument('-m', '--metric', default='epsd'),
    'metric_p':      lambda p: p.add_argument('metric_p'),
    'model':         lambda p: p.add_argument('model'),
    'plot':          lambda p: p.add_argument('-plt', '--plot', action='store_true'),
    'help':          lambda p: p.add_argument('-h', '--help', action='store_true'),
    'request':       lambda p: p.add_argument('-r', '--request', action='store_true'),
    'plot_p':        lambda p: p.add_argument('plot_p'),
    'file':          lambda p: p.add_argument('-f', '--file')
}

def parse_args_cli(arg_str, expected_args, prog_name='command'):
    parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    for arg in expected_args:
        if arg not in ARGUMENTS:
            raise ValueError(f"Unknown core arg: {arg}")
        ARGUMENTS[arg](parser)

    tokens = shlex.split(arg_str)
    try:
        known_args, unknown_args = parser.parse_known_args(tokens)

        core_args = []
        for arg in expected_args:
            if arg == 'ticker_flag':
                val = getattr(known_args, 'ticker', None)
            else:
                val = getattr(known_args, arg, None)

            if isinstance(val, str) and arg in (
                'ticker', 'ticker_flag', 'metric', 'metric_p', 
                'save', 'plot_p', 'file'
            ):
                val = val.upper()

            if arg == 'num' and val is not None:
                try:
                    val = int(val)
                except (ValueError, TypeError):
                    val = None

            core_args.append(val)

        it = iter(unknown_args)
        plugin_kwargs = {}
        other_args = []
        for k in it:
            if not k.startswith('--'):
                other_args.append(k)
                continue
            key = k.lstrip('-').replace('-', '_')
            try:
                val = next(it)
                plugin_kwargs[key] = val
            except StopIteration:
                plugin_kwargs[key] = True

        return tuple(core_args), plugin_kwargs, other_args

    except SystemExit:
        raise TypeError

def check_help(arg_str, help_func=None):
    tokens = shlex.split(arg_str)
    has_help = '-h' in tokens or '--help' in tokens
    has_command = next((t for t in tokens if not t.startswith('-')), None)
    if has_help and has_command is None:
        if help_func:
            help_func()
        return True
    return False

