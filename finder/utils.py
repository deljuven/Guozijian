# -*- coding: utf-8 -*-
import calendar
import locale
import os

import configparser

# DB_URI = 'mysql+pymysql://mysql:ef5793f4772cfe5a@202.120.40.20:11266/finder'
SQLITE_URI = 'sqlite:///db/finder.db'

if os.name is 'nt':
    locale.setlocale(locale.LC_ALL, "chinese")
else:
    locale.setlocale(locale.LC_ALL, "zh_CN.utf8")
__cal__ = calendar.Calendar(firstweekday=calendar.MONDAY)
__days__ = __cal__.iterweekdays()
WEEKDAYS = [(day, calendar.day_name[day].decode(locale.getpreferredencoding())) for day in __days__]
WEEKDAY_MAP = dict(WEEKDAYS)
ENCODING = locale.getpreferredencoding()

config = configparser.ConfigParser()
config.read_file(open('config.cfg'))
RETRY = config['DEFAULT']['RetryNumber']
INTERVAL = config['DEFAULT']['TimeInterval']
