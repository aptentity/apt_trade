"""
止损策略
1、盈利3个点之前，回撤5%
2、盈利3个点后，成本
3、盈利5个点之后，回撤一半
"""
from utils import futuUtils as fu
from futu import *
import shelve


def cut_loss():
    fu.unlock_trade()

    s = shelve.open('high.txt', flag='c')
    s1 = shelve.open('high1.txt', flag='c')

    # ret, data = fu.trade_context.position_list_query(refresh_cache=True)
    # if ret == RET_OK:
    #     print(data)
    #     for row in data.itertuples():
    #         deal(row, s, s1)

    ret, data = fu.trade_us_context.position_list_query(refresh_cache=True)
    if ret == RET_OK:
        print(data)
        for row in data.itertuples():
            deal(row, s, s1)

    s.close()
    s1.close()
    try:
        os.remove('high.txt')
        os.rename('high1.txt', 'high.txt')
    finally:
        print('ok')


def deal(row, s, s1):
    # 数量不足
    if getattr(row, 'qty') < 1:
        return

    code = getattr(row, 'code')
    high = 0
    try:
        high = s[code]
        print('hight=' + str(high))
    except:
        print('-----------')
    finally:
        high = high if high > getattr(row, 'nominal_price') else getattr(row, 'nominal_price')
        if need_cut_loss(getattr(row, 'cost_price'), high, getattr(row, 'nominal_price')):
            print('cut loss sell')
            if "US" in code:
                ret, data = fu.trade_us_context.place_order(price=getattr(row, 'nominal_price'),
                                                            qty=getattr(row, 'qty'), code=code, trd_side=TrdSide.SELL,
                                                            trd_env=TrdEnv.REAL, order_type=OrderType.MARKET)
                print(data)
            if "HK" in code:
                ret, data = fu.trade_context.place_order(price=100,
                                                            qty=getattr(row, 'qty'), code=code, trd_side=TrdSide.SELL,
                                                            trd_env=TrdEnv.REAL, order_type=OrderType.NORMAL)
                print(data)
        s1[code] = high


def need_cut_loss(cost, high, close):
    high = high if high > cost else cost
    print('need_cut_loss:' + 'cost=' + str(cost) + ";high=" + str(high) + ";close=" + str(close))
    if (high - cost) / cost < 0.03:
        if (high - close) / cost > 0.05:
            return True
    elif (high - cost) / cost < 0.05:
        if (close - cost) / cost < 0.005:
            return True
    elif close - cost < (high - cost) / 2:
        return True
    return False


cut_loss()
# # True
# print(need_cut_loss(7,5,5))
# print('should true')
# print(need_cut_loss(100, 102, 96))
# print(need_cut_loss(100, 100, 94))
# print(need_cut_loss(100, 104, 100))
# print(need_cut_loss(100, 104, 100.1))
# print(need_cut_loss(100, 107, 103))
#
# # False
# print('should false')
# print(need_cut_loss(100, 102, 101))
# print(need_cut_loss(100, 102, 99.5))
# print(need_cut_loss(100, 104, 101))
# print(need_cut_loss(100, 107, 104))

# fu.quote_context.subscribe(code, SubType.K_3M, extended_time=True)
# ret, data = fu.quote_context.get_cur_kline(code, 10, SubType.K_3M)
