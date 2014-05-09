#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Representation and parsing of warnings."""

import re

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


def parse_warnings(text):
    warnings = []
    warning_re = re.compile(r'^(.*):(\d+): warning: (.*)$')

    for line in text.split('\n'):
        match = warning_re.match(line)
        if match:
            file, line, text = match.groups()
            warnings.append(Warning(file, int(line), text))

    return warnings
