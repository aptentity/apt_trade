"""
日内交易
根据3分钟来操作
1、买点：20和Base金叉之后，5与20金叉
2、卖点-形态：20和Base死叉之后，5与20死叉
3、卖点-止盈：盈利10%
4、卖点-止损：盈利3%之前，亏损3%
5、卖点-回撤：盈利3%之后，不能亏损；盈利5%之后，回撤一半
"""
from utils import futuUtils as fu
from utils import signal_utils as su
from futu import *
import logging
import shelve


# 0，不操作
# 1，买入
# 2，卖出
def day_trade_signal(code):
    fu.quote_context.subscribe(code, SubType.K_3M, extended_time=True)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_3M)
    if ret != RET_OK:
        logging.info('code=' + code + ':' + data)
        return 0

    # 计算5、20、base
    ema5 = su.get_EMA(data['close'], 5)
    ema20 = su.get_EMA(data['close'], 20)
    ema30 = su.get_EMA(data['close'], 30)
    ema72 = su.get_EMA(data['close'], 72)
    base = (ema30 + ema72) / 2

    # 5与20金叉
    if ema5.iloc[-1] > ema20.iloc[-1] > base.iloc[-1] and (
            ema5.iloc[-2] < ema20.iloc[-2] or su.macd_king_cross(data['close'])):
        for i in range(50):
            if ema20.iloc[-i] < base.iloc[-i]:  # 找到20与base的金叉
                logging.info('买入：' + data.iloc[-1]['time_key'] + ':' + str(data.iloc[-1]['close']))
                return 1
    # 5与20死叉
    elif ema5.iloc[-1] < ema20.iloc[-1] < base.iloc[-1] and (
            ema5.iloc[-2] > ema20.iloc[-2] or su.macd_death_cross(data['close'])):
        for i in range(50):
            if ema20.iloc[-i] > base.iloc[-i]:  # 找到20与base的死叉
                logging.info('卖出：' + data.iloc[-1]['time_key'] + ':' + str(data.iloc[-1]['close']))
                return 2
    return 0


def is_hold_stock(code_input):
    ret, data = fu.trade_us_context.position_list_query(refresh_cache=True)
    if ret != RET_OK:
        logging.info(data)

    for row in data.itertuples():
        code = getattr(row, 'code')
        if getattr(row, 'qty') > 1 and code == code_input:  # 持仓
            return True, row
    return False, 'no holding data'


def need_cut_loss(cost, high, close):
    high = high if high > cost else cost
    print('need_cut_loss:' + 'cost=' + str(cost) + ";high=" + str(high) + ";close=" + str(close))
    if (high - cost) / cost < 0.03:
        if (high - close) / cost > 0.03:
            logging.info('need_cut_loss 亏损3%，卖出')
            return True
    elif (high - cost) / cost < 0.05:
        if (close - cost) / cost < 0.01:
            logging.info('need_cut_loss 平价，卖出')
            return True
    elif close - cost < (high - cost) / 2:
        logging.info('need_cut_loss 回撤达到一半，卖出')
        return True
    return False


def get_high(code):
    s = shelve.open('day_trade_high.txt', flag='c')
    high = 0
    try:
        high = s[code]
    except:
        high = 0
    finally:
        s.close()
        return high


def set_high(code, high):
    s = shelve.open('day_trade_high.txt', flag='c')
    s[code] = high
    s.close()


def day_trade(code, count):
    logging.basicConfig(level=logging.INFO,
                        filename='./day_trade_log.txt',
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')

    # code_array = ['US.LABD', 'US.LABU']
    # num = {'US.LABD': 100, 'US.LABU': 500}
    fu.unlock_trade()

    ret, data = is_hold_stock(code)
    if ret:  # 持有
        print('hold')
        if fu.is_sell_trading_time(code):
            return
        high = get_high(code)
        print(high)
        print(getattr(data, 'cost_price'))
        print(getattr(data, 'nominal_price'))
        high = max([high, getattr(data, 'cost_price'), getattr(data, 'nominal_price')])
        print(high)
        set_high(code, high)
        if need_cut_loss(getattr(data, 'cost_price'), high, getattr(data, 'nominal_price')) or day_trade_signal(
                code) == 2:
            fu.get_trade_context(code).place_order(price=getattr(data, 'nominal_price'),
                                                   qty=getattr(data, 'qty'), code=code,
                                                   trd_side=TrdSide.SELL,
                                                   trd_env=TrdEnv.REAL, order_type=OrderType.MARKET)
            set_high(code, 0)

    elif fu.is_buy_trading_time(code) and day_trade_signal(code) == 1:  # 不持有
        print('buy')
        fu.get_trade_context(code).place_order(price=1, qty=count, code=code, trd_side=TrdSide.BUY, trd_env=TrdEnv.REAL,
                                               order_type=OrderType.MARKET)


# print(day_trade('US.SOXL', 100))
# print('done')
