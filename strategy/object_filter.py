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


def select_object_from_plate(fun):
    print('call select_object_from_plate', fun)
    allCode = []
    selectName = []
    selectCode = []
    plate = pd.read_csv('../object/plate.csv')
    plate_list = plate[plate['enable'] != 'n']
    for plate in plate_list['code']:
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
