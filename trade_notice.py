from job import select_plate
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def trade_notice(group_name):
    buyCode = []
    buyName = []
    sellCode = []
    sellName = []
    # 取出列表
    ret, data = fu.quote_context.get_user_security(group_name)
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M, extended_time=True)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            # print(data)
            ema5 = ta.ma('ema', data['close'], length=5)
            ema20 = ta.ma('ema', data['close'], length=20)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            # 做多
            if ema20.iloc[-1] > base.iloc[-1]:
                if ema5.iloc[-1] > ema20.iloc[-1] and ema5.iloc[-2] < ema20.iloc[-2]:
                    buyCode.append(code)
                    buyName.append(getattr(row, 'name'))
                else:
                    result = select_plate.cal_macd(data['close'])
                    if result.iloc[-1] > 0 and result.iloc[-2] < 0:
                        buyCode.append(code)
                        buyName.append(getattr(row, 'name'))
            # 卖出
            else:
                if ema5.iloc[-1] < ema20.iloc[-1] and ema5.iloc[-2] > ema20.iloc[-2]:
                    sellCode.append(code)
                    sellName.append(getattr(row, 'name'))
                else:
                    result = select_plate.cal_macd(data['close'])
                    if result.iloc[-1] < 0 and result.iloc[-2] > 0:
                        sellCode.append(code)
                        sellName.append(getattr(row, 'name'))
        else:
            print(code + ':' + getattr(row, 'name'))
            print(data)

    print(buyName)
    print(sellName)

    if buyName and group_name == '美股':
        dd.duy_notice(';\n'.join(buyCode))
    elif buyName:
        dd.duy_notice(';\n'.join(buyName))

    if sellName and group_name == '美股':
        dd.sell_notice(';\n'.join(sellCode))
    elif sellName:
        dd.sell_notice(';\n'.join(sellName))


def trade_notice_cn():
    trade_notice('特别关注')


def trade_notice_us():
    trade_notice('美股')
    # code = 'US.SOXL'
    # fu.quote_context.subscribe(code, SubType.K_15M, extended_time=True)
    # ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
    # print(data)
