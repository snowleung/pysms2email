#!/usr/bin/python
#coding:utf-8
import sqlite3 as sql
import string
import os

SMSDB_PATH = r'''/var/mobile/Library/SMS/sms.db'''
SMSDB = sql.connect(SMSDB_PATH)
SMSDB.execute("PRAGMA journal_mode = wal")
SMSDB.commit()
SMSDB.execute('''update message set is_read=1 where is_from_me=0 and is_read=0''')
SMSDB.commit()
output = '%i' % SMSDB.total_changes
print output
os.system('say message as read')
