"""
    Reusable logging configuration.

    Modules and plugins that wish to use logging should import one of the Info,
    Warn, Debug, Error, Critical objects:

    from tools.logger import Info

    ...and target it with debug or info messages:

    Info('Something has gone wrong!')
"""


import logging
from os import path, environ, getcwd

LOG_FILE = path.join(environ['HOME'], 'python_logging.log')

def __find_file(flist):
    """
        test if the config_entry parameter is a valid config file
        if not, try to find a config file
            * at $HOME/.mailtom_logging.cfg
    """
    for c in flist:
        if path.exists(c):
            print("Using the configuration file for the logger: %s" % c)
            return c

    raise ValueError("Could not find a suitable configuration file for the logger module.\nTried the following files: %s" % flist)


def set_level(loglevel='info'):
    """
    change the logging level for the console.
    http://docs.python.org/2/library/logging.html#logging-levels
    .
    loglevel = {"debug", "info", warning", "error", "critical" }
    """

    global console_h
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.getLogger('').setLevel(numeric_level)
    console_h.setLevel(numeric_level)
    print "new log level = %s" % loglevel
    print "new log level = %d" % numeric_level


def set_logfile(f):
    global file_h, fileformat, dateformat
    print file_h
    if file_h is not None:
        file_h.flush()
        file_h.close()
    logging.getLogger('').removeHandler(file_h)
    print " new logfile : %s" % f
    file_h = logging.FileHandler(filename=f)
    file_h.setFormatter(logging.Formatter(fileformat))
    print logging.DEBUG
    file_h.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(file_h)
    logging.getLogger('').setLevel(logging.DEBUG)
    print " new logfile : done"

# set up logging to file
fileformat    = '%(asctime)s - %(levelname)-8s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
dateformat    = '%m-%d %H:%M'

file_h = None
set_logfile(LOG_FILE)
print file_h

# define a Handler which writes INFO messages or higher to the sys.stderr
console_h = logging.StreamHandler()
console_h.setLevel(logging.INFO)
console_h.setFormatter(logging.Formatter('%(levelname)-8s: %(message)s'))
# add the handler to the root logger
logging.getLogger('').addHandler(console_h)

logger = logging.getLogger('')

#The logger singletons
Debug    = logger.debug
Info     = logger.info
Warn     = logger.warn
Error    = logger.error
Critical = logger.critical
