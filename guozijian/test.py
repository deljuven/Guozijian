# -*- coding: utf-8 -*-


class Test:
    def __init__(self, name, value, warning=50, interval=5):
        self.name = name
        self.value = value
        self.interval = interval
        self.warning = warning

    def __repr__(self):
        return '<Test %r>' % {'name': self.name, 'value': self.value, 'warning': self.warning,
                              'interval': self.interval}


def test(a=1, b=2, c=3):
    print (a, b, c)


if __name__ == '__main__':
    pass
    # print dict(name="1", begin=2, end=3, days_of_week=[3, 5], total=6)
    #
    # origin = [u'1', u'2', u'3']
    # print json.dumps([0, 3])
    # print "***********************"
    # print [datetime.min] * 3
    # test = json.dumps(origin)
    # print test
    # res = [t.encode('ascii') for t in origin]
    # print res
    # print json.dumps(res)
    # parse = {"name": "hello", "head": 1}
    # print json.dumps(parse)
    # date_test = datetime.datetime.strptime("8:09", "%H:%M")
    # date_test2 = datetime.datetime.strptime("18:09", "%H:%M")
    # print date_test.time().strftime("%H:%M")
    # print date_test2.time().strftime("%H:%M")
    # print date_test2.time()
    # print date_test2 < date_test
    # print Test(1, 2, 3)
    # print MSG_TYPE[WARN_LEVEL]
    # print "%d < %d x %d%%" % (10, 20, 50)
    args = [11, 22, 33]
    kwargs = {'a': -1, 'b': -2, 'c': -3}
    test(**kwargs)
