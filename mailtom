#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sys import stdout
from optparse import OptionParser

import mailers
import actions
import printers

import config
from tools.logger import Debug, Info, Warn, Error

DEFAULT_CFG = os.path.join(os.environ['HOME'], '.mailtom.cfg')


class MailToOrg:
    def __init__(self, options):
        #Debug("config file : %s", options.file)

        # look for a configuration file for gtdToMail - the default is $HOME/.mailtom.cfg
        cfg = config.find_config_file(options.config, DEFAULT_CFG)

        mclient = mailers.MailClient(cfg)

        # build the list of mail objects
        mail_list = mclient.fetch()

        printer = printers.MailToOrgMode()

        # open the destination file if requested, else use stdout
        if options.output is not None:
            f = open(options.output, 'a')
        else:
            f = stdout

        # process mails
        for m in mail_list:
            f.write(printer.process(m))

        Info("%d emails processed" % len(mail_list))

        if options.output is not None:
            f.close()


def main():
    Debug("Debug output enabled.")
    parser = OptionParser()
    parser.add_option("-c", "--config",
            dest="config",
            type = "string",
            help="use the configuration file FILE")
    parser.add_option("-o", "--output",
            dest="output",
            type = "string",
            help="output file")

    (options, args) = parser.parse_args(args=None, values=None)
    Debug( "... options : %s", options)
    Debug( "... args : %s", args)

    orgmail = MailToOrg(options)

    Debug("END")

if __name__ == '__main__':
    main()

