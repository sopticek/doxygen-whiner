#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-16
#

"""Unit tests for the db module."""

import sqlite3
import tempfile
import unittest

from doxygen_whiner.db import Database
from doxygen_whiner.warning import Person
from doxygen_whiner.warning import Warning
from doxygen_whiner.warning import WarningWithCulprit


class TestCreateDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')

    def tearDown(self):
        self.conn.close()

    def test_non_existing_database_is_initialized(self):
        database = Database(self.conn)
        self.assertTrue(self.conn.execute('SELECT * FROM warnings;'))

    def test_existing_database_is_not_initialized(self):
        database1 = Database(self.conn)
        self.conn.execute('INSERT INTO warnings DEFAULT VALUES;')
        database2 = Database(self.conn)
        cursor = self.conn.execute('SELECT * FROM warnings;')
        self.assertTrue(cursor.fetchone())
        self.assertFalse(cursor.fetchone())


class BaseForDatabaseOperationsTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.database = Database(self.conn)

    def tearDown(self):
        self.conn.close()

class TestResetDatabase(BaseForDatabaseOperationsTests):
    def test_reset_works_correctly(self):
        self.conn.execute('INSERT INTO warnings DEFAULT VALUES;')
        self.database.reset()
        cursor = self.conn.execute('SELECT * FROM warnings;')
        self.assertFalse(cursor.fetchone())


def create_warning_with_culprit():
    file = '/mnt/data/error.c'
    line = 45
    text = r'missing argument after \class'
    name = 'John Little'
    email = 'john.little@gmail.com'
    culprit = Person(name, email)
    warn = Warning(file, line, text)
    return WarningWithCulprit(warn, culprit)


class TestOperationsWithWarnings(BaseForDatabaseOperationsTests):
    def setUp(self):
        super().setUp()
        self.warn_with_culprit = create_warning_with_culprit()

    def test_insert_warning_and_has_warning_work_correctly(self):
        self.database.insert_warning(self.warn_with_culprit)
        self.assertTrue(self.database.has_warning(self.warn_with_culprit))

    def test_has_warning_returns_false_if_there_is_no_warning(self):
        self.assertFalse(self.database.has_warning(self.warn_with_culprit))

    def scenario_warnings_are_compared_without_line_numbers(self,
            line1, line2, text_with_line1, text_with_line2):
        self.warn_with_culprit.line = line1
        self.warn_with_culprit.text = text_with_line1
        self.database.insert_warning(self.warn_with_culprit)
        self.warn_with_culprit.line = line2
        self.warn_with_culprit.text = text_with_line2
        self.assertTrue(self.database.has_warning(self.warn_with_culprit))

    def test_warnings_are_compared_without_line_numbers(self):
        self.scenario_warnings_are_compared_without_line_numbers(
            35, 875, 'on line', 'on line')
        self.scenario_warnings_are_compared_without_line_numbers(
            35, 35, 'on line 789', 'on line 987')
        self.scenario_warnings_are_compared_without_line_numbers(
            35, 35, 'on line:789', 'on line:987')
        self.scenario_warnings_are_compared_without_line_numbers(
            35, 35, 'on line:789 and', 'on line:987 and')

    def test_numbers_in_identifiers_are_not_line_numbers(self):
        self.warn_with_culprit.text = 'parameter dog43'
        self.database.insert_warning(self.warn_with_culprit)
        self.warn_with_culprit.text = 'parameter dog600'
        self.assertFalse(self.database.has_warning(self.warn_with_culprit))

    def test_old_warnings_are_not_considered_during_comparison(self):
        self.database.insert_warning(self.warn_with_culprit)
        self.database.make_all_warnings_old()
        self.assertFalse(self.database.has_warning(self.warn_with_culprit))


class TestDatabasePersistence(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile()
        self.conn = sqlite3.connect(self.db_file.name)

    def tearDown(self):
        self.conn.close()
        self.db_file.close()

    def test_data_are_kept_upon_closing_database_connection(self):
        database = Database(self.conn)
        warn_with_culprit = create_warning_with_culprit()
        database.insert_warning(warn_with_culprit)
        self.conn.close()
        self.conn = sqlite3.connect(self.db_file.name)
        database = Database(self.conn)
        self.assertTrue(database.has_warning(warn_with_culprit))
