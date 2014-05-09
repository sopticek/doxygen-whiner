#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Unit tests for the warning module."""

import unittest

from doxygen_whiner.warning import Warning
from doxygen_whiner.warning import parse_warnings


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

    def test_repr(self):
        warn = Warning('/src/check.h', 25, 'missing argument')
        self.assertEqual(repr(warn),
            "Warning('/src/check.h', 25, 'missing argument')")


class TestParseWarnings(unittest.TestCase):
    def scenario_warnings_are_parsed_correctly(self, text, exp_warnings):
        self.assertEqual(parse_warnings(text), exp_warnings)

    def create_warning_text_and_instance(self, path, line, text):
        warn_text = path + ':' + str(line) + ': warning: '+ text + '\n'
        warn = Warning(path, line, text)
        return (warn_text, warn)

    def test_parse_empty_text(self):
        self.scenario_warnings_are_parsed_correctly('', [])

    def test_parse_text_with_one_warning(self):
        text, warn = self.create_warning_text_and_instance(
            '/src/checking.h', 25, 'missing argument after \class')
        exp_warnings = [warn]
        self.scenario_warnings_are_parsed_correctly(text, exp_warnings)

    def test_parse_text_with_two_warnings(self):
        text1, warn1 = self.create_warning_text_and_instance(
            '/src/checking.h', 25, 'missing argument after \class')
        text2, warn2 = self.create_warning_text_and_instance(
            '/src/checking.c', 34, 'include file error.h not found')
        exp_warnings = [warn1, warn2]
        self.scenario_warnings_are_parsed_correctly(text1 + text2, exp_warnings)

    def test_lines_in_text_with_invalid_format_are_ignored(self):
        text, warn = self.create_warning_text_and_instance(
            '/src/checking.h', 25, 'missing argument after \class')
        text = '#blabla\n' + text + '#blablaba\n'
        exp_warnings = [warn]
        self.scenario_warnings_are_parsed_correctly(text, exp_warnings)

    def test_parse_text_with_multiline_warning(self):
        text, warn = self.create_warning_text_and_instance(
            '/src/checking.h', 25, 'the following parameters are not documented:\n'
            "\tparameter 'n'\n"
            "\tparameter 'm'")
        exp_warnings = [warn]
        self.scenario_warnings_are_parsed_correctly(text, exp_warnings)

