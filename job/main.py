import day_bear
import day_bull
import filter_stock
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
from futu import *
import pandas_ta as ta
from utils import dingding as dd


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
        filter_stock.filter_base()
        day_report.day_report()
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


def apt_job(group_from='操作', group_to='重点', send_msg=1):
    if not fu.is_ch_normal_trading_time():
        print('not trading time')
        return
    print('do apt_job')
    group_name = group_to

    # 取出列表
    ret, data = fu.quote_context.get_user_security(group_from)
    if ret != RET_OK:
        print(data)
        return
    # ret1, data1 = fu.quote_context.get_user_security('港股')
    # if ret1 != RET_OK:
    #     print(data1)
    #     return
    # data = data.append(data1)
    print(data)
    resultCode = []
    resultName = []
    resultNew = []
    for row in data.itertuples():
        code = getattr(row, 'code')

        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            # print(data)
            ema20 = ta.ma('ema', data['close'], length=20)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] > base.iloc[-1]:
                resultName.append(getattr(row, 'name'))
                resultCode.append(code)
                if ema20.iloc[-2] < base.iloc[-2]:
                    resultNew.append(getattr(row, 'name'))
        else:
            print('error:', data)
    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])
    if resultNew:
        tips = '15分钟金叉：' + ';'.join(resultNew)
        if send_msg == 1:
            dd.trend_bull(tips)
        logging.info(tips)

    resultNameSell = []
    # 取出列表
    ret, data = fu.quote_context.get_user_security(group_from)
    if ret != RET_OK:
        print(data)
        return
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=20)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] < base.iloc[-1] and ema20.iloc[-2] > base.iloc[-2]:
                resultNameSell.append(getattr(row, 'name'))
        else:
            print('error:', data)
    if resultNameSell:
        tips = '15分钟死叉：' + ';'.join(resultNameSell)
        if send_msg == 1:
            dd.trend_bear(tips)
        logging.info(tips)


def my_job():
    apt_job()
    apt_job('沪深', '重点2', 0)


logging.basicConfig(level=logging.INFO,
                    filename='./main_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
my_job()
schedule.every(5).minutes.do(my_job)

# trend_bear.trend_bear(0)
# trend_bull.trend_bull(0)
# short_job(1)
# day_job()
# schedule.every(5).minutes.do(short_job)
# schedule.every().day.at("14:40").do(day_job)

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
