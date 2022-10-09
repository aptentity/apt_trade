"""
选择板块，根据月MACD
"""

from utils import futuUtils as fu
from futu import *
import pandas_ta as ta


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
    fu.quote_context.subscribe(code, SubType.K_MON)
    ret, data = fu.quote_context.get_cur_kline(code, 100, SubType.K_MON)
    if ret != RET_OK:
        print(data)
    else:
        result = cal_macd(data['close'])
        print(result)
        print(result.iloc[-1])
        if result.iloc[-1] > 0:
            print("selected")
            if result.iloc[-2] <= 0:
                return 2
            elif result.iloc[-1] > result.iloc[-2]:
                return 1
    return 0


group_name = '板块'
resultCode = []
resultName = []
crossCode = []
crossName = []

fu.clear_user_security(group_name)
ret, data = fu.quote_context.get_plate_list(Market.SH, Plate.ALL)
if ret == RET_OK:
    for row in data.itertuples():
        code = getattr(row, 'code')
        result = selected(code)
        if result == 1:
            resultCode.append(code)
            resultName.append(getattr(row, 'plate_name'))
        elif result == 2:
            crossCode.append(code)
            crossName.append(getattr(row, 'plate_name'))
else:
    print('error:', data)
print(resultName)
print(crossName)
print((len(resultName) + len(resultCode)) / len(data))
fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)