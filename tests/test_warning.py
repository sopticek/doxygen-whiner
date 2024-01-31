#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@protonmail.com
# Date:     2014-05-08
#

"""Unit tests for the warning module."""

import unittest

from doxygen_whiner.warning import Person
from doxygen_whiner.warning import Warning
from doxygen_whiner.warning import WarningWithCulprit
from doxygen_whiner.warning import parse_warnings
from doxygen_whiner.warning import group_by_culprit


class TestWarning(unittest.TestCase):
    def test_warning_attributes_are_correctly_set_after_creation(self):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
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
        warn = Warning('/src/check.h', 25, r'missing argument after \class')
        self.assertEqual(repr(warn),
            r"Warning('/src/check.h', 25, 'missing argument after \\class')")

    def test_dir_returns_correct_directory(self):
        warn = Warning('/src/check.h', 25, 'missing argument')
        self.assertEqual(warn.dir, '/src')

    def test_dir_cannot_be_set(self):
        warn = Warning('/src/check.h', 25, 'missing argument')
        with self.assertRaises(AttributeError):
            warn.dir = '/usr/src'

    def test_file_name_correctly_returns_file_name(self):
        warn = Warning('/src/check.h', 25, r'missing argument after \class')
        self.assertEqual(warn.file_name, 'check.h')

    def test_original_data_correctly_formats_warning(self):
        warn = Warning('/src/check.h', 25, r'missing argument after \class')
        self.assertEqual(warn.original_data,
            r'/src/check.h:25: warning: missing argument after \class')


class TestPerson(unittest.TestCase):
    def test_create_person_and_access_its_data(self):
        name = 'John Little'
        email = 'john.little@gmail.com'
        person = Person(name, email)
        self.assertEqual(person.name, name)
        self.assertEqual(person.email, email)

    def test_create_person_with_invalid_type_of_its_data(self):
        self.assertRaises(TypeError, Person, 10, 'a@mail.com')
        self.assertRaises(TypeError, Person, 'John Little', 10)

    def test_two_person_with_same_data_are_equivalent(self):
        person1 = Person('John Little', 'john.little@gmail.com')
        person2 = Person('John Little', 'john.little@gmail.com')
        self.assertEqual(person1, person2)

    def test_two_persons_with_different_names_are_not_equivalent(self):
        person1 = Person('John Little', 'john.little@gmail.com')
        person2 = Person('John Huge', 'john.little@gmail.com')
        self.assertNotEqual(person1, person2)

    def test_two_persons_with_different_email_are_not_equivalent(self):
        person1 = Person('John Little', 'john.little@gmail.com')
        person2 = Person('John Little', 'john.huge@gmail.com')
        self.assertNotEqual(person1, person2)

    def test_repr(self):
        name = 'John Little'
        email = 'john.little@gmail.com'
        person = Person(name, email)
        self.assertEqual(repr(person),
            "Person('John Little', 'john.little@gmail.com')")

    def test_lt_gt(self):
        aa = Person('A', 'A@gmail.com')
        ab = Person('A', 'B@gmail.com')
        ba = Person('B', 'A@gmail.com')
        self.assertLess(aa, ab)
        self.assertLess(aa, ba)
        self.assertGreaterEqual(ba, aa)
        self.assertGreaterEqual(ab, aa)


class TestWarningWithCulprit(unittest.TestCase):
    def test_create_warning_and_access_its_data(self):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        warn = Warning(file, line, text)
        name = 'John Little'
        email = 'john.little@gmail.com'
        culprit = Person(name, email)
        warn_with_culprit = WarningWithCulprit(warn, culprit)
        self.assertEqual(warn_with_culprit.culprit, culprit)
        self.assertEqual(warn_with_culprit.file, file)
        self.assertEqual(warn_with_culprit.line, line)
        self.assertEqual(warn_with_culprit.text, text)

    def test_repr(self):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        warn = Warning(file, line, text)
        name = 'John Little'
        email = 'john.little@gmail.com'
        culprit = Person(name, email)
        warn_with_culprit = WarningWithCulprit(warn, culprit)
        self.assertEqual(repr(warn_with_culprit),
            "WarningWithCulprit({}, {})".format(warn, culprit))



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

    def test_parse_text_which_starts_with_white_space(self):
        text, warn = self.create_warning_text_and_instance(
            '/src/checking.h', 25, 'missing argument after \class')
        text = '  \n' + text
        exp_warnings = [warn]
        self.scenario_warnings_are_parsed_correctly(text, exp_warnings)


class TestGroupByCulprit(unittest.TestCase):
    def create_warning_and_culprit(self, culprit_name):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        warn = Warning(file, line, text)
        email = 'generic@gmail.com'
        culprit = Person(culprit_name, email)
        warn_with_culprit = WarningWithCulprit(warn, culprit)
        return (warn_with_culprit, culprit)

    def test_without_warnings_generates_nothing(self):
        gen = group_by_culprit([])
        self.assertRaises(StopIteration, next, gen)

    def test_with_one_warning_generates_one_result(self):
        warn, culprit = self.create_warning_and_culprit('John Little')
        gen = group_by_culprit([warn])
        self.assertEqual(next(gen), (culprit, [warn]))
        self.assertRaises(StopIteration, next, gen)

    def test_two_persons_each_with_one_warning(self):
        warn1, culprit1 = self.create_warning_and_culprit('John Little')
        warn2, culprit2 = self.create_warning_and_culprit('Jane Book')
        gen = group_by_culprit([warn1, warn2])
        self.assertEqual(next(gen), (culprit2, [warn2]))
        self.assertEqual(next(gen), (culprit1, [warn1]))
        self.assertRaises(StopIteration, next, gen)

    def test_two_persons_each_with_two_warnings(self):
        warn1, culprit1 = self.create_warning_and_culprit('John Little')
        warn2, _        = self.create_warning_and_culprit('John Little')
        warn3, culprit2 = self.create_warning_and_culprit('Jane Book')
        warn4, _        = self.create_warning_and_culprit('Jane Book')

        gen = group_by_culprit([warn1, warn2, warn3, warn4])
        self.assertEqual(next(gen), (culprit2, [warn3, warn4]))
        self.assertEqual(next(gen), (culprit1, [warn1, warn2]))
        self.assertRaises(StopIteration, next, gen)
