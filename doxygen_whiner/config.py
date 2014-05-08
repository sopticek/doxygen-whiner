#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@gmail.com
# Date:     2014-04-21
#

"""Representation and parsing of configuration files."""

import configparser


def parse(*config_files):
    config = configparser.ConfigParser()
    config.read(config_files)
    return config
