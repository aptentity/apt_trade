import time

from utils import futuUtils as fu
from utils import time_utils as tu
from futu import *
from utils import signal_utils as su
from utils import dingding as dd
import pandas as pd


def select_from_subject_good(fun):
    print('call select_from_subject_good', fun)
    selectName = []
    selectCode = []
    etf = pd.read_csv('../object/subject.csv')
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
    return selectCode


def select_object_from_etf(fun, status=0):
    print('call select_object_from_etf', fun)
    selectName = []
    selectCode = []
    etf = pd.read_csv('../object/etf_new.csv')
    if status != 0:
        etf = etf[etf['status'] == status]
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
    return selectCode


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
    fu.quote_context.modify_user_security('空', ModifyUserSecurityOp.ADD, selectCode[::-1])
    return selectCode


def select_object_from_my(fun, status=0):
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
    if status != 0:
        stock = stock[stock['status'] == status]
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
    group_name = 'ETF'
    resultCode = []
    resultName = []

    fu.delete_user_security(group_name)
    ret, data = fu.quote_context.get_plate_list(Market.SH, Plate.INDUSTRY)
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


# print(filter_base())
# print(get_hot_plate())

