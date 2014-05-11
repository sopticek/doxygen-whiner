#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-10
#

"""Unit tests for the git module."""

import os
import unittest
import subprocess
from unittest import mock

from doxygen_whiner.git import Person
from doxygen_whiner.git import WarningWithCulprit
from doxygen_whiner.git import create_warning_with_culprit
from doxygen_whiner.git import GitError
from doxygen_whiner.warning import Warning


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


@mock.patch('os.chdir')
@mock.patch('subprocess.check_output')
class TestCreateWarningWithCulprit(unittest.TestCase):
    def setUp(self):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        self.warn = Warning(file, line, text)
        name = 'John Little'
        email = 'john.little@gmail.com'
        self.culprit = Person(name, email)
        self.warn_with_culprit = WarningWithCulprit(self.warn, self.culprit)

    def test_create_from_valid_data(self, mock_check_output, mock_chdir):
        mock_check_output.return_value = '\n'.join([
            'c1935c22bc9e78b5973cca27d4ad539f74cd1ee3 {0} {0} 1',
            'author {1}',
            'author-mail <{2}>',
            'author-time 1398073301',
            'author-tz +0200',
            'committer {1}',
            'committer-mail <{2}>',
            'committer-time 1398073301',
            'committer-tz +0200',
            'summary Added description.',
            'boundary',
            'filename {3}',
            '        \\class']
        ).format(
            self.warn.line,
            self.warn_with_culprit.culprit.name,
            self.warn_with_culprit.culprit.email,
            self.warn.file
        ).encode('utf-8')

        self.assertEqual(create_warning_with_culprit(self.warn),
            self.warn_with_culprit)

    def test_file_dir_does_not_exist(self, mock_check_output, mock_chdir):
        mock_chdir.side_effect = [FileNotFoundError, None]
        self.assertRaises(GitError,
            create_warning_with_culprit, self.warn)

    def test_git_command_does_not_exist(self, mock_check_output, mock_chdir):
        mock_check_output.side_effect = FileNotFoundError
        self.assertRaises(GitError,
            create_warning_with_culprit, self.warn)

    def test_file_does_not_exist(self, mock_check_output, mock_chdir):
        mock_check_output.side_effect = subprocess.CalledProcessError(128, 'git', b'error')
        with self.assertRaises(GitError) as e:
            create_warning_with_culprit(self.warn)
        self.assertEqual(str(e.exception), 'error')

    def test_line_in_file_does_not_exist(self, mock_check_output, mock_chdir):
        mock_check_output.side_effect = subprocess.CalledProcessError(128, 'git', b'error')
        with self.assertRaises(GitError) as e:
            create_warning_with_culprit(self.warn)
        self.assertEqual(str(e.exception), 'error')

    def test_upon_raising_exception_chdir_to_original_cwd_is_called(
            self, mock_check_output, mock_chdir):
        mock_check_output.side_effect = subprocess.CalledProcessError(128, 'git', b'error')
        original_cwd = os.getcwd()
        with self.assertRaises(GitError) as e:
            create_warning_with_culprit(self.warn)
        self.assertEqual(str(e.exception), 'error')
        self.assertEqual(mock_chdir.mock_calls[-1], mock.call(original_cwd))
