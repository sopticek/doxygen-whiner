#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-13
#

"""Creation and sending of emails."""

from email.mime.text import MIMEText


def create_email(culprit, warnings, from_addr, subject):
    body = '''Dear {},

you were identified as the author of the code lines on which doxygen reported the following warnings:

{}

Please, correct them (if you haven't already done so).

    Your doxygen-whiner
'''.format(culprit.name, '\n'.join(w.original_data for w in warnings))

    email = MIMEText(body)
    email['Subject'] = subject
    email['From'] = from_addr
    email['To'] = culprit.email
    return email
