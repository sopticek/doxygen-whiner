#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Unit tests for the io module."""

import unittest
from io import StringIO

from doxygen_whiner import io
from .utils import TemporaryFile
from .utils import RedirectStdin


class TestIOReadFile(unittest.TestCase):
    def scenario_file_is_read_correctly(self, data):
        with TemporaryFile(data) as tf:
            self.assertEqual(io.read_file(tf.name), data)

    def test_empty_file_is_read_correctly(self):
        self.scenario_file_is_read_correctly('')

    def test_nonempty_file_is_read_correctly(self):
        data = 'blablabla\nblablabla\nbla'
        self.scenario_file_is_read_correctly(data)

    def test_exception_is_raised_on_nonexisting_file(self):
        self.assertRaises(FileNotFoundError, io.read_file,
            '89r_15t8y1.txt')


class TestIOReadStdin(unittest.TestCase):
    def scenario_stdin_is_read_correctly(self, data):
        stream = StringIO(data)
        with RedirectStdin(stream):
            self.assertEqual(io.read_stdin(), data)

    def test_no_data_on_stdin(self):
        self.scenario_stdin_is_read_correctly('')

    def test_data_on_stdin(self):
        data = 'blabla\nblababla\nbla'
        self.scenario_stdin_is_read_correctly(data)
