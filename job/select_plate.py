"""
选择板块，根据月MACD
"""
import time

from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd
from utils import signal_utils as su


# 获取EMA数据 , cps：close_prices 收盘价集合 days:日期 days=5 5日线
def get_EMA(cps, days):
    emas = cps.copy()  # 创造一个和cps一样大小的集合
    for i in range(len(cps)):
        if i == 0:
            emas[i] = cps[i]
        if i > 0:
            emas[i] = ((days - 1) * emas[i - 1] + 2 * cps[i]) / (days + 1)
    return emas


def cal_macd(close):
    ema12 = get_EMA(close, 12)
    ema26 = get_EMA(close, 26)
    # ema12 = ta.ma('ema', close, length=12)
    # ema26 = ta.ma('ema', close, length=26)
    dif = ema12 - ema26
    dea = get_EMA(dif, 9)
    macd = (dif - dea) * 2
    return macd


def selected(code):
    try:
        fu.quote_context.subscribe(code, SubType.K_WEEK)
        ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
        if ret != RET_OK:
            # print(data, code)
            a = 0
        else:
            ema20 = su.get_EMA(data['close'], 10)
            ema30 = su.get_EMA(data['close'], 30)
            ema72 = su.get_EMA(data['close'], 72)
            base = (ema30 + ema72) / 2
            count = 0
            for i in range(0, 5):
                if base.iloc[-1 - i] > ema20.iloc[-1 - i]:
                    count = count + 1
            if count < 3:
                result = cal_macd(data['close'])
                if result.iloc[-1] > result.iloc[-2] and result.iloc[-2] < 0:
                    # print('select:', code)
                    return 1
            # 超跌
            if data['low'].iloc[-1] < base.iloc[-1] * 0.8:
                return 2
            else:
                print('-------------')
    except Exception as e:
        print('Error:', e, code)
    return 0


def query_subscription():
    ret, data = fu.quote_context.query_subscription()
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)


def select_plate():
    group_name = '板块'
    resultCode = []
    resultName = []
    crossCode = []
    crossName = []

    fu.delete_user_security(group_name)
    ret, data = fu.quote_context.get_plate_list(Market.SH, Plate.ALL)
    print(data)
    if ret == RET_OK:
        count = 0
        for row in data.itertuples():
            count = count + 1
            code = getattr(row, 'code')
            result = selected(code)
            print(code, result)
            if result == 1 or result == 2:
                resultCode.append(code)
                resultName.append(getattr(row, 'plate_name'))

            if count % 300 == 0:
                query_subscription()
                time.sleep(60)
                fu.quote_context.unsubscribe_all()
                query_subscription()
    else:
        print('error:', data)
    print(resultName)
    print(crossName)
    print((len(resultName) + len(crossName)) / len(data))
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])

    time.sleep(60)
    fu.quote_context.unsubscribe_all()

    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security('全部')
    if ret == RET_OK:
        print(data)
        for row in data.itertuples():
            code = getattr(row, 'code')
            result = selected(code)
            if result == 1:
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    fu.quote_context.modify_user_security("重点", ModifyUserSecurityOp.ADD, selectCode[::-1])
    print('select:', selectName)
    tips = '选股：' + ';'.join(selectName)
    dd.send_week_bull(tips)

    return "强势板块：" + str((len(resultName) + len(crossName)) / len(data)) + " :" + ';'.join(resultName)


# query_subscription()
# print(select_plate())
