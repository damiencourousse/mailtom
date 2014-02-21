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
"""Reusable logging configuration.

FIXME

GTG modules and plugins that wish to use logging should import the Log object:

  from tools.logger import Log

...and target it with debug or info messages:

  Log.debug('Something has gone terribly wrong!')

"""
from os import path, environ, getcwd
import logging
import logging.config

CFG_LIST = [ path.join(environ['HOME'], '.mailtom_logging.cfg')
           , path.join(getcwd(), "logging.cfg")
           ]

class Debug_logger(object):
    """Singleton class that acts as interface for GTG's logger"""

    def __init__ (self):
        """ Configure the logger """

        #If we already have a logger, we keep that
        if not hasattr(Debug_logger, "__logger"):
            self.__init_logger()
        #Shouldn't be needed, but the following line makes sure that
        # this is a Singleton.
        self.__dict__['_Debug__logger'] = Debug_logger.__logger
        self.debugging_mode = False

    def __init_logger(self):
        # load config file
        cfg = self.__find_config_file(CFG_LIST)

        # print ("config file for logging : %s" % cfg)
        logging.config.fileConfig(cfg)
        Debug_logger.__logger = logging.getLogger("main")

    def __getattr__(self, attr):
        """ Delegates to the real logger """
        return getattr(Debug_logger.__logger, attr)

    def __setattr__(self, attr, value):
        """ Delegates to the real logger """
        return setattr(Debug_logger.__logger, attr, value)

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
