# -*- coding: utf-8 -*-
import calendar
import json
import locale
import time

from datetime import datetime

from utils import WEEKDAY_MAP

if __name__ == '__main__':
    print dict(name="1", begin=2, end=3, days_of_week=[3, 5], total=6)

    origin = [u'1', u'2', u'3']
    print json.dumps([0, 3])
    print "***********************"
    test = json.dumps(origin)
    print test
    res = [t.encode('ascii') for t in origin]
    print res
    print json.dumps(res)
    # parse = {"name": "hello", "head": 1}
    # print json.dumps(parse)
    # date_test = datetime.datetime.strptime("8:09", "%H:%M")
    # date_test2 = datetime.datetime.strptime("18:09", "%H:%M")
    # print date_test.time().strftime("%H:%M")
    # print date_test2.time().strftime("%H:%M")
    # print date_test2.time()
    # print date_test2 < date_test

    locale.setlocale(locale.LC_ALL, "chinese")

    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    days = cal.iterweekdays()
    choices = [(day, calendar.day_name[day].decode("gbk").encode("utf8")) for day in days]
    print choices[0][1]
    map_ = dict(choices)
    print map(lambda x: map_[x], json.loads("[1,2,3,4,5]"))
    print map(lambda x: WEEKDAY_MAP[x], json.loads("[1,2,3,4,5]"))
    print map(lambda x: WEEKDAY_MAP[x].encode("utf8"), json.loads("[1,2,3,4,5]"))

    begin = time.strptime("09:00", "%H:%M")
    end = time.strptime("10:00", "%H:%M")
    print begin < end
    test = "test"
    print "%%%s%%" % test
    d = datetime.fromtimestamp(1481448907.636)
    print d
