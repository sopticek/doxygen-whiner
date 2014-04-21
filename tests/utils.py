#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Test utilities."""

import sys

class Redirect:
     def __init__(self, *, stdout=None, stderr=None):
         self._stdout = stdout or sys.stdout
         self._stderr = stderr or sys.stderr

     def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

     def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr
