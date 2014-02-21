# -*- coding: utf-8 -*-

import re
from datetime import datetime
import email.utils

from tools.logger import Debug, Info, Warn, Error


class MailedAction(object):
    def __init__(self
                , subject
                , body
                , attachment_list = None
                , date = None
                ):
        self._subject     = subject
        self._body        = body
        self._attachments = attachment_list
        self._date        = date
        self._ctx_ptn     = re.compile(r" (@\w+)", re.VERBOSE)
    def subject(self):
        return self._subject
    def body(self):
        return self._body
    def context(self):
        return self._ctx_ptn.findall(self._subject)
    def date(self):
        """ returns a datetime object
        .
        The current implementation of date() uses a workaround,
        because the %z directive of datetime is not recognized:
        http://bugs.python.org/issue6641
        http://www.beyondlinux.com/2012/02/06/how-to-convert-string-with-timezone-info-to-date-in-python/
        """
        return datetime(*email.utils.parsedate_tz(self._date)[:6])
    def attachments(self):
        """
        returns the list of attachment filenames
        """
        return self._attachments


def MailedMain():
    a = MailedAction( "description @context @context2"
                    , """body
                         multilined
                      """
                    , "Wed, 19 Feb 2014 16:12:13 +0100"
                    , ["att1.txt", "att2.txt"]
                    )
    print a.subject()
    print a.body()
    print a.context()
    print a.date()
    a._subject = "s"
    print a.context()


if __name__ == '__main__':
    MailedMain()
