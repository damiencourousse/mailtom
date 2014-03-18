#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Damien Couroussé <damien.courousse@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#from copy import copy
import glob, os, sys
from setuptools import setup, find_packages
#from ez_setup import use_setuptools
#use_setuptools()



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
    """
    import subprocess
    cmd = "git describe --tags"
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    version = res.stdout.read()
    res.stdout.close()

    return version


# VERSION
# version number
# todo use git info
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
     ,  license          = 'CeCILL-B'
     ,  version          = version
     ,  author           = 'Damien Couroussé'
     ,  author_email     = 'damien.courousse@gmail.com'
     ,  platforms        = 'Cross Platform'
     ,  scripts          = ['mailtom']
     ,  packages         = find_packages()
     ,  py_modules       = ['actions', 'config', 'mailers', 'printers']
     ,  ext_modules      = []
    )

