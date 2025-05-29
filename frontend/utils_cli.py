import shlex
import argparse

def parse_args(arg_str, def_args, prog_name='command'):
    parser = argparse.ArgumentParser(prog=prog_name)
    def_args(parser)
    
    try:
        args = parser.parse_args(shlex.split(arg_str))
        return args
    except SystemExit:
        return None

