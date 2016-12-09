# -*- coding: utf-8 -*-
import calendar
import json
import locale

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
    print locale.getlocale()
    print locale.locale_alias["zh_cn"]
    print locale.getpreferredencoding()
    print locale.getdefaultlocale()

    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    days = cal.iterweekdays()
    # for day in days:
    #     print calendar.day_name[day]
    choices = [(day, calendar.day_name[day].decode(locale.getpreferredencoding()).encode("utf8")) for day in days]
    print choices[0][1]
