"""
选股
15分钟金叉
1、底部反弹：长时间下跌后出现
2、上升趋势的下跌
此方法为短线，不可用长期持有，尤其是发送亏损
反复金叉死叉不可操作
看日线，需要在macd绿区
13：30 14：40 收盘前操作
如果不大涨，最多持有两天
跌破前低就卖出
"""

from futu import *
import time
from utils import futuUtils as fu
import pandas_ta as ta
from utils import signal_utils as su


def filter_15_cross(code):
    fu.quote_context.subscribe(code, SubType.K_15M)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
    fu.quote_context.unsubscribe(code, SubType.K_15M)
    if ret == RET_OK:
        ema20 = ta.ma('ema', data['close'], length=20)
        ema30 = ta.ma('ema', data['close'], length=30)
        ema72 = ta.ma('ema', data['close'], length=72)
        base = (ema30 + ema72) / 2
        for i in range(30):
            # 金叉前出现死叉
            if ema20.iloc[-i] < base.iloc[-i] and ema20.iloc[-i - 1] > base.iloc[-i - 1]:
                return False
            if ema20.iloc[-i] > base.iloc[-i] and ema20.iloc[-i - 1] < base.iloc[-i - 1]:
                return True
        return False
    else:
        print(code)
        print(data)
        return False


# 10天
def day_ok(code):
    fu.quote_context.subscribe(code, SubType.K_DAY)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
    fu.quote_context.unsubscribe(code, SubType.K_DAY)
    if ret == RET_OK:
        ema20 = su.get_EMA(data['close'], 20)
        ema30 = su.get_EMA(data['close'], 30)
        ema72 = su.get_EMA(data['close'], 72)
        base = (ema30 + ema72) / 2
        for i in range(10):
            if ema20.iloc[-i] < base.iloc[-i]:
                return False
        return True
    return False


def week_ok(code):
    fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_WEEK)
    fu.quote_context.unsubscribe(code, SubType.K_WEEK)
    if ret == RET_OK:
        ema20 = su.get_EMA(data['close'], 20)
        ema30 = su.get_EMA(data['close'], 30)
        ema72 = su.get_EMA(data['close'], 72)
        base = (ema30 + ema72) / 2
        if ema20.iloc[-1] > base.iloc[-1]:
            return True
    return False


# 富途条件选股
def filter_base():
    simple_filter = SimpleFilter()
    simple_filter.filter_min = 50 * 100000000
    simple_filter.filter_max = 800 * 100000000
    simple_filter.stock_field = StockField.FLOAT_MARKET_VAL
    simple_filter.is_no_filter = False
    # simple_filter.sort = SortDir.ASCEND

    simple_filter2 = SimpleFilter()
    simple_filter2.filter_min = 10
    # simple_filter2.filter_max = 100
    simple_filter2.stock_field = StockField.PE_TTM
    simple_filter2.is_no_filter = False
    simple_filter2.sort = SortDir.ASCEND

    simple_filter3 = SimpleFilter()
    simple_filter3.filter_min = 5
    simple_filter3.filter_max = 200
    simple_filter3.stock_field = StockField.CUR_PRICE
    simple_filter3.is_no_filter = False

    accumulate_filter = AccumulateFilter()
    accumulate_filter.stock_field = StockField.TURNOVER
    accumulate_filter.filter_min = 2000
    accumulate_filter.filter_max = 5000
    accumulate_filter.days = 1

    accumulate_filter2 = AccumulateFilter()
    accumulate_filter2.stock_field = StockField.CHANGE_RATE
    accumulate_filter2.filter_max = 1
    accumulate_filter2.filter_min = -1
    accumulate_filter2.days = 4
    resultName = []
    resultCode = []
    nBegin = 0
    last_page = False
    ret_list = list()
    while not last_page:
        nBegin += len(ret_list)
        ret, ls = fu.quote_context.get_stock_filter(market=Market.SH,
                                                    filter_list=[simple_filter,simple_filter2],
                                                    begin=nBegin)
        if ret == RET_OK:
            last_page, all_count, ret_list = ls
            print('all count = ', all_count)
            for item in ret_list:
                if '银行' in item.stock_name:
                    continue
                if filter_15_cross(item.stock_code) and day_ok(item.stock_code) and week_ok(item.stock_code):
                    print(item.stock_code)  # 取股票代码
                    print(item.stock_name)  # 取股票名称
                    resultName.append(item.stock_name)
                    resultCode.append(item.stock_code)
                # print(item[simple_filter])  # 取 simple_filter 对应的变量值
        else:
            print('error: ', ls)
        time.sleep(1)  # 加入时间间隔，避免触发限频
    group_name = '短线A'
    # fu.delete_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
    return resultName


print(filter_base())
# ret, data = fu.quote_context.get_user_security('沪深')
# if ret == RET_OK:
#     for row in data.itertuples():
#         code = getattr(row, 'code')
#         if filter_15_cross(code):
#             print(getattr(row, 'name'))
# else:
#     print(data)
