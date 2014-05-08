#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Test utilities."""

import os
import sys
from tempfile import NamedTemporaryFile

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


class RedirectStdin:
    def __init__(self, stdin):
        self._stdin = stdin

    def __enter__(self):
        self._old_stdin = sys.stdin
        sys.stdin = self._stdin

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdin = self._old_stdin


class TemporaryFile:
    def __init__(self, content):
        self.content = content

    def __enter__(self):
        with NamedTemporaryFile('wt', delete=False) as f:
            self.name = f.name
            try:
                f.write(self.content)
            except:
                os.remove(self.name)
                raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self.name)
