import filter_stock
import short_bear
import short_bull
import trade_notice
import trend_bear
import trend_bull
import schedule
from utils import futuUtils as fu
from report import day_report
from futu import *
import pandas_ta as ta
from utils import dingding as dd
from utils import signal_utils as su
import select_plate


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
        select_plate.select_plate()
        # filter_stock.filter_base()
        # day_report.day_report()
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


def apt_job(group_from='重点', group_to='操作', send_msg=1):
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
            ema20 = ta.ma('ema', data['close'], length=10)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] > base.iloc[-1]:
                if ema20.iloc[-2] < base.iloc[-2]:
                    resultNew.append(getattr(row, 'name'))
                # 判断日线
                fu.quote_context.subscribe(code, SubType.K_DAY)
                ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_DAY)
                if ret == RET_OK:
                    result = su.cal_macd(data['close'])
                    amount = 0
                    for i in range(0, 2):
                        if result.iloc[(-1 - i)] > result.iloc[(-2 - i)]:
                            amount = amount + 1
                    if amount > 0 and min(result.iloc[-1], result.iloc[-2], result.iloc[-3]) < 0:
                        resultName.append(getattr(row, 'name'))
                        resultCode.append(code)
                else:
                    print('get day kline error:', data)

        else:
            print(code, 'error:', data)
    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])
    if resultNew:
        tips = '15分钟金叉：' + ';'.join(resultNew)
        if send_msg == 1 and fu.is_ch_normal_trading_time():
            dd.trend_bull(tips)
        logging.info(tips)

    resultNameSell = []
    # 取出列表
    ret, data = fu.quote_context.get_user_security('特别关注')
    if ret != RET_OK:
        print(data)
        return
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=10)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] < base.iloc[-1] and ema20.iloc[-2] > base.iloc[-2]:
                resultNameSell.append(getattr(row, 'name'))
        else:
            print('error:', data, code)
    if resultNameSell:
        tips = '15分钟死叉：' + ';'.join(resultNameSell)
        if send_msg == 1 and fu.is_ch_normal_trading_time():
            dd.trend_bear(tips)
        logging.info(tips)


def buy_tip():
    # 取出列表
    ret, data = fu.quote_context.get_user_security('操作')
    resultNameBuy = []
    resultCode = []
    group_name = '买点'
    if ret != RET_OK:
        print(data)
        return
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            result = su.cal_macd(data['close'])
            if (result.iloc[-1] > result.iloc[-2] < result.iloc[-3] and result.iloc[-2] > 0) or (
                    result.iloc[-3] < 0 and result.iloc[-1] > result.iloc[-2] > result.iloc[-3] < result.iloc[-4]):
                resultNameBuy.append(getattr(row, 'name'))
                resultCode.append(code)
        else:
            print('error:', data)

    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])
    if resultNameBuy and fu.is_ch_normal_trading_time():
        tips = '买入信号：' + ';'.join(resultNameBuy)
        dd.trend_bull(tips)
        logging.info(tips)


def sell_tip():
    # 取出列表
    ret, data = fu.quote_context.get_user_security('特别关注')
    resultNameSell = []
    resultCode = []
    group_name = '卖点'
    if ret != RET_OK:
        print(data)
        return
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=10)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] < base.iloc[-1]:
                result = su.cal_macd(data['close'])
                if result.iloc[-3] > 0 and result.iloc[-1] < result.iloc[-2] < result.iloc[-3] > result.iloc[-4]:
                    resultNameSell.append(getattr(row, 'name'))
                    resultCode.append(code)
        else:
            print('error:', data)

    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])
    if resultNameSell and fu.is_ch_normal_trading_time():
        tips = '卖出信号：' + ';'.join(resultNameSell)
        dd.trend_bear(tips)
        logging.info(tips)


def my_job():
    apt_job()
    # apt_job('沪深', '重点2', 0)
    buy_tip()
    sell_tip()


logging.basicConfig(level=logging.INFO,
                    filename='./main_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
my_job()
# select_plate.select_plate()
schedule.every(5).minutes.do(my_job)
schedule.every().day.at("14:45").do(day_job)

while True:
    print("while")
    schedule.run_pending()
    time.sleep(5)
