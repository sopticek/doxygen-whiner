#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@protonmail.com
# Date:     2014-05-09
#

"""Unit tests for the utils module."""

import unittest

from doxygen_whiner.utils import TypeCheckedAttribute


class WithAttributes:
    str_attr = TypeCheckedAttribute('str_attr', str)
    int_attr = TypeCheckedAttribute('int_attr', int)

    def __init__(self, str_attr, int_attr):
        self.str_attr = str_attr
        self.int_attr = int_attr


class TestTypeCheckedAttribute(unittest.TestCase):
    def test_types_are_correct(self):
        attrs = WithAttributes('string', 15)
        self.assertEqual(attrs.str_attr, 'string')
        self.assertEqual(attrs.int_attr, 15)

    def test_str_type_is_incorrect(self):
        self.assertRaises(TypeError, WithAttributes, 15, 15)

    def test_int_type_is_incorrect(self):
        self.assertRaises(TypeError, WithAttributes, 'string', 15.5)

    def test_add_attribute_to_descriptor(self):
        WithAttributes.str_attr.new = 5
        self.assertEqual(WithAttributes.str_attr.new, 5)
