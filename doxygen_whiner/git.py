#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Author:   Daniela Ďuričeková, daniela.duricekova@protonmail.com
# Date:     2014-05-10
#

"""Interface to git."""

import re
import os
import subprocess

from .warning import Person
from .warning import WarningWithCulprit


class GitError(Exception):
    pass


def create_warning_with_culprit(warning):
    '''Creates WarningWithCulprit from the given warning.

    It detects the culprit by running `git blame` on warning.file.

    In the following situations, GitError is raised:
    - warning.file_name does not exist in warning.dir
    - git is not installed
    - warning.line does not exist in warning.file
    '''
    current_dir = os.getcwd()

    try:
        os.chdir(warning.dir)
        git_output = subprocess.check_output([
            'git', 'blame', warning.file_name,
            '-L', '{0},{0}'.format(warning.line),
            '--porcelain'], stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        # Either git is not installed or warning.file does not exist.
        raise GitError(str(e))
    except subprocess.CalledProcessError as e:
        # Error of the form:
        #
        # Command 'xxx' returned non-zero exit status N.
        raise GitError(e.output.decode('utf-8'))
    finally:
        os.chdir(current_dir)

    git_output = git_output.decode('utf-8')

    name_re = re.compile(r'^author (.*)$', re.MULTILINE)
    email_re = re.compile(r'^author-mail <(.*)>$', re.MULTILINE)
    name = name_re.search(git_output).group(1)
    email = email_re.search(git_output).group(1)

    return WarningWithCulprit(warning, Person(name, email))
