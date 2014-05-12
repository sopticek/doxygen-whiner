#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Representation and parsing of warnings."""

import re
import os
from functools import total_ordering

from .utils import TypeCheckedAttribute


class Warning:
    file = TypeCheckedAttribute('file', str)
    line = TypeCheckedAttribute('line', int)
    text = TypeCheckedAttribute('text', str)

    def __init__(self, file, line, text):
        self.file = file
        self.line = line
        self.text = text

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Warning({!r}, {}, {!r})'.format(self.file,
            self.line, self.text)

    @property
    def dir(self):
        '''Returns the directory in which the file is located.'''
        return os.path.dirname(self.file)


@total_ordering
class Person:
    name = TypeCheckedAttribute('name', str)
    email = TypeCheckedAttribute('email', str)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return 'Person({!r}, {!r})'.format(self.name, self.email)

    def __eq__(self, other):
        return (self.name, self.email) == (other.name, other.email)

    def __lt__(self, other):
        return (self.name, self.email) < (other.name, other.email)


class WarningWithCulprit(Warning):
    def __init__(self, warning, culprit):
        self.__dict__.update(warning.__dict__)
        self.culprit = culprit

    def __repr__(self):
        return 'WarningWithCulprit({}, {!r})'.format(
            super().__repr__(), self.culprit)


def parse_warnings(text):
    text = text.strip()

    # There may be warnings spanning over multiple lines, like:
    #
    # /src/checking.h:25: warning: the following parameters are not documented:
    #   parameter 'n'
    #   parameter 'm'
    #
    # To handle such warnings, we split the text into lines. Then, we merge
    # lines starting with white space with the previous line. This simplifies
    # the parsing of such warnings later.
    lines = []
    continued_line_re = re.compile(r'[\t ]+')
    for line in text.split('\n'):
        match = continued_line_re.match(line)
        if match:
            lines[-1] += '\n' + line
        else:
            lines.append(line)

    warnings = []
    warning_re = re.compile(r'^(.*):(\d+): warning: (.*)$', re.DOTALL)
    for line in lines:
        match = warning_re.match(line)
        if match:
            file, line, text = match.groups()
            warnings.append(Warning(file, int(line), text))

    return warnings
