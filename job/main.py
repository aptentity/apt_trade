import schedule
from futu import *
import select_plate
import stock_filter
import second_wave


def day_job():
    try:
        stock_filter.overfall()
    finally:
        print("day_job done")


def short_job():
    stock_filter.select_operation()
    stock_filter.ema_king_cross_tip()
    stock_filter.ema_death_cross_tip()
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
long_job()
short_job()
schedule.every(60).minutes.do(long_job)
schedule.every(10).minutes.do(short_job)
schedule.every().day.at("14:45").do(day_job)

while True:
    schedule.run_pending()
    time.sleep(10)
