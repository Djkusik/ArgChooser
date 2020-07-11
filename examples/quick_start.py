from argchoose import ArgChooser


def foo():
    print('bar')


ac = ArgChooser()
ac.add_argument('-f', '--foo', method=foo)
ac.execute()