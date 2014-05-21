#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Loads the output from the doxygen program, parses it to obtain a list of
warnings, and sends emails to users who have introduced the warning."""

import sys
import sqlite3
from getpass import getpass
from smtplib import SMTP
from smtplib import SMTP_SSL

from doxygen_whiner.args import parse as parse_args
from doxygen_whiner.config import parse as parse_config
from doxygen_whiner.io import read_file
from doxygen_whiner.io import read_stdin
from doxygen_whiner.warning import parse_warnings
from doxygen_whiner.warning import group_by_culprit
from doxygen_whiner.git import create_warning_with_culprit
from doxygen_whiner.email import create_email
from doxygen_whiner.db import Database


def main(argc, argv):
    args = parse_args(argv)
    config = parse_config("config.ini", "config.local.ini")

    if args.file:
        text = read_file(args.file)
    else:
        text = read_stdin()

    warnings = parse_warnings(text)
    warnings_with_culprit = map(create_warning_with_culprit, warnings)

    with sqlite3.connect(config['db']['path']) as db_conn:
        db = Database(db_conn)
        warnings_with_culprit = filter(lambda w: not db.has_warning(w),
            warnings_with_culprit)
        db.make_all_warnings_old()

        server = config['email']['server'] or input('Email server: ')
        port = config['email']['port'] or input('Email server port: ')
        use_ssl = config['email'].getboolean('use_ssl')
        username = config['email']['username'] or input('Email server username: ')
        password = config['email']['password'] or getpass('Email server password: ')

        from_addr = config['email']['from'] or input('From address: ')
        subject = config['email']['subject']
        to_addr = config['email']['to']
        reply_to_addr = config['email']['reply_to']

        SMTPServer = SMTP_SSL if use_ssl else SMTP
        with SMTPServer(server, port) as smtp_server:
            smtp_server.login(username, password)
            for culprit, warnings in group_by_culprit(warnings_with_culprit):
                email = create_email(culprit, warnings, from_addr, subject,
                    to_addr=to_addr, reply_to_addr=reply_to_addr)
                smtp_server.send_message(email)
                for w in warnings:
                    db.insert_warning(w)


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
