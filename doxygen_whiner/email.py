#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-13
#

"""Creation and sending of emails."""

from email.mime.text import MIMEText


def create_email(culprit, warnings, from_addr, subject, *,
        to_addr=None, reply_to_addr=None):
    body = '''Dear {},

you were identified as the author of the code lines on which doxygen reported the following warnings:

{}

Please, correct them (if you haven't already done so).

    Your Doxygen Whiner
'''.format(culprit.name, '\n'.join(w.original_data for w in warnings))

    email = MIMEText(body)
    email['Subject'] = subject
    email['From'] = from_addr
    email['To'] = culprit.email if not to_addr else to_addr

    if reply_to_addr:
        email['Reply-To'] = reply_to_addr

    return email
