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

    subject = pd.concat([etf[etf['status'] > 2], stock[stock['status'] > 2]])
    subject.to_csv('../object/subject.csv')

    print('check_status_end')


# check_status()

def filter_base():
    simple_filter = SimpleFilter()
    simple_filter.filter_min = 1 * 100000000
    simple_filter.filter_max = 8000 * 100000000
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
    simple_filter3.filter_min = 1
    simple_filter3.filter_max = 150
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

    custom_filter_day = CustomIndicatorFilter()
    custom_filter_day.ktype = KLType.K_DAY
    custom_filter_day.stock_field1 = StockField.EMA20
    custom_filter_day.stock_field2 = StockField.EMA60
    custom_filter_day.relative_position = RelativePosition.MORE
    custom_filter_day.is_no_filter = False

    custom_filter_week = CustomIndicatorFilter()
    custom_filter_week.ktype = KLType.K_WEEK
    custom_filter_week.stock_field1 = StockField.EMA10
    custom_filter_week.stock_field2 = StockField.EMA60
    custom_filter_week.relative_position = RelativePosition.MORE
    custom_filter_week.is_no_filter = False

    resultName = []
    resultCode = []
    nBegin = 0
    last_page = False
    ret_list = list()
    while not last_page:
        nBegin += len(ret_list)
        ret, ls = fu.quote_context.get_stock_filter(market=Market.HK,
                                                    # plate_code=plate,
                                                    filter_list=[custom_filter_day, custom_filter_week],
                                                    begin=nBegin)
        if ret == RET_OK:
            last_page, all_count, ret_list = ls
            print('all count = ', all_count)
            for item in ret_list:
                resultName.append(item.stock_name)
                resultCode.append(item.stock_code)
        else:
            print('error: ', ls)
            time.sleep(30)
    print(resultName)
    print(resultCode)
    return resultName