# coding:utf-8

import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class Pymail(object):

    def __init__(self, _user, _passw, _tolist, _smtp_host='smtp-mail.outlook.com', _smtp_port=587):
        self._user = _user
        self._passw = _passw
        self._fromaddr = self._user
        self._tolist = _tolist.split(',')
        self._smtp_host = _smtp_host
        self._smtp_port = _smtp_port
        self._server = None
        
    def _login(self):
        self._clean()
        self._server = smtplib.SMTP()
        self._server.connect(self._smtp_host, self._smtp_port)
        self._server.ehlo()
        self._server.starttls()
        self._server.ehlo()
        #self._server.set_debuglevel(1)
        self._server.login(self._user, self._passw)

    def _clean(self):
        if self._server:
            self._server.close()
            self._server = None

    def send_mail(self, sub, text):
        self._login()
        msg = email.MIMEMultipart.MIMEMultipart()
        msg['From'] = self._fromaddr
        msg['To'] = email.Utils.COMMASPACE.join(self._tolist)
        msg['Subject'] = sub
        msg.attach(MIMEText(text))
        msg.attach(MIMEText('\nsent via python', 'plain'))
        self._server.sendmail(self._user, self._tolist, msg.as_string())
        print 'mail it!'
        self._clean()


if __name__ == '__main__':
    import datetime
    import os
    hotmail = Pymail(os.environ.get('USER_MAIL'), os.environ.get('USER_PASSWD'), os.environ.get('MAIL_TO'))
    hotmail.send_mail('test', 'test_messge'+str(datetime.datetime.now()))
