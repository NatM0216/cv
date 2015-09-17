#!/usr/bin/env python
"""jinja: basic jinja templating
"""

from __future__ import absolute_import, division, print_function
from future_builtins import ascii, filter, hex, map, oct, zip

__version__ = "$Revision: 871 $"

## Copyright 2011, 2015 Michael M. Hoffman <mmh1@uw.edu>

import codecs
import sys

from jinja2 import Environment, FileSystemLoader

def parse_variable_specs(specs):
    res = {}

    if not specs:
        return res

    for spec in specs:
        key, _, value = spec.partition("=")
        res[key] = value

    return res

def jinja(infile, outfilename, variable_specs):
    env = Environment(loader=FileSystemLoader([".", "../cv-private"]),
                      extensions=['jinja2.ext.do'])
    template = env.get_template(infile)

    variables = parse_variable_specs(variable_specs)

    with codecs.open(outfilename, "w", "utf-8") as outfile:
        print(template.render(variables), file=outfile)

def parse_args(args):
    from argparse import (ArgumentDefaultsHelpFormatter, ArgumentParser,
                          FileType)

    description = __doc__.splitlines()[0].partition(": ")[2]
    parser = ArgumentParser(description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("infile", metavar="INFILE",
                        help="input Jinja template")
    parser.add_argument("outfile", nargs="?", metavar="OUTFILE",
                        help="output file")

    parser.add_argument("-s", "--set", action="append", metavar="VAR=VALUE",
                        help="set variable VAR to VALUE")

    version = "%(prog)s {}".format(__version__)
    parser.add_argument("--version", action="version", version=version)

    return parser.parse_args(args)

def main(argv=sys.argv[1:]):
    args = parse_args(argv)

    return jinja(args.infile, args.outfile, args.set)

if __name__ == "__main__":
    sys.exit(main())