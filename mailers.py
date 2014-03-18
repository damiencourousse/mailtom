# -*- coding: utf-8 -*-

import ConfigParser
import email
import getpass
import os
import poplib

from actions import MailedAction
from tools.logger import Debug, Info, Warn, Error

def read_fetch_mail_config(config_file, param, default=None,
        method=ConfigParser.SafeConfigParser.get):
    """
    config_file is assumed to be a valid file
    .
    returns: an instance of the SafeConfigParser clas from ConfigParser
    """
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)

    try:
        res = method(config, 'fetch_mail', param)
    except ConfigParser.NoOptionError:
        if default is None:
            raise ValueError(
"""Missing parameter '%s' in the configuration file %s".
Could not continue with a default value""" % (param, config_file))
        else:
            res = default

    Debug(" configuration file : %s" % (config_file))
    Debug(" %s             : %s" % (param, res))
    return res


class Mail(object):
    def __init__(self, subject, body, attachment = None):
        self._subject = subject
        self._body = body
        self._attachment = attachment
        charset = 'utf-8'
        self._msg            = email.MIMEText(body, _charset  = charset)
        self._msg['Subject'] = email.Header(subject, charset)
    def subject(self):
        return self._subject
    def body(self):
        return self._body
    def attachment(self):
        return self._attachment
    def send(self, mailer, dest):
        # Attachments are not handled
        Info("=== sending mail to %s === " % (dest) )
        Info(" [subject] \n%s" % (self.subject()) )
        Info(" [body] \n%s" % (self.body()) )

        self._msg['To']      = dest
        mailer.send(dest, self._msg)


class MailClient(object):
    def __init__(self, config_file):

        self._server  = read_fetch_mail_config(config_file, 'server', 'localhost')
        self._port    = read_fetch_mail_config(config_file, 'port', 110)
        self._user    = read_fetch_mail_config(config_file, 'user', getpass.getuser())

        # self._passwd: do not use getpass.getpass() as the default value,
        # because getpass() would be evaluated, i.e. the user is asked for a
        # password even if there is a valid line in the configuration file.
        self._passwd  = read_fetch_mail_config(config_file, 'passwd', None)

        self._savedir = read_fetch_mail_config(config_file, 'savedir', '/tmp')

        # By default, leaves emails on the server
        self._delete  = read_fetch_mail_config(config_file, 'delete_msg',
                False, ConfigParser.SafeConfigParser.getboolean)

        # methods that will process specific MIME contents
        self._processors = {
                'text/plain' : self.__process_text,
                'text/html' : self.__process_text,
                }

    def fetch(self):
        """
        connects to the mail server,
        saves all attachments in savedir,
        and returns a list of Mail instances
        """
        #self._connection = poplib.POP3_SSL('pop.gmail.com', 995)
        self._connection = poplib.POP3(self._server)
        #self._connection.set_debuglevel(1)
        self._connection.user(self._user)
        if self._passwd is None:
            self._passwd = getpass.getpass()
        self._connection.pass_(self._passwd)

        email_nb, total_bytes = self._connection.stat()
        Debug("{0} emails in the inbox, {1} bytes total".format(email_nb, total_bytes))
        # return is in format: (response, ['mesg_num octets', ...], octets)
        msg_list = self._connection.list()

        mails = list()

        # processing messages
        for i in range(email_nb):
            email_no = i+1
            Debug("=== reading email %d ===" % email_no)

            # return is in format: (response, ['line', ...], octets)
            response = self._connection.retr(email_no)
            raw_message = response[1]

            str_message = email.message_from_string("\n".join(raw_message))
            print type(str_message)
            debug_str = "\n".join((str(str_message).split('\n'))[0:30])
            Debug(debug_str)

            # walk over the message contents
            atts = list()
            mail = dict() # stores email contents; associates the content
                            # parts with its type
            for part in str_message.walk():
                attachments = list()

                content = part.get_content_type()
                Debug("  content type : %s" % content)

                if part.get_content_maintype() == 'multipart':
                    continue

                processor = self._processors.get(content)

                # process part contents
                if processor is not None:
                    if mail.get(content) is not None:
                        raise ValueError("""I have already stored contents of type %s.
                                            I need a new implementation!!! """ % content)
                    mail[content] = processor(part, email_no)
                else:
                    atts.append(self.__process_attachment(part, email_no))

            body = u""
            for k in mail.keys():
                body += mail.get(k)

            Debug("list of attachments for mail #%d: %s" % (email_no, atts))

            subject =  getmailheader(str_message.get('Subject', ''))
            Debug("= subject: %s" % subject)
            mails.append(MailedAction( subject
                                     , body
                                     , atts
                                     , str_message.get('Date')
                                     ))
            if self._delete is True:
                Debug("mark message %d for deletion" % email_no)
                self._connection.dele(email_no)

        self._connection.quit()
        return mails

    def __process_text(self, part, email_no):
        try:
            payload = part.get_payload(decode=True).decode(part.get_content_charset())
            Debug("\n=== mailToOrg debug info <START> ===\n")
            Debug("  charset = %s\n" % part.get_content_charset())
            Debug("=== mailToOrg debug info <END> ===\n")
        except TypeError:
            Warn(part)
            Warn("Could not retrieve mail body for email %d." % email_no)
            payload = "<mail body is missing>"

        #Info(payload)
        return payload

    def __process_attachment(self, part, email_no):
        filename = part.get_filename()
        if not(filename):
            filename = "attachment.txt"

        fullname = os.path.join(self._savedir, filename)
        Debug("  attachment saved to: %s" % fullname)
        if os.path.isfile(fullname):
            Warn("Skipping attachment %s. A file with the same name was found. " % fullname)
        with open(fullname, 'wb') as f:
            data = part.get_payload(decode=True)
            if data is not None:
                f.write(data)
            else:
                Warn("(email %d) Could not retrieve attachment %s" % (email_no, fullname))

        return fullname

def getmailheader(header_text, default="ascii"):
    """
    Decode header_text if needed
    Source: Alain Spineux (pyzmail) -- http://blog.magiksys.net/parsing-email-using-python-content
    """
    try:
        headers=email.Header.decode_header(header_text)
    except email.Errors.HeaderParseError:
        # This already append in email.base64mime.decode()
        # instead return a sanitized ascii string
        # this faile '=?UTF-8?B?15HXmdeh15jXqNeVINeY15DXpteUINeTJ9eV16jXlSDXkdeg15XXldeUINem15PXpywg15TXptei16bXldei15nXnSDXqdecINek15zXmdeZ?==?UTF-8?B?157XldeR15nXnCwg157Xldek16Ig157Xl9eV15wg15HXodeV15bXnyDXk9ec15DXnCDXldeh15gg157Xl9eR16rXldeqINep15wg15HXmdeQ?==?UTF-8?B?15zXmNeZ?='
        return header_text.encode('ascii', 'replace').decode('ascii')
    else:
        for i, (text, charset) in enumerate(headers):
            try:
                headers[i]=unicode(text, charset or default, errors='replace')
            except LookupError:
                # if the charset is unknown, force default
                headers[i]=unicode(text, default, errors='replace')
        return u"".join(headers)


def fetch_test():
    d=MailClient()
    d.fetch()


if __name__ == '__main__':
    fetch_test()

