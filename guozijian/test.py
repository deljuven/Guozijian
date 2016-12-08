import calendar

if __name__ == '__main__':
    # test = json.loads("[1,2,3]")
    # print json.dumps(test)
    # parse = {"name": "hello", "head": 1}
    # print json.dumps(parse)
    # date_test = datetime.datetime.strptime("8:09", "%H:%M")
    # date_test2 = datetime.datetime.strptime("18:09", "%H:%M")
    # print date_test.time().strftime("%H:%M")
    # print date_test2.time().strftime("%H:%M")
    # print date_test2.time()
    # print date_test2 < date_test

    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    days = cal.iterweekdays()
    # for day in days:
    #     print calendar.day_name[day]
    choices = [(day, calendar.day_name[day]) for day in days]
    print choices
