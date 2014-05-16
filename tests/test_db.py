#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-16
#

"""Unit tests for the db module."""

import unittest
import sqlite3

from doxygen_whiner.db import Database
from doxygen_whiner.warning import Person
from doxygen_whiner.warning import Warning
from doxygen_whiner.warning import WarningWithCulprit


class TestCreateDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')

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


class TestResetDatabase(BaseForDatabaseOperationsTests):
    def test_reset_works_correctly(self):
        self.conn.execute('INSERT INTO warnings DEFAULT VALUES;')
        self.database.reset()
        cursor = self.conn.execute('SELECT * FROM warnings;')
        self.assertFalse(cursor.fetchone())


class TestInsertWarningAndHasWarning(BaseForDatabaseOperationsTests):
    def setUp(self):
        super().setUp()

        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        warn = Warning(file, line, text)
        name = 'John Little'
        email = 'john.little@gmail.com'
        culprit = Person(name, email)
        self.warn_with_culprit = WarningWithCulprit(warn, culprit)

    def test_insert_warning_and_has_warning_work_correctly(self):
        self.database.insert_warning(self.warn_with_culprit)
        self.assertTrue(self.database.has_warning(self.warn_with_culprit))

    def test_has_warning_returns_false_if_there_is_no_warning(self):
        self.assertFalse(self.database.has_warning(self.warn_with_culprit))

