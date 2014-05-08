#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Unit tests for the warning module."""

import unittest

from doxygen_whiner.warning import Warning


class TestWarning(unittest.TestCase):
    def test_warning_attributes_are_correctly_set_after_creation(self):
        file = '/mnt/data/error.c'
        line = 45
        text = 'missing argument after \class'
        w = Warning(file, line, text)
        self.assertEqual(w.file, file)
        self.assertEqual(w.line, line)
        self.assertEqual(w.text, text)

    def test_types_of_warning_attributes_are_checked(self):
        self.assertRaises(TypeError, Warning, 52, 45, '')
        self.assertRaises(TypeError, Warning, '', 45.5, '')
        self.assertRaises(TypeError, Warning, '', 45, 45)
