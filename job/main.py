import day_bear
import day_bull
import select_plate
import short_bear
import short_bull
import trade_notice
import trend_bear
import trend_bull
import week_bear
import week_bull
import time
import schedule
from utils import futuUtils as fu
from report import day_report


def short_job(code=0):
    try:
        if code == 1 or fu.is_ch_normal_trading_time():
            print('A..............')
            short_bull.short_bull()
            time.sleep(10)
            short_bear.short_bear()
            time.sleep(10)

            trend_bull.trend_bull(1)
            time.sleep(10)
            trend_bear.trend_bear(1)
            time.sleep(10)

            trade_notice.trade_notice_cn()
            time.sleep(10)
        if code == 1 or fu.is_us_normal_trading_time():
            print('us..............')
            trade_notice.trade_notice_us()
            time.sleep(10)
            short_bear.short_bear('美股')
            time.sleep(10)
    finally:
        print("short job done")


def day_job():
    try:
        day_report()
        # trend_bull.trend_bull(0)
        # time.sleep(10)
        # trend_bear.trend_bear(0)
        # time.sleep(10)
        #
        # week_bull.week_bull()
        # time.sleep(10)
        # week_bear.week_bear()
        # time.sleep(10)
        #
        # day_bull.day_bull()
        # time.sleep(10)
        # day_bear.day_bear()
        # time.sleep(10)
        #
        # select_plate.select_plate()
    finally:
        print("day_job done")


trend_bear.trend_bear(0)
trend_bull.trend_bull(0)
short_job(1)
schedule.every(10).minutes.do(short_job)
schedule.every().day.at("14:45").do(day_job)

while True:
    print("while")
    schedule.run_pending()
    time.sleep(5)

#


# fu.unlock_trade()

# fu.is_normal_trading_time('HK.07226')

# fu.get_holding_position('US.SOXL')

# print(fu.get_ask_and_bid('US.SOXL'))
# quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
# print(quote_ctx.get_market_snapshot('HK.00700'))  # 获取港股 HK.00700 的快照数据
# quote_ctx.close() # 关闭对象，防止连接条数用尽
#
#
# trd_ctx = OpenSecTradeContext(host='127.0.0.1', port=11111)  # 创建交易对象
# print(trd_ctx.place_order(price=500.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE))  # 模拟交易，下单（如果是真实环境交易，在此之前需要先解锁交易密码）
#
# trd_ctx.close()  # 关闭对象，防止连接条数用尽

# ret, data = fu.quote_context.get_user_security_group()
# if ret == RET_OK:
#     print(data)

# ret, data = fu.quote_context.get_user_security('沪深')
# if ret == RET_OK:
#     print(data)
#
# print(data.iloc[0, 0])
#
# for row in data.itertuples():
#     print(row[1])

# fu.quote_context.subscribe(data.iloc[0, 0], SubType.K_15M)
# ret, data = fu.quote_context.get_cur_kline(data.iloc[0, 0], 1000, SubType.K_15M)
# if ret == RET_OK:
#     print('111111111')
#     print(data)
# else:
#     print('error:', data)
