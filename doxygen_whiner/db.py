#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-16
#

"""Module for working with database."""

class Database:
    def __init__(self, conn):
        self.conn = conn
        self._initialize_table()

    def _initialize_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                file TEXT,
                line INTEGER,
                text TEXT,
                name TEXT,
                email TEXT);
        ''')

    def _convert_warning_to_tuple(self, warning):
        return (
            warning.file,
            warning.line,
            warning.text,
            warning.culprit.name,
            warning.culprit.email
        )

    def insert_warning(self, warning):
        self.conn.execute('''
            INSERT INTO warnings VALUES (?, ?, ?, ?, ?);''',
            self._convert_warning_to_tuple(warning)
        )

    def has_warning(self, warning):
        cursor = self.conn.execute('''
            SELECT * FROM warnings
            WHERE file = ?
                AND line = ?
                AND text = ?
                AND name = ?
                AND email = ?;''',
            self._convert_warning_to_tuple(warning)
        )
        return cursor.fetchone() is not None


    def reset(self):
        self.conn.execute('DELETE FROM warnings;')
