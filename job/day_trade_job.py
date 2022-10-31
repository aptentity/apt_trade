import schedule
import time
from trades import day_trade
from utils import futuUtils as fu


def trade_job():
    print('do trade_job')
    day_trade.day_trade('US.LABU', 500)
    day_trade.day_trade('US.LABD', 200)


schedule.every(1).minutes.do(trade_job)

while True:
    schedule.run_pending()
    time.sleep(5)
