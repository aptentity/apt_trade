import datetime
import time


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


# print(between_time())

# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def getdate(beforeOfDay):
    import datetime
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')  # #号可以去除0
    return re_date


def get_today():
    local_time = time.localtime(time.time())  # 获取当前时间的时间元组
    week_index = local_time.tm_wday  # 获取时间元组内的tm_wday值
    if week_index == 6:
        return getdate(2)
    elif week_index == 5:
        return getdate(1)
    else:
        return getdate(0)

