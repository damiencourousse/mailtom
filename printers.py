# -*- coding: utf-8 -*-

import ConfigParser
import mailers
from tools.logger import Debug, Info, Error


class MailToOrgMode(object):
    """
    Reads an instance from MailedAction,
    returns a text buffer as a suitable input for org-mode
    """
    def process(self, mail):
        msg = u""

        # == task headline
        # TODO delete context keywords from the subject string
        # TODO add support for deadlines
        msg += u"* INACTIVE " + mail.subject()
        # add contexts
        if mail.context() != []:
            msg += " :"
            msg += ":".join(mail.context())
            msg += ":"
        msg += u"\n"

        # # deadline, scheduled date
        #if (0 != len(action.due_date())):
            #body += u"  DEADLINE: <"  + action.due_date('%Y-%m-%d %b.') + ">"
            ## do not push a carriage return here, DEADLINE and SCHEDULED are
            ## written on the same body line
        #if action.is_scheduled():
            #body += u"  SCHEDULED: <"  + action.scheduled_date('%Y-%m-%d %b.') + ">"
        #if (0 != len(action.due_date())) or action.is_scheduled():
            #body += u"\n"
        msg += u"  :PROPERTIES:\n"
        msg += u"  :CREATED: ["  + mail.date().strftime('%Y-%m-%d %b. %H:%M') + "]\n"

        # topic
        #body += u"  :CATEGORY:"  + action.topic() + "\n"

        msg += u"  :END:\n"
        # == task data
        msg += u"   - Note taken on [] \\\\\n"
        if mail.attachments() != []:
            msg += u"   - Fichiers joints: \n"
            for a in mail.attachments():
                msg += u"     file:" + a + "\n"
        msg += mail.body()
        msg += u"\n"

        return msg.encode('utf-8')


