#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Loads the output from the doxygen program, parses it to obtain a list of
warnings, and sends emails to users who have introduced the warning."""

import sys

from doxygen_whiner.args import parse as parse_args
from doxygen_whiner.config import parse as parse_config
from doxygen_whiner.io import read_file
from doxygen_whiner.io import read_stdin
from doxygen_whiner.warning import parse_warnings


def main(argc, argv):
    args = parse_args(argv)
    config = parse_config("config.ini", "config.local.ini")

    if args.file:
        text = read_file(args.file)
    else:
        text = read_stdin()

    warnings = parse_warnings(text)
    # TODO: remove
    from pprint import pprint
    pprint(warnings)

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
