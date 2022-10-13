import datetime


def between_time():
    # 范围时间
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '21:30', '%Y-%m-%d%H:%M')
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '22:30', '%Y-%m-%d%H:%M')

    # 当前时间
    n_time = datetime.datetime.now()
    print(n_time)
    print(d_time)
    print(d_time1)
    # 判断当前时间是否在范围时间内
    if d_time < n_time < d_time1:
        return True
    else:
        return False


print(between_time())
