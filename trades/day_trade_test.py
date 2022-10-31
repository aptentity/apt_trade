import logging
from utils import futuUtils as fu
from utils import signal_utils as su
from futu import *
import datetime
import time


def day_trade_signal(signal_input):
    # 计算5、20、base
    ema5 = su.get_EMA(signal_input['close'], 5)
    ema20 = su.get_EMA(signal_input['close'], 20)
    ema30 = su.get_EMA(signal_input['close'], 30)
    ema72 = su.get_EMA(signal_input['close'], 72)
    base = (ema30 + ema72) / 2

    # 5与20金叉
    if ema5.iloc[-1] > ema20.iloc[-1] > base.iloc[-1] and (
            ema5.iloc[-2] < ema20.iloc[-2] or su.macd_king_cross(signal_input['close'])):
        for i in range(50):
            if ema20.iloc[-i] < base.iloc[-i]:  # 找到20与base的金叉
                logging.info('买入：' + signal_input.iloc[-1]['time_key'] + ':' + str(signal_input.iloc[-1]['close']))
                return 1
    # 5与20死叉
    elif ema5.iloc[-1] < ema20.iloc[-1] < base.iloc[-1] and (
            ema5.iloc[-2] > ema20.iloc[-2] or su.macd_death_cross(signal_input['close'])):
        for i in range(50):
            if ema20.iloc[-i] > base.iloc[-i]:  # 找到20与base的死叉
                logging.info('卖出：' + signal_input.iloc[-1]['time_key'] + ':' + str(signal_input.iloc[-1]['close']))
                return 2
    return 0


def need_cut_loss(cost, high, close):
    high = high if high > cost else cost
    print('need_cut_loss:' + 'cost=' + str(cost) + ";high=" + str(high) + ";close=" + str(close))
    if (high - cost) / cost < 0.03:
        if (high - close) / cost > 0.03:
            logging.info('need_cut_loss 亏损3%，卖出')
            return True
    elif (high - cost) / cost < 0.05:
        if (close - cost) / cost < 0.005:
            logging.info('need_cut_loss 平价，卖出')
            return True
    elif close - cost < (high - cost) / 2:
        logging.info('need_cut_loss 回撤达到一半，卖出')
        return True
    return False


logging.basicConfig(level=logging.INFO,
                    filename='./day_trade_test_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
hold_price = 0
high = 0
for i in range(1000):
    time.sleep(1)
    startTime = (datetime.datetime.strptime('2022-06-14 00:00:00', "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        minutes=3 * i)).strftime("%Y-%m-%d %H:%M:%S")
    endTime = (datetime.datetime.strptime('2022-06-21 04:00:00', "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
        minutes=3 * i)).strftime("%Y-%m-%d %H:%M:%S")

    ret, data, page_req_key = fu.quote_context.request_history_kline('US.LABU', start=startTime,
                                                                     end=endTime,
                                                                     ktype=KLType.K_3M, autype=AuType.QFQ,
                                                                     max_count=10000, extended_time=True)

    if ret != RET_OK:
        logging.info('request_history_kline error---' + data)
    elif hold_price == 0:
        print(data)
        if day_trade_signal(data) == 1:
            logging.info('buy')
            hold_price = data.iloc[-1]['close']
            high = hold_price
    else:
        high = max(high, data.iloc[-1]['close'])
        if need_cut_loss(hold_price, high, data.iloc[-1]['close']) or day_trade_signal(data) == 2:
            logging.info('sell at ' + str(data.iloc[-1]['close']) + "  " + str(data.iloc[-1]['close'] - hold_price))
            hold_price = 0

strTime = '2022-06-11 11:03:00'
strTime = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")
print((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
print((strTime + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))
print('All pages are finished!')
