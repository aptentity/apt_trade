import time

from utils import futuUtils as fu
from utils import time_utils as tu
from futu import *
from utils import signal_utils as su
from utils import dingding as dd
import pandas as pd


def select_object_from_etf(fun):
    print('call select_object_from_etf', fun)
    selectName = []
    selectCode = []
    etf = pd.read_csv('../object/etf_new.csv')
    for row in etf.itertuples():
        code = str(getattr(row, 'code'))
        if not code.__contains__('.'):
            code = 'SH.' + code if code.startswith('5') else 'SZ.' + code
        if fun(code):
            selectCode.append(code)
            selectName.append(getattr(row, 'name'))
    print(selectName)
    print(selectCode)
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])


def select_object_from_my_select(fun):
    print('call select_object_from_my_select', fun)
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security("全部")
    if ret == RET_OK:
        for row in data.itertuples():
            if fun(getattr(row, 'code')):
                selectCode.append(getattr(row, 'code'))
                selectName.append(getattr(row, 'name'))
    print(selectName)
    print(selectCode)
    return selectCode


def select_object_from_my(fun):
    print('call select_object_from_my', fun)
    allCode = []
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security("全部")
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            allCode.append(code)
            if fun(getattr(row, 'code')):
                selectCode.append(getattr(row, 'code'))
                selectName.append(getattr(row, 'name'))

    stock = pd.read_csv('../object/stock.csv')
    for row in stock.itertuples():
        code = str(getattr(row, 'code'))
        if not code.__contains__('.'):
            code = 'SH.' + code if code.startswith('5') else 'SZ.' + code
        if code in allCode:
            print(code)
        else:
            allCode.append(code)
            if fun(code):
                selectCode.append(code)
                selectName.append(getattr(row, 'name'))
    print(selectName)
    print(selectCode)
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])


def select_plate(fun):
    print('call select_plate', fun)
    group_name = '板块'
    resultCode = []
    resultName = []

    fu.delete_user_security(group_name)
    ret, data = fu.quote_context.get_plate_list(Market.SH, Plate.ALL)
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            if fun(code):
                resultCode.append(code)
                resultName.append(getattr(row, 'plate_name'))
    print(resultName)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])


def select_object_from_plate(fun, plates=None):
    def get_from_plate(plate_in):
        print('get_from_plate', plate_in)
        ret, data = fu.quote_context.get_plate_stock(plate_in)
        if ret == RET_OK:
            for row in data.itertuples():
                code = getattr(row, 'code')
                if code in allCode:
                    print(code)
                else:
                    allCode.append(code)
                    print('-------------', code)
                    if fun(code):
                        selectCode.append(code)
                        selectName.append(getattr(row, 'stock_name'))
        else:
            print(plate, data)

    print('call select_object_from_plate', fun)
    allCode = []
    selectName = []
    selectCode = []
    plate = pd.read_csv('../object/plate.csv')
    plate_list = plate[plate['enable'] != 'n']
    for plate in plate_list['code']:
        get_from_plate(plate)
    if plates:
        for plate in plates:
            get_from_plate(plate)

    print(selectName)
    print(selectCode)
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])


def select_object_from_yesterday_limit(n_start, n_end, fun, name='超短'):
    print('call select_object_from_yesterday_limit', fun)
    allCode = []
    selectCode = []
    selectName = []
    object_list = pd.read_csv('../object/yesterday_limit.csv', index_col=0)
    object_list = object_list[(object_list['day'] >= tu.getdate(n_start)) & (object_list['day'] <= tu.getdate(n_end))]
    for row in object_list.itertuples():
        code = getattr(row, 'code')
        if code in allCode:
            print(code)
        else:
            allCode.append(code)
            if fun(code):
                selectCode.append(code)
                selectName.append(getattr(row, 'stock_name'))
    print(selectCode)
    print(selectName)
    fu.quote_context.modify_user_security(name, ModifyUserSecurityOp.ADD, selectCode[::-1])
    return selectCode


def get_hot_plate():
    print('call get_hot_plate')
    plate_list = pd.read_csv('../object/yesterday_limit_plate.csv', index_col=0)
    plate_list = plate_list[plate_list['day'] >= tu.getdate(10)]
    vc = plate_list['plate_code'].value_counts()
    return vc.head().index.tolist()


def select_object_from_hot_plate(fun):
    print('call select_object_from_yesterday_limit', fun)
    plate_list = pd.read_csv('../object/yesterday_limit_plate.csv', index_col=0)
    vc = plate_list['plate_code'].value_counts()
    return select_object_from_plate_list(vc.head().index.tolist(), fun)


def select_object_from_plate_list(plates, fun):
    print('call select_object_from_plate', plates, fun)
    allCode = []
    selectName = []
    selectCode = []
    for plate in plates:
        ret, data = fu.quote_context.get_plate_stock(plate)
        if ret == RET_OK:
            for row in data.itertuples():
                code = getattr(row, 'code')
                if code in allCode:
                    print(code)
                else:
                    allCode.append(code)
                    print('-------------', code)
                    if fun(code):
                        selectCode.append(code)
                        selectName.append(getattr(row, 'stock_name'))
        else:
            print(plate, data)
    print(selectName)
    print(selectCode)
    return selectCode


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

# print(filter_base())
# print(get_hot_plate())