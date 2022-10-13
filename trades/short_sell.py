"""
短线涨幅过大卖出
策略一：一分钟死叉
策略二：15分钟macd向下
策略三：3分钟macd向下
策略四：3分钟macd死叉
9：30-10：30 之间容易激烈回调，使用策略3
其他情况使用策略4
如果突破BT1直接卖出

需要配合止损策略
"""
from utils import futuUtils as fu
from futu import *
from utils import signal_utils as su
from utils import time_utils as tu
from utils import dingding as dd


def short_sell():
    return


def short_sell_by_code(code, amount, real=False):
    fu.quote_context.subscribe(code, SubType.K_15M, extended_time=True)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
    result = False
    if ret == RET_OK:
        ema20 = su.get_EMA(data['close'], 20)
        print(data['high'].iloc[-1])
        print(ema20.iloc[-1])

        if ema20.iloc[-1] * 1.1 < data['high'].iloc[-1]:
            # 直接卖掉
            result = True

        if ema20.iloc[-1] * 1.05 < data['high'].iloc[-1] or ema20.iloc[-2] * 1.05 < data['high'].iloc[-2]:
            # dd.send_short_bear('短期涨幅较大：\n'+code)
            fu.quote_context.subscribe(code, SubType.K_3M, extended_time=True)
            ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_3M)
            if ret == RET_OK:
                if tu.between_time():
                    result = su.macd_down(data['close'])
                else:
                    result = su.macd_death_cross(data['close'])

    if result:
        print('short sell!!!!!!!!!!  ' + code)
        dd.sell_notice('short sell \n' + code)
        if real:
            if "US" in code:
                ret, data = fu.trade_us_context.place_order(price=data['close'].iloc[-1],
                                                            qty=amount, code=code, trd_side=TrdSide.SELL,
                                                            trd_env=TrdEnv.REAL, order_type=OrderType.MARKET)
                print(data)
            if "HK" in code:
                ret, data = fu.trade_context.place_order(price=data['close'].iloc[-1],
                                                         qty=amount, code=code, trd_side=TrdSide.SELL,
                                                         trd_env=TrdEnv.REAL, order_type=OrderType.MARKET)
                print(data)
    return result


# short_sell_by_code('US.SOXS', 100)
