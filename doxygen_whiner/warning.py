#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-05-08
#

"""Representation and parsing of warnings."""


class _TypeCheckedAttribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('{!r} is not of type {}'.format(
                value, self.type))
        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]


class Warning:
    file = _TypeCheckedAttribute('file', str)
    line = _TypeCheckedAttribute('line', int)
    text = _TypeCheckedAttribute('text', str)

    def __init__(self, file, line, text):
        self.file = file
        self.line = line
        self.text = text
