# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Damien Couroussé <damien.courousse@gmail.com>
#
# This file is part of mailtom.
#
# mailtom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mailtom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mailtom.  If not, see <http://www.gnu.org/licenses/>.
#


import datetime
import email.utils
import html2text
import re

from pytools.logger import Debug, Info, Warn, Error


class MailedAction(object):
    def __init__(self
                , subject
                , body
                , attachment_list = None
                , date = None
                ):
        self._known_dl = { 'yyyymmdd'  : self.__process_dl_yyyymmdd
                         , 'yymmdd'    : self.__process_dl_yymmdd
                         , 'mmdd'      : self.__process_dl_mmdd
                         , 'mmslashdd' : self.__process_dl_mmslashdd
                         , 'dd'        : self.__process_dl_dd
                         , 'plus'      : self.__process_dl_plus
                         , 'weeks'     : self.__process_dl_weeks
                         }
        self._subject     = subject
        self._body        = body
        self._attachments = attachment_list
        self._date        = date

        # the space before @ prevents considering postfixes of email adresses
        # as context keywords
        self._ptn_ctx     = re.compile(r" (@\w+)", re.VERBOSE)

        dates_regexes = [ r"(?P<yyyymmdd>\d{8})"             # 8 digits: yyyymmdd
                        , r"(?P<yymmdd>\d{6})"               # 6 digits: yymmdd
                        , r"(?P<mmdd>\d{3,4})"               # 3-4 digits: mmdd
                        , r"(?P<mmslashdd>\d{1,2}\/\d{1,2})" # mm/dd
                        , r"(?P<dd>\d{1,2})"                 # 1-2 digits: dd
                        , r"\+(?P<weeks>\d+)w"               # n weeks from now
                        , r"\+(?P<plus>\d+)d?"               # n days from now
                        ]
        self._ptn_dl = re.compile(r"|".join([r"d:"+d for d in dates_regexes]), re.VERBOSE)
        self._ptn_sl = re.compile(r"|".join([r"s:"+d for d in dates_regexes]), re.VERBOSE)

    def subject(self):
        s = self._subject

        # filter out Re: and Fwd: strings
        # standard prefixes: https://en.wikipedia.org/wiki/List_of_email_subject_abbreviations
        # we first do some cleanup, in order to avoid interpreting fwd:
        # patterns as false positives for deadline info
        subject_prefixes = [ 'Re: '   # filtering is applied case insensitive
                           , 'Re:'
                           , 'Fwd: '
                           , 'Fwd:'
                           , 'Fw: '
                           , 'Fw:'
                           , 'Fyi: '
                           , 'Fyi:'
                           ]
        for i in subject_prefixes:
            s = re.sub(i, '', s, flags=re.I)

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
        """ return the email body
        .
        Filter out the end of the body, starting from the first signature found
        Following Usenet Signature Convention in RFC 3676 (section 4.3)
        https://tools.ietf.org/html/rfc3676#section-4.3
        .
        If html is found, render plain text with the module html2text.
        """
        b = self._body
        if b.startswith("<html>"):
            b = html2text.html2text(b)

        body, sep, sign = b.partition("\n-- \n")
        return (body + "\n")

    def context(self):
        return self._ptn_ctx.findall(self._subject)

    def date(self):
        """ returns a datetime object
        .
        Workaround here:
        because the %z directive of datetime is not recognized:
        http://bugs.python.org/issue6641
        http://www.beyondlinux.com/2012/02/06/how-to-convert-string-with-timezone-info-to-date-in-python/
        """
        return datetime.datetime(*email.utils.parsedate_tz(self._date)[:6])

    def deadline(self):
        return self.__search_date_pattern(self._ptn_dl)

    def scheduled(self):
        return self.__search_date_pattern(self._ptn_sl)

    def __search_date_pattern(self, ptn):
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

    def __process_dl_yyyymmdd(self, date):
        """
        returns a datetime object according to the yyyymmdd pattern matching
        """
        return datetime.datetime.strptime(date, '%Y%m%d')

    def __process_dl_yymmdd(self, date):
        """
        returns a datetime object according to the yymmdd pattern matching
        """
        return datetime.datetime.strptime(date, '%y%m%d')

    def __process_dl_mmdd(self, date):
        """
        returns a datetime object according to the mmdd pattern matching
        """
        thisy = datetime.datetime.today().year
        d = datetime.datetime.strptime(date, '%m%d')
        return datetime.date(thisy, d.month, d.day)

    def __process_dl_mmslashdd(self, date):
        """
        returns a datetime object according to the mmdd pattern matching
        """
        l = date.split('/')
        d = int(l.pop())
        m = int(l.pop())
        thisy = datetime.datetime.today().year
        try:
            date = datetime.date(thisy, m, d)
        except ValueError:
            Warn("Incorrect deadline format. Was reading: %s/%s" % (m, d))
            date = None
        return date

    def __process_dl_dd(self, date):
        """
        returns a datetime object according to the mmdd pattern matching
        """
        thisy = datetime.datetime.today().year
        thism = datetime.datetime.today().month
        day   = datetime.datetime.strptime(date, '%d').day
        return datetime.date(thisy, thism, day)

    def __process_dl_plus(self, date):
        """
        returns a datetime object according to the plus pattern matching
        """
        return self.date() + datetime.timedelta(int(date))

    def __process_dl_weeks(self, date):
        """
        returns a datetime object according to the weeks pattern matching
        """
        return self.date() + datetime.timedelta(0, weeks=int(date))

    def attachments(self):
        """
        returns the list of attachment filenames
        """
        return self._attachments


def MailedMain():
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
    a._subject = "deadline description d:20140302"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:140302"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:0302"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:032"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:04/05"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:04/5"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description s:032"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:02"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description d:2"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline description s:02"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline in three days d:+3"
    print "> deadline: %s" % a.deadline()
    print "> scheduled: %s" % a.scheduled()
    print "################################"
    a._subject = "deadline 2014, march the 3rd d:20140302"
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
