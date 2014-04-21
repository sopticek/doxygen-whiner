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

def main(argc, argv):
    args = parse_args(argv)

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
