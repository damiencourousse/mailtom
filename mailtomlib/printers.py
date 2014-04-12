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


import ConfigParser
import mailers
from pytools.logger import Debug, Info, Error


class MailToOrgMode(object):
    """
    Reads an instance from MailedAction,
    returns a text buffer as a suitable input for org-mode
    """
    def process(self, mail):
        Debug("==== processing mail : %s" % mail.subject())
        msg = u""

        # == task headline
        msg += u"* INACTIVE " + mail.subject()
        # add contexts
        if mail.context() != []:
            msg += " :"
            msg += ":".join(mail.context())
            msg += ":"
        msg += u"\n"

        # add deadline info
        deadline = mail.deadline()
        if deadline is not None:
            msg += u"  DEADLINE: <"  + deadline.strftime('%Y-%m-%d %b.') + ">\n"

        # add scheduled info
        scheduled = mail.scheduled()
        if scheduled is not None:
            msg += u"  SCHEDULED: <"  + scheduled.strftime('%Y-%m-%d %b.') + ">\n"

        # create task drawer with creation date info
        msg += u"  :PROPERTIES:\n"
        msg += u"  :CREATED: ["  + mail.date().strftime('%Y-%m-%d %b. %H:%M') + "]\n"
        # topic
        #msg += u"  :CATEGORY:"  + action.topic() + "\n"
        msg += u"  :END:\n"

        # == task data
        msg += u"   - Note taken on [%s] \\\\\n" % mail.date().strftime('%Y-%m-%d %b. %H:%M')
        if mail.attachments() != []:
            msg += u"   - Fichiers joints: \n"
            for a in mail.attachments():
                msg += u"     [[file:" + a + "]]\n"
        msg += mail.body()
        msg += u"\n"

        return msg.encode('utf-8')

