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

    def test_two_warnings_with_same_data_are_equivalent(self):
        warn1 = Warning('/src/check.h', 25, 'missing argument')
        warn2 = Warning('/src/check.h', 25, 'missing argument')
        self.assertEqual(warn1, warn2)

    def test_two_warnings_with_different_file_are_not_equivalent(self):
        warn1 = Warning('/src/check.h', 25, 'missing argument')
        warn2 = Warning('/home/soptik/spam.c', 25, 'missing argument')
        self.assertNotEqual(warn1, warn2)

    def test_two_warnings_with_different_line_are_not_equivalent(self):
        warn1 = Warning('/src/check.h', 25, 'missing argument')
        warn2 = Warning('/src/check.h', 123, 'missing argument')
        self.assertNotEqual(warn1, warn2)

    def test_two_warnings_with_different_text_are_not_equivalent(self):
        warn1 = Warning('/src/check.h', 25, 'missing argument')
        warn2 = Warning('/src/check.h', 25, 'file not found')
        self.assertNotEqual(warn1, warn2)
