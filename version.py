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

def git_version(abbrev=False):
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
    if abbrev == True:
        abbrev_str = "--abbrev=0"
    else:
        abbrev_str = "--abbrev=1"
    try:
        with open('/dev/null', 'w') as devnull:
            return subprocess.check_output( ["git", "describe", "--tags", abbrev_str]
                                          , stderr=devnull
                                          ).rstrip('\n')
    except subprocess.CalledProcessError:
        return None







__version__ = '0.2'


if git_version() != None:
    __version__ = git_version()


