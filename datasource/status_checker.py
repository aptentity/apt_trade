#
from utils import futuUtils as fu
from utils import signal_utils as su
from futu import *
import pandas as pd


def sleep_and_retry(data):
    print(data)
    if data == '订阅额度不足':
        time.sleep(60)
        fu.quote_context.unsubscribe_all()


def check_object_status(code):
    print(code)
    code = str(code)
    if code.find('.') == -1:
        code = 'SH.' + code if code.startswith('5') else 'SZ.' + code

    ret, data = fu.quote_context.subscribe(code, SubType.K_WEEK)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_WEEK)
    if ret != RET_OK:
        print(code, data)
        return
    week_status = su.ema_above_base(data['close'])
    ret, data = fu.quote_context.subscribe(code, SubType.K_DAY)
    if ret != RET_OK:
        sleep_and_retry(data)
        fu.quote_context.subscribe(code, SubType.K_DAY)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
    if ret != RET_OK:
        print(code, data)
        return
    day_status = su.ema_above_base2(data['close'], day=20, short=15)
    if ~week_status & ~day_status:
        return 1
    elif ~week_status & day_status:
        return 2
    elif week_status & ~day_status:
        return 3
    elif week_status & day_status:
        return 4


def check_status():
    etf = pd.read_csv('../object/etf_new.csv', index_col=0)
    etf['status'] = (etf['code']).apply(lambda x: check_object_status(x))
    etf.to_csv('../object/etf_new.csv')

    stock = pd.read_csv('../object/stock.csv', index_col=0)
    stock['status'] = (stock['code']).apply(lambda x: check_object_status(x))
    stock.to_csv('../object/stock.csv')

    print('check_status_end')


check_status()