import datetime

import day_bear
import day_bull
import select_plate
import select_stock
import trend_bear
import trend_bull
import week_bear
import week_bull
import time
from utils import dingding as dd

def day_report():
    week_bear_r = week_bear.week_bear()
    time.sleep(10)
    week_bull_r = week_bull.week_bull()
    time.sleep(10)
    day_bear_r = day_bear.day_bear()
    time.sleep(10)
    day_bull_r = day_bull.day_bull()
    time.sleep(10)
    trend_bear_r = trend_bear.trend_bear(0)
    time.sleep(10)
    trend_bull_r = trend_bull.trend_bull(0)
    time.sleep(10)
    select_stock_r = select_stock.selset_stock()
    items = [select_plate.select_plate(),
             select_stock_r,
             week_bear_r,
             week_bull_r,
             day_bear_r,
             day_bull_r,
             trend_bear_r,
             trend_bull_r]
    report = '\n\n' + str(datetime.datetime.now()) + '\n' + '\n'.join(items)
    dd.send_day_bull(report)
    with open('day_report.txt', 'a') as f:
        f.writelines(report)


# day_report()
