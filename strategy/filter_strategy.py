from utils import futuUtils as fu
from futu import *
from utils import signal_utils as su
from utils import dingding as dd
import pandas as pd


def empty_strategy(code):
    return True


def sleep_and_retry(data):
    print(data)
    if data == '订阅额度不足':
        time.sleep(60)
        fu.quote_context.unsubscribe_all()


def is_in_week_trend_buy(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_WEEK)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_WEEK)

    ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
    if ret != RET_OK:
        print(data)
    return ret == RET_OK and su.qushi_dibu(data['close'])


def is_in_day_week_trend_buy(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_WEEK)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_WEEK)

    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_WEEK)
    if ret != RET_OK:
        print(code, data)
    elif su.ema_above_base(data['close']):
        ret, data = fu.quote_context.subscribe(code, SubType.K_DAY)
        if ret != RET_OK:
            sleep_and_retry(data)
            fu.quote_context.subscribe(code, SubType.K_DAY)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
        if ret != RET_OK:
            print(code, data)
        elif data['close'].iloc[-1] < 150 and \
                su.ema_above_base2(data['close'], day=5, short=20) and \
                (su.macd_up(data['close']) or su.macd_king_cross(data['close'])) and \
                data['close'].iloc[-1] / data['close'].iloc[-2] < 1.07 and \
                data['close'].iloc[-1] / data['close'].iloc[-4] < 1.15 and \
                data['turnover'].iloc[-1] / (
                (data['turnover'].iloc[-2] + data['turnover'].iloc[-3] + data['turnover'].iloc[-4]) / 3) < 2.5:  # 成交量
            return True
    return False


def is_in_day_trend_buy(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_DAY)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_DAY)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
    if ret != RET_OK:
        print(code, data)
    elif data['close'].iloc[-1] < 150 and \
            su.ema_above_base2(data['close'], day=5, short=20) and \
            (su.macd_up(data['close']) or su.macd_king_cross(data['close'])) and \
            data['close'].iloc[-1] / data['close'].iloc[-2] < 1.07 and \
            data['close'].iloc[-1] / data['close'].iloc[-4] < 1.15 and \
            data['turnover'].iloc[-1] / (
            (data['turnover'].iloc[-2] + data['turnover'].iloc[-3] + data['turnover'].iloc[-4]) / 3) < 2.5:  # 成交量
        return True
    return False


def is_in_week_trend(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_WEEK)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
    return ret == RET_OK and su.ema_above_base(data['close'])


def is_week_over_fall(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_WEEK)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
    if ret == RET_OK:
        ema20 = su.get_EMA(data['close'], 20)
        return data['low'].iloc[-1] < ema20.iloc[-1] * 0.8
    else:
        print(data)
    return False


def is_back_low_before(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_WEEK)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 50, SubType.K_WEEK)
    if ret == RET_OK and len(data) > 45:
        if su.macd_up2(data['close']):
            min_low = min(data['close'][len(data) - 45:len(data) - 10])
            min_low_recently = min(data['close'][len(data) - 5:len(data) - 1])
            print(code, min_low, min_low_recently)
            return abs((min_low_recently - min_low) / min_low) < 0.15
    return False


# 超短线
def is_in_short_buy(code):
    ret, data = fu.quote_context.subscribe(code, SubType.K_30M)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_30M)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_30M)
    if ret != RET_OK:
        print(code, data)
    elif su.ema_above_base2(data['close'], day=5, short=20) and \
            (su.macd_up(data['close']) or su.macd_king_cross(data['close'])):
        return True
    elif su.ema_king_cross2(data['close'], 5):
        return True
    return False
