#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Damien Couroussé <damien.courousse@gmail.com>
#
# This file is part of mailtom.
#
# mailtom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mailtom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mailtom.  If not, see <http://www.gnu.org/licenses/>.
#

import glob, os, sys
from setuptools import setup, find_packages


def determine_path():
    """Borrowed from wxglade.py"""
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print "I'm sorry, but something is wrong."
        print "There is no __file__ variable. Please contact the author."
        sys.exit ()


def determine_version():
    """ invocate git describe in a shell run from the current directory
    .
    this use of git describe will return a complete description of the release
    version number :
        $ git describe --tags
        v0.1-2-gdd4e
    means: 2 commits after v0.1, namely commit gdd4e
    .
    To force a shorter version including only the tag name, we must use
    --abbrev=0
    """
    import subprocess
    return subprocess.check_output(["git", "describe", "--tags", "--abbrev=1"]).rstrip('\n')


# version number
try:
    version = determine_version()
except KeyError:
    version = 'unknown_version'


setup( name             = 'mailtom'
     ,  description      = 'translates emails to org-mode tasks'
     ,  long_description = """
        mailtom is a tool for the creation of org-mode tasks from an email box.
        The purpose is to fill automatically your GTD inbox from the contents
        of a dedicated email box.
        """
     ,  install_requires = []
     ,  license          = 'GPLv3'
     ,  version          = version
     ,  author           = 'Damien Couroussé'
     ,  author_email     = 'damien.courousse@gmail.com'
     ,  platforms        = 'Cross Platform'
     ,  scripts          = ['mailtom']
     ,  packages         = find_packages()
     ,  py_modules       = ['actions', 'config', 'mailers', 'printers']
     ,  ext_modules      = []
    )

