#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Representation and parsing of warnings."""

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
