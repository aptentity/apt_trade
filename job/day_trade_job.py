import schedule
import time
from trades import day_trade
from utils import futuUtils as fu


def trade_job():
    print('do trade_job')
    day_trade.day_trade('US.LABU', 500, is_buy=False)
    day_trade.day_trade('US.LABD', 200, is_buy=False)
    day_trade.day_trade('HK.07226', 5000, is_buy=False)
    day_trade.day_trade('HK.07552', 1000, is_buy=False)


schedule.every(1).minutes.do(trade_job)

while True:
    schedule.run_pending()
    time.sleep(5)
