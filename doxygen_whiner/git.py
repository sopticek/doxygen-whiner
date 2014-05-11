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
from io import StringIO

from .utils import TypeCheckedAttribute
from .warning import Warning


class Person:
    name = TypeCheckedAttribute('name', str)
    email = TypeCheckedAttribute('email', str)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return 'Person({!r}, {!r})'.format(self.name, self.email)

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email

    def __ne__(self, other):
        return not self == other


class WarningWithCulprit(Warning):
    def __init__(self, warning, culprit):
        self.__dict__.update(warning.__dict__)
        self.culprit = culprit

    def __repr__(self):
        return 'WarningWithCulprit({}, {!r})'.format(
            super().__repr__(), self.culprit)


class GitError(Exception):
    pass


def create_warning_with_culprit(warning):
    '''Creates WarningWithCulprit from the given warning.

    It detects the culprit by running `git blame` on warning.file.

    In the following situations, GitError is raised:
    - warning.file does not exist
    - git is not installed
    - warning.line does not exist in warning.file
    '''
    current_dir = os.getcwd()

    try:
        os.chdir(warning.dir)
        stderr = StringIO()
        git_output = subprocess.check_output([
            'git', 'blame', warning.file,
            '-L', '{0},{0}'.format(warning.line),
            '--porcelain'], stderr=stderr)
    except FileNotFoundError as e:
        # Either git is not installed or warning.file does not exist.
        raise GitError(str(e))
    except subprocess.CalledProcessError as e:
        # Error of the form:
        #
        # Command 'xxx' returned non-zero exit status N.
        raise GitError(stderr.getvalue())
    finally:
        os.chdir(current_dir)

    git_output = git_output.decode('utf-8')

    name_re = re.compile(r'^author (.*)$', re.MULTILINE)
    email_re = re.compile(r'^author-mail <(.*)>$', re.MULTILINE)
    name = name_re.search(git_output).group(1)
    email = email_re.search(git_output).group(1)

    return WarningWithCulprit(warning, Person(name, email))
