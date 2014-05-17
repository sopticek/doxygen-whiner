#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-16
#

"""Module for working with database."""

import re


class Database:
    def __init__(self, conn):
        self.conn = conn
        self._initialize_table()

    def _initialize_table(self):
        # The new column is, in fact, of the Boolean type (sqlite3 does not
        # support the Boolean type, so we use the Integer type).
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                file TEXT,
                line INTEGER,
                text TEXT,
                text_to_cmp TEXT,
                name TEXT,
                email TEXT,
                new INTEGER DEFAULT 1);
        ''')

    def _get_text_to_cmp(self, text):
        return re.sub(r'\b\d+\b', 'XXX', text)

    def insert_warning(self, warning):
        self.conn.execute('''
            INSERT INTO warnings (file, line, text, text_to_cmp, name, email)
                VALUES (?, ?, ?, ?, ?, ?);''',
            (warning.file,
             warning.line,
             warning.text,
             self._get_text_to_cmp(warning.text),
             warning.culprit.name,
             warning.culprit.email
            )
        )

    def has_warning(self, warning):
        # While comparing we do not take into consideration the line number and
        # original text. Instead, we use text_to_cmp.
        cursor = self.conn.execute('''
            SELECT * FROM warnings
            WHERE file = ?
                AND text_to_cmp = ?
                AND name = ?
                AND email = ?
                AND new = 1;''',
            (warning.file,
             self._get_text_to_cmp(warning.text),
             warning.culprit.name,
             warning.culprit.email
            )
        )
        return cursor.fetchone() is not None

    def make_all_warnings_old(self):
        self.conn.execute('UPDATE warnings SET new = 0;')

    def reset(self):
        self.conn.execute('DELETE FROM warnings;')
