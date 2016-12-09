# -*- coding: utf-8 -*-
import calendar
import locale

DB_URI = 'mysql+pymysql://mysql:ef5793f4772cfe5a@202.120.40.20:11266/guozijian'
SQLITE_URI = 'sqlite:///db/guozijian.db'
PER_PAGE = 10

locale.setlocale(locale.LC_ALL, "chinese")
__cal__ = calendar.Calendar(firstweekday=calendar.MONDAY)
__days__ = __cal__.iterweekdays()
WEEKDAYS = [(day, calendar.day_name[day].decode(locale.getpreferredencoding())) for day in __days__]
WEEKDAY_MAP = dict(WEEKDAYS)
ENCODING = locale.getpreferredencoding()
