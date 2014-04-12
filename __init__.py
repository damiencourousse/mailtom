# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Damien Couroussé <damien.courousse@gmail.com>
#
# This file is part of pytools.
#
# pytools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pytools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pytools.  If not, see <http://www.gnu.org/licenses/>.
#


from logger import Info, Debug, Warn, Error, Critical
import logger
from os import path, environ, getcwd

def main():
    print "main: START"

    Debug    ( "debug msg    -- ceci est un test" )
    Info     ( "info msg     -- ceci est un test" )
    Warn     ( "warn msg     -- ceci est un test" )
    Error    ( "error msg    -- ceci est un test" )
    Critical ( "critical msg -- ceci est un test" )

    print "========"

    logger.set_level("debug")
    Debug    ( "debug msg    -- ceci est un test" )
    Info     ( "info msg     -- ceci est un test" )
    Warn     ( "warn msg     -- ceci est un test" )
    Error    ( "error msg    -- ceci est un test" )
    Critical ( "critical msg -- ceci est un test" )

    print "========"

    logger.set_logfile(path.join(getcwd(), "output.log"))
    Debug    ( "debug msg    -- ceci est un test" )
    Info     ( "info msg     -- ceci est un test" )
    Warn     ( "warn msg     -- ceci est un test" )
    Error    ( "error msg    -- ceci est un test" )
    Critical ( "critical msg -- ceci est un test" )

    print "========"

    logger.set_level("warning")
    Debug    ( "debug msg    -- ceci est un test" )
    Info     ( "info msg     -- ceci est un test" )
    Warn     ( "warn msg     -- ceci est un test" )
    Error    ( "error msg    -- ceci est un test" )
    Critical ( "critical msg -- ceci est un test" )
    print "main: END"

if __name__ == '__main__':
    main()
