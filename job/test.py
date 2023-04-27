from utils import futuUtils as fu
from futu import *
from utils import signal_utils as su
from utils import dingding as dd
import pandas as pd
import stock_filter


def add_all():
    selectCode = []
    etf = pd.read_csv('../object/etf_new.csv')
    stock = pd.read_csv('../object/stock.csv')
    stock_low = pd.read_csv('../object/stock_low.csv')
    new_list = pd.concat([etf, stock, stock_low])
    for row in new_list.itertuples():
        code = str(getattr(row, 'code'))
        if not code.__contains__('.'):
            code = 'SH.' + code if code.startswith('5') else 'SZ.' + code
        selectCode.append(code)
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])


stock_filter.select_object_in_trend()
