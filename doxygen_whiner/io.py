#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""I/O-related functions."""

import sys


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


def read_stdin():
    return sys.stdin.read()

