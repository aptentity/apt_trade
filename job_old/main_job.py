import schedule
from futu import *
import stock_filter
from job_old import second_wave


def day_job():
    try:
        stock_filter.select_etf()
        stock_filter.select_object_in_trend()
        stock_filter.overfall()
        stock_filter.select_stock_day_trend()
    finally:
        print("day_job done")


def short_job():
    stock_filter.select_up_and_down()
    stock_filter.buy_tip()
    stock_filter.sell_tip()
    print("short_job done")


def long_job():
    stock_filter.select_my()
    stock_filter.select_focus()
    second_wave.stock_second_wave()
    second_wave.plate_second_wave()
    print('long_job done')


logging.basicConfig(level=logging.INFO,
                    filename='./main_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
# long_job()
schedule.every(15).minutes.do(short_job)
schedule.every().day.at("14:40").do(day_job)

while True:
    schedule.run_pending()
    time.sleep(10)
