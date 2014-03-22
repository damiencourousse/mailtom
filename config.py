# -*- coding: utf-8 -*-

import ConfigParser

from os import path, environ
from tools.logger import Debug, Info, Warn, Error

DEFAULT_CFG = path.join(environ['HOME'], '.mailtom.cfg')

def find_config_file(self, config_entry = DEFAULT_CFG):
    """
        test if the config_entry parameter is a valid config file
        if not, try to find a config file
            * at $HOME/.mailtom.cfg
    """
    if config_entry is None:
        config_entry = DEFAULT_CFG

    Debug("config_entry = %s" % config_entry)
    if (path.exists(config_entry)):
        Info("Using configuration file %s " % config_entry)
        return config_entry

    # fallback: no config file found
    raise ValueError("ERROR! no suitable config file found")
    return None # we should never land here


def read_param(config_file, section, param, default=None,
        method=ConfigParser.SafeConfigParser.get):
    """
    config_file is assumed to be a valid file
    .
    returns: an instance of the SafeConfigParser clas from ConfigParser
    """
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)

    try:
        res = method(config, section, param)
    except ConfigParser.NoOptionError:
        if default is None:
            Error("Missing parameter '%s' (section '%s') in the configuration file %s"
                    % (param, section, config_file))
            Error("Could not continue with a default value")
            raise ValueError("missing parameter in %s" % config_file)
        else:
            res = default

    Debug(" configuration file : %s" % (config_file))
    Debug(" %s             : %s" % (param, res))
    return res

