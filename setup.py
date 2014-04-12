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
from distutils.command.install import install

import mailtomlib.version as version

print find_packages()

class InstallVersion(install):

    def run(self):
        version.save_version()
        install.run(self)

setup( name             = 'mailtom'
     , description      = 'translates emails to org-mode tasks'
     , long_description = """
       mailtom creates org-mode tasks from the contents of an email box.
       Considering that email is one of the most accessible and spread
       communication tools, and that most of daily information land in email
       boxes, the purpose of mailtom is to easily create GTD tasks from emails.
       mailtom translates email contents and headers to org-mode tasks.
       """
     , install_requires = []
     , license          = 'GPLv3'
     , version          = version.git_version()
     , author           = 'Damien Couroussé'
     , author_email     = 'damien.courousse@gmail.com'
     , platforms        = 'Cross Platform'
     , scripts          = ['mailtom']
     # TODO mv tools -> mailtomlib/pytools
     , packages         = ['mailtomlib', 'tools']
     , package_data     = {'mailtomlib': ['data/version.txt']}
     , cmdclass         = { 'install': InstallVersion
                          }
     )
