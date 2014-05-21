#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-13
#

"""Unit tests for the email module."""

import unittest

from doxygen_whiner.email import create_email
from doxygen_whiner.warning import Person
from doxygen_whiner.warning import Warning
from doxygen_whiner.warning import WarningWithCulprit


class TestCreateEmail(unittest.TestCase):
    def setUp(self):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        self.warn1 = Warning(file, line, text)
        file = '/mnt/data/quick.c'
        line = 89
        text = r'missing parameter'
        self.warn2 = Warning(file, line, text)
        self.culprit = Person('John Little', 'john.little@gmail.com' )
        self.warn_with_culprit1 = WarningWithCulprit(self.warn1, self.culprit)
        self.warn_with_culprit2 = WarningWithCulprit(self.warn2, self.culprit)
        self.from_addr = 'doxygen@gmail.com'
        self.subject = 'Warnings'

    def test_create_email_correctly_create_email(self):
        email = create_email(self.culprit,
            [self.warn_with_culprit1, self.warn_with_culprit2],
            self.from_addr, self.subject)

        self.assertEqual(email['Subject'], self.subject)
        self.assertEqual(email['From'], self.from_addr)
        self.assertEqual(email['To'], self.culprit.email)
        self.assertIsNone(email['Reply-To'])

        self.assertIn(self.warn1.file, email.get_payload())
        self.assertIn(str(self.warn1.line), email.get_payload())
        self.assertIn(self.warn1.text, email.get_payload())

        self.assertIn(self.warn2.file, email.get_payload())
        self.assertIn(str(self.warn2.line), email.get_payload())
        self.assertIn(self.warn2.text, email.get_payload())

    def test_override_to_addr(self):
        to_addr = 'email@email.co.uk'
        email = create_email(self.culprit,
            [self.warn_with_culprit1, self.warn_with_culprit2],
            self.from_addr, self.subject, to_addr=to_addr)

        self.assertEqual(email['To'], to_addr)

    def test_set_reply_to_addr(self):
        reply_to_addr = 'email@email.co.uk'
        email = create_email(self.culprit,
            [self.warn_with_culprit1, self.warn_with_culprit2],
            self.from_addr, self.subject, reply_to_addr=reply_to_addr)

        self.assertEqual(email['Reply-To'], reply_to_addr)
