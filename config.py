# -*- coding: utf-8 -*-

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
        Info("Using the configuration file %s for gtdToMail" % config_entry)
        return config_entry

    # fallback: no config file found
    raise ValueError("ERROR! no suitable config file found")
    return None # we should never land here

