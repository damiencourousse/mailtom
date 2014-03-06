# -*- coding: utf-8 -*-

import re
import datetime
import email.utils

from tools.logger import Debug, Info, Warn, Error


class MailedAction(object):
    def __init__(self
                , subject
                , body
                , attachment_list = None
                , date = None
                ):
        self._known_dl = { 'full8' : self.__process_dl_full8
                         , 'full6' : self.__process_dl_full6
                         , 'plus'  : self.__process_dl_plus
                         , 'weeks' : self.__process_dl_weeks
                         }
        self._subject     = subject
        self._body        = body
        self._attachments = attachment_list
        self._date        = date

        # the space before @ prevents considering postfixes of email adresses
        # as context keywords
        self._ptn_ctx     = re.compile(r" (@\w+)", re.VERBOSE)

        dates_regexes = [ r"(?P<full8>\d{8})"    # 8 digits: yyyymmdd
                        , r"(?P<full6>\d{6})"    # 6 digits: yymmdd
                        , r"\+(?P<weeks>\d+)w"   # n weeks from now
                        , r"\+(?P<plus>\d+)d?"   # n days from now
                        ]
        self._ptn_dl = re.compile(r"|".join([r"d:"+d for d in dates_regexes]), re.VERBOSE)
        self._ptn_sl = re.compile(r"|".join([r"s:"+d for d in dates_regexes]), re.VERBOSE)

    def subject(self):
        s = self._subject

        # filter out contexts from the original subject string
        s = re.sub(self._ptn_ctx, "", s)

        # filter out deadlines
        s = re.sub(self._ptn_dl, "", s)
        if re.search(self._ptn_dl, self._subject) is not None:
            # if deadlines are found in the mail subject, we also need to
            # filter out the 'd:' prefix
            s = re.sub(r"d:", "", s)

        # filter out scheduled info
        s = re.sub(self._ptn_sl, "", s)
        if re.search(self._ptn_sl, self._subject) is not None:
            # if deadlines are found in the mail subject, we also need to
            # filter out the 'd:' prefix
            s = re.sub(r"s:", "", s)
        return s

    def body(self):
        return self._body

    def context(self):
        return self._ptn_ctx.findall(self._subject)

    def date(self):
        """ returns a datetime object
        .
        The current implementation of date() uses a workaround,
        because the %z directive of datetime is not recognized:
        http://bugs.python.org/issue6641
        http://www.beyondlinux.com/2012/02/06/how-to-convert-string-with-timezone-info-to-date-in-python/
        """
        return datetime.datetime(*email.utils.parsedate_tz(self._date)[:6])

    def deadline(self):
        return self.__search_pattern(self._ptn_dl)

    def scheduled(self):
        return self.__search_pattern(self._ptn_sl)

    def __search_pattern(self, ptn):
        try:
            for k, v in re.search(ptn, self._subject).groupdict().iteritems():
                if v is not None:
                    Debug(" pattern string found: %s" % v)
                    Debug(" matching with: %s" % k)
                    return self._known_dl.get(k)(v)
        except AttributeError:
            # groupdict() returned None
            # if none of the scheduled formats was found, return None
            Debug(" no pattern match found for: %s" % self._subject)
            return None

    def __process_dl_full8(self, date):
        """
        returns a datetime object according to the date8 pattern matching
        """
        return datetime.datetime.strptime(date, '%Y%m%d')

    def __process_dl_full6(self, date):
        """
        returns a datetime object according to the date6 pattern matching
        """
        return datetime.datetime.strptime(date, '%y%m%d')

    def __process_dl_plus(self, date):
        """
        FIXME docstring
        """
        return self.date() + datetime.timedelta(int(date))

    def __process_dl_weeks(self, date):
        """
        FIXME docstring
        """
        return self.date() + datetime.timedelta(0, weeks=int(date))

    def attachments(self):
        """
        returns the list of attachment filenames
        """
        return self._attachments


def MailedMain():
    from email.header import Header
    a = MailedAction("description @context @context2"
                    , """body
                         multilined
                      """
                      , date = " Wed, 05 Mar 2014 23:24:25 +0100"
                      )
    print "################################"
    print a.subject()
    print a.body()
    print a.context()
    print a.date()
    print "################################"
    a._subject = "task description"
    print a.context()
    print "################################"
    a._subject = "deadline description d:140303"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline in three days d:+3"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline 2014, march the 3rd d:20140303"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline in 2 weeks d:+2w"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "scheduled in 2 weeks s:+2w"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "starts tomorrow, due in 1 week d:+1 s:+1w"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "> subject: %s" % a.subject()


if __name__ == '__main__':
    MailedMain()
