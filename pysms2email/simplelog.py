#!/usr/bin/python
# coding:utf-8

import logging
import logging.config

logging.config.fileConfig('./simplelog.cfg')
logger_pysms2email = logging.getLogger('pysms2email')
logger_pysms2email.info('logging init OK')
