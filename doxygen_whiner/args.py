#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@protonmail.com
# Date:     2014-04-21
#

"""Parses arguments from the command line."""

import argparse


def parse(argv):
    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument("file", help="load warnings from the given file",
                        nargs="?", default=None)
    parsed_args = parser.parse_args(argv[1:])
    return parsed_args
