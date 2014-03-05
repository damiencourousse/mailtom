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
        Debug("==== processing mail : %s" % mail.subject())
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

        # add deadline info
        deadline = mail.deadline()
        Debug(")) deadline: %s" % deadline)
        if deadline is not None:
            msg += u"  DEADLINE: <"  + deadline.strftime('%Y-%m-%d %b.') + ">\n"

        # add scheduled info
        scheduled = mail.scheduled()
        Debug(")) scheduled: %s "% scheduled)
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
                msg += u"     file:" + a + "\n"
        msg += mail.body()
        msg += u"\n"

        return msg.encode('utf-8')


