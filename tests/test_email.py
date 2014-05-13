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
    def test_create_email_correctly_create_email(self):
        file = '/mnt/data/error.c'
        line = 45
        text = r'missing argument after \class'
        warn1 = Warning(file, line, text)
        file = '/mnt/data/quick.c'
        line = 89
        text = r'missing parameter'
        warn2 = Warning(file, line, text)
        culprit = Person('John Little', 'john.little@gmail.com' )
        warn_with_culprit1 = WarningWithCulprit(warn1, culprit)
        warn_with_culprit2 = WarningWithCulprit(warn2, culprit)
        from_addr = 'doxygen@gmail.com'
        subject = 'Warnings'
        email = create_email(culprit, [warn_with_culprit1, warn_with_culprit2],
            from_addr, subject)

        self.assertEqual(email['Subject'], subject)
        self.assertEqual(email['From'], from_addr)
        self.assertEqual(email['To'], culprit.email)

        self.assertIn(warn1.file, email.get_payload())
        self.assertIn(str(warn1.line), email.get_payload())
        self.assertIn(warn1.text, email.get_payload())

        self.assertIn(warn2.file, email.get_payload())
        self.assertIn(str(warn2.line), email.get_payload())
        self.assertIn(warn2.text, email.get_payload())
