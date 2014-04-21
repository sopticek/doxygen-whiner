#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Unit tests for the args module."""

from io import StringIO
import re
import unittest

from doxygen_whiner import args
from .utils import Redirect

PROG_NAME = "doxygen-whiner"

class TestArgsParse(unittest.TestCase):
    def test_if_no_arguments_are_given_file_is_set_to_none(self):
        parsed_args = args.parse([PROG_NAME])
        self.assertEqual(parsed_args.file, None)

    def test_if_file_is_given_file_is_set_to_file(self):
        file = "tmp/text"
        parsed_args = args.parse([PROG_NAME, file])
        self.assertEqual(parsed_args.file, file)

    def scenario_parse_args_exits(self, argv):
        with self.assertRaises(SystemExit) as cm:
            stdout = StringIO()
            stderr = StringIO()
            with Redirect(stdout=stdout, stderr=stderr):
                parsed_args = args.parse(argv)
        return (stdout.getvalue(), stderr.getvalue(), cm.exception.code)

    def scenario_help_is_printed_if_help_arg_is_given(self, help_arg):
        stdout_text, stderr_text, exit_code = self.scenario_parse_args_exits(
            [PROG_NAME, help_arg])
        help_regex = re.compile("^usage: {}.*(?!error:).*$".format(PROG_NAME),
            re.DOTALL)
        self.assertRegex(stdout_text, help_regex)
        self.assertEqual(stderr_text, "")
        self.assertEqual(exit_code, 0)

    def test_if_help_is_requested_it_is_printed(self):
        self.scenario_help_is_printed_if_help_arg_is_given("-h")
        self.scenario_help_is_printed_if_help_arg_is_given("--help")

    def scenario_error_is_printed_if_invalid_args_are_given(self, argv):
        stdout_text, stderr_text, exit_code = self.scenario_parse_args_exits(argv)
        error_regex = re.compile("^.*error:.*$", re.DOTALL)
        self.assertRegex(stderr_text, error_regex)
        self.assertEqual(stdout_text, "")
        self.assertNotEqual(exit_code, 0)

    def test_if_invalid_arguments_are_given_error_is_printed(self):
        self.scenario_error_is_printed_if_invalid_args_are_given(
            [PROG_NAME, "test1", "test2"])
        self.scenario_error_is_printed_if_invalid_args_are_given(
            [PROG_NAME, "--skl"])
