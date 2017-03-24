#!/usr/bin/python
# coding:utf-8

import logging
import logging.config
import os

logging.config.fileConfig(os.path.join(os.path.split(__file__)[0], 'simplelog.cfg'))
logger_pysms2email = logging.getLogger('pysms2email')
logger_pysms2email.info('logging init OK')
