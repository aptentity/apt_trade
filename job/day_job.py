import schedule
from futu import *
import stock_filter


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


day_job()
logging.basicConfig(level=logging.INFO,
                    filename='./main_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')

schedule.every(15).minutes.do(short_job)
schedule.every().day.at("14:40").do(day_job)

while True:
    schedule.run_pending()
    time.sleep(10)
