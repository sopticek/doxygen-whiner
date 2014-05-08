#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Unit tests for the config module."""

import unittest

from doxygen_whiner import config
from .utils import TemporaryFile


class TestConfigParse(unittest.TestCase):
    def test_if_no_files_are_given_empty_config_is_returned(self):
        parsed_config = config.parse()
        self.assertEqual(parsed_config.sections(), [])

    def test_simple_file_is_parsed_correctly(self):
        config_content = '''
        ; Local configuration file for doxygen-whiner.

        [db]
            path = db.sql

        [email]
            server = gmail.com
        '''
        with TemporaryFile(config_content) as cf:
            parsed_config = config.parse(cf.name)
            self.assertEqual(parsed_config.sections(), ['db', 'email'])
            self.assertEqual(parsed_config['db']['path'], 'db.sql')
            self.assertEqual(parsed_config['email']['server'], 'gmail.com')

    def test_two_files_are_parsed_correctly(self):
        global_config_content = '''
        ; Global configuration file for doxygen-whiner.

        [db]
            path = db.sql

        [email]
            server = gmail.com
        '''
        local_config_content = '''
        ; Local configuration file for doxygen-whiner.

        [db]
            path = /var/db/db.sql
            username = beruska
        '''
        with TemporaryFile(global_config_content) as global_cf:
            with TemporaryFile(local_config_content) as local_cf:
                parsed_config = config.parse(global_cf.name, local_cf.name)
                self.assertEqual(parsed_config.sections(), ['db', 'email'])
                self.assertEqual(parsed_config['db']['path'], '/var/db/db.sql')
                self.assertEqual(parsed_config['email']['server'], 'gmail.com')
                self.assertEqual(parsed_config['db']['username'], 'beruska')

