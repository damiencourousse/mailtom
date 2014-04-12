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
