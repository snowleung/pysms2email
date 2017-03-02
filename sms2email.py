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
SMSDB_PATH = '/var/mobile/Library/SMS/sms.db'
SQL_QUERY_TEMPLATE = string.Template(
    '''select date, hd.id, text from message as msg, handle as hd where msg.handle_id=hd.rowid and date>${date} order by msg.date desc limit 10''')
# sql index
# date=0
# author=1
# text=2

SMSDB = sql.connect(SMSDB_PATH)
SMSDB_CURSOR = SMSDB.cursor()
mail = pymail.Pymail(os.environ.get('USER_MAIL'), os.environ.get('USER_PASSWD'), os.environ.get('MAIL_TO'))
mq = Queue()


def email_sender():
    '''worker
    '''
    item = mq.get()
    if item:
        mail.send_mail('SMS on IPhone4', msg_body)
    mq.task_done()


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


if __name__ == '__main__':
    print 'worker sender is OK'
    while(1):
        if UPDATE_DATE > 0:
            SMSDB_CURSOR.execute(SQL_QUERY_TEMPLATE.safe_substitute(date=UPDATE_DATE))
            message_data = SMSDB_CURSOR.fetchall()
            if message_data:
                UPDATE_DATE = int(message_data[0][0])
                msg_body = build_content(message_data)
                mq.put(msg_body)
                t = threading.Thread(target=email_sender)
                t.daemon = True
                t.start()
                time.sleep(UPDATE_CHECK_SECONDS)
        else:
            # INIT
            SMSDB_CURSOR.execute('''select date, hd.id, text from message as msg, handle as hd where msg.handle_id=hd.rowid order by msg.date desc limit 2''')
            message_data = SMSDB_CURSOR.fetchall()
            UPDATE_DATE = int(message_data[0][0])
            msg_body = build_content(message_data)
            mail.send_mail('SMS Monitor', 'init OK, SMS monitor has is running. recent messge is \n' + msg_body)
