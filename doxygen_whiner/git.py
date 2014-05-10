#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-10
#

"""Interface to git."""

import re
import os
import subprocess

from .utils import TypeCheckedAttribute
from .warning import Warning


class Person:
    name = TypeCheckedAttribute('name', str)
    email = TypeCheckedAttribute('email', str)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email

    def __ne__(self, other):
        return not self == other


class WarningWithCulprit(Warning):
    def __init__(self, warning, culprit):
        self.__dict__.update(warning.__dict__)
        self.culprit = culprit


def create_warning_with_culprit(warning):
    current_dir = os.getcwd()
    os.chdir(warning.dir)

    git_output = subprocess.check_output([
        'git', 'blame', warning.file,
        '-L', '{0},{0}'.format(warning.line),
        '--porcelain'])
    git_output = git_output.decode('utf-8')

    name_re = re.compile(r'^author (.*)$', re.MULTILINE)
    email_re = re.compile(r'^author-mail <(.*)>$', re.MULTILINE)
    name = name_re.search(git_output).group(1)
    email = email_re.search(git_output).group(1)

    os.chdir(current_dir)

    return WarningWithCulprit(warning, Person(name, email))
