# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Gettings Things Gnome! - a personal organizer for the GNOME desktop
# Copyright (c) 2008-2009 - Lionel Dricot & Bertrand Rousseau
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

# FIXME modifier le cartouche, laisser les auteurs d'origine
# -----------------------------------------------------------------------------
"""
    Reusable logging configuration.

    Modules and plugins that wish to use logging should import one of the Info,
    Warn, Debug, Error, Critical objects:

    from tools.logger import Info

    ...and target it with debug or info messages:

    Info('Something has gone wrong!')
"""

from os import path, environ, getcwd
import logging
import logging.config

CFG_LIST = [ path.join(environ['HOME'], '.python_logging.cfg')
           , path.join(getcwd(), "logging.cfg")
           ]

class Debug_logger(object):
    """Singleton class that acts a standalone configurable logger"""

    def __init__ (self):
        """ Configure the logger """

        print "< logger init"
        #If we already have a logger, we keep that
        if not hasattr(Debug_logger, "__logger"):
            print "< logger init: has no __logger attribute"
            self.__init_logger()
        #Shouldn't be needed, but the following line makes sure that
        # this is a Singleton.
        self.__dict__['_Debug__logger'] = Debug_logger.__logger
        self.debugging_mode = False

    def __init_logger(self):
        Debug_logger.__logger = logging.getLogger('main')
        # set a stream handler for debugging
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - " +
                                      "%(module)s:%(funcName)s:%(lineno)d - " +
                                      "%(message)s")
        ch.setFormatter(formatter)
        Debug_logger.__logger.addHandler(ch)

    def __getattr__(self, attr):
        """ Delegates to the real logger """
        return getattr(Debug_logger.__logger, attr)

    def __setattr__(self, attr, value):
        """ Delegates to the real logger """
        return setattr(Debug_logger.__logger, attr, value)

    def set_config(self, cfg_list):
        print "< set_config"
        cfg = self.__find_config_file(cfg_list)
        logging.config.fileConfig(cfg)
        print Debug_logger.__logger
        ch = logging.getLogger("root")
        Debug_logger.__logger.addHandler(ch)
        print Debug_logger.__logger
        Debug_logger.__logger = logging.getLogger("root")
        print Debug_logger.__logger
        print "- set_config"

    def set_debugging_mode(self, value):
        self.debugging_mode = value
    def is_debugging_mode(self):
        return self.debugging_mode

    def __find_config_file(self, cfg_list):
        """
            test if the config_entry parameter is a valid config file
            if not, try to find a config file
                * at $HOME/.mailtom_logging.cfg
        """
        for c in cfg_list:
            if path.exists(c):
                print("Using the configuration file for the logger: %s" % c)
                return c

        raise ValueError("Could not find a suitable configuration file for the logger module.\nTried the following files: %s" % cfg_list)



#The singleton itself
Debug    = Debug_logger().debug
Info     = Debug_logger().info
Warn     = Debug_logger().warn
Error    = Debug_logger().error
Critical = Debug_logger().critical
