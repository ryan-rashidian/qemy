import shlex
import argparse

def parse_engine(arg_str, def_args, prog_name='command'):
    parser = argparse.ArgumentParser(prog=prog_name)
    def_args(parser)
    try:
        args = parser.parse_args(shlex.split(arg_str))
        return args
    except SystemExit:
        return None
#=============================================================================#
def define_arg_s(parser):
    parser.add_argument('-s', '--save', default='NO', help='save (e.g. -s y, --save yes)')
def parse_arg_s(arg, name='none'):
    args = parse_engine(arg, define_arg_s, prog_name=name)
    if not args:
        return None
    return args.save.upper()

def define_arg_p(parser):
    parser.add_argument('-p', '--period', default='1Y', help='period (e.g. 5D, 3M, 1Y)')
def parse_arg_p(arg, name='none'):
    args = parse_engine(arg, define_arg_p, prog_name=name)
    if not args:
        return None
    return args.period

def define_arg_p_t(parser):
    parser.add_argument('-p', '--period', default='1W', help='period (e.g. 5D, 3M, 1Y)')
    parser.add_argument('ticker', help='stock ticker symbol')
def parse_arg_p_t(arg, name='none'):
    args = parse_engine(arg, define_arg_p_t, prog_name=name)
    if not args:
        return None, None
    return args.period, args.ticker.upper()

def define_arg_p_s(parser):
    parser.add_argument('-p', '--period', default='1Y', help='period (e.g. -p 5D, --price 3M, -p 1Y)')
    parser.add_argument('-s', '--save', default='NO', help='save (e.g. -s y, --save yes)')
def parse_arg_p_s(arg, name='none'):
    args = parse_engine(arg, define_arg_p_s, prog_name=name)
    if not args:
        return None, None
    return args.period, args.save.upper()

