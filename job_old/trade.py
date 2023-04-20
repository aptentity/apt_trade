import time
import schedule

from trades import short_sell
from utils import futuUtils as fu


def trade_job():
    if fu.is_us_normal_trading_time():
        short_sell.short_sell_by_code('US.SOXL', 100)
        short_sell.short_sell_by_code('US.SOXS', 100)
        # short_sell.short_sell_by_code('US.LABU', 100)
        # short_sell.short_sell_by_code('US.LABD', 100)


trade_job()
schedule.every(1).minutes.do(trade_job)

while True:
    print("while")
    schedule.run_pending()
    time.sleep(5)
