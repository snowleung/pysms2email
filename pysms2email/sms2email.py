#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Work at python2.5, iphone4(ios6) with cydia, using hotmail to send the message.
'''

import sqlite3 as sql
import email
import os
import sys
import codecs
import string
import datetime
from Queue import Queue
import time
import threading
import pymail


EMAIL_CONTENT = '''Author:${author}\nTEXT:\n${text}\n${date}\n\n\n'''


reload(sys)
sys.setdefaultencoding('utf8')
streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)


UPDATE_DATE = -1
UPDATE_CHECK_SECONDS = 30

mq = Queue()


class SMSDBMonitor(object):

    def __init__(self):
        self.SMSDB_PATH = '/var/mobile/Library/SMS/sms.db'
        self.SQL_QUERY_TEMPLATE = string.Template(
            '''select date, hd.id, text from message as msg, handle as hd where msg.handle_id=hd.rowid and date>${date} order by msg.date desc limit 10''')
        # sql index
        # date=0
        # author=1
        # text=2
        self.SMSDB = sql.connect(self.SMSDB_PATH)
        self.SMSDB_CURSOR = self.SMSDB.cursor()

    def fetch_update(self, date):
        self.SMSDB_CURSOR.execute(self.SQL_QUERY_TEMPLATE.safe_substitute(date=date))
        return self.SMSDB_CURSOR.fetchall()

    def fetch_recent_history(self, num=2):
        self.SMSDB_CURSOR.execute(
            '''select date, hd.id, text from message as msg, handle as hd where msg.handle_id=hd.rowid order by msg.date desc limit ''' + str(num))
        return self.SMSDB_CURSOR.fetchall()


def message_date(mac_time):
    '''see: http://stackoverflow.com/questions/10746562/parsing-date-field-of-iphone-sms-file-from-backup
    '''
    unix_time = int(mac_time) + 978307200
    date = datetime.datetime.fromtimestamp(unix_time)
    return date


def build_content(message_data):
    msg_body = ''
    for m in message_data:
        _body = string.Template(EMAIL_CONTENT)
        msg_body += _body.safe_substitute(author=str(m[1]), text=m[2], date=message_date(m[0]))
    return msg_body


class ThreadEmailSender(threading.Thread):

    def __init__(self, _queue, _sender):
        threading.Thread.__init__(self)
        self.queue = _queue
        self.sender = _sender

    def run(self):
        while(True):
            item = self.queue.get()
            if item:
                self.sender.send_mail('SMS on IPhone4', item)
            time.sleep(2)


def run_diagnostic(init_diagnostic_file_path='./diagnostic'):
    content = None
    if os.path.exists(init_diagnostic_file_path):
        f = open(init_diagnostic_file_path, 'r')
        content = f.read()
        f.close()
    return content


if __name__ == '__main__':
    mail = pymail.Pymail(os.environ.get('USER_MAIL'), os.environ.get('USER_PASSWD'), os.environ.get('MAIL_TO'))
    t = ThreadEmailSender(mq, mail)
    t.setDaemon(True)
    t.start()
    print 'worker emailsender is OK'
    smsdb_monitor = SMSDBMonitor()
    init_diagnostic_file_path = './.diagnostic'
    while(1):
        diag_content = run_diagnostic(init_diagnostic_file_path)
        if diag_content:
            mq.put(str(diag_content))
            os.remove(init_diagnostic_file_path)
        if UPDATE_DATE > 0:
            message_data = smsdb_monitor.fetch_update(UPDATE_DATE)
            if message_data:
                UPDATE_DATE = int(message_data[0][0])
                msg_body = build_content(message_data)
                mq.put(msg_body)
        else:
            # INIT
            message_data = smsdb_monitor.fetch_recent_history()
            UPDATE_DATE = int(message_data[0][0])
            msg_body = build_content(message_data)
            mq.put('init OK, SMS monitor is running. recent messge is \n' + msg_body)
        time.sleep(UPDATE_CHECK_SECONDS)
