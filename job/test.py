from utils import futuUtils as fu
from futu import *
import pandas as pd
from job_old import stock_filter
from strategy import object_filter
from strategy import filter_strategy


def add_all():
    selectCode = []
    etf = pd.read_csv('../object/etf_new.csv')
    stock = pd.read_csv('../object/stock.csv')
    new_list = etf  # pd.concat([etf, stock])
    for row in new_list.itertuples():
        code = str(getattr(row, 'code'))
        if not code.__contains__('.'):
            code = 'SH.' + code if code.startswith('5') else 'SZ.' + code
        selectCode.append(code)
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])


print(object_filter.select_from_subject_good(filter_strategy.is_day_start_up))
# add_all()
# stock_filter.select_object_in_trend()
# fu.quote_context.subscribe('SZ.000001', SubType.K_DAY)
# ret, data = fu.quote_context.get_cur_kline('SZ.000001', 1000, SubType.K_DAY)
# print(data)
# print(data['turnover'].iloc[-1] / (
#                 (data['turnover'].iloc[-2] + data['turnover'].iloc[-3] + data['turnover'].iloc[-4]) / 3))


# ret, data = fu.quote_context.get_owner_plate(['HK.00001', 'SZ.002291', 'SZ.002315'])
# if ret == RET_OK:
#     print(data)
#     print(data['code'][0])  # 取第一条的股票代码
#     print(data['plate_code'].values.tolist())  # 板块代码转为 list
# else:
#     print('error:', data)

# ret, data = fu.quote_context.get_plate_stock('SH.BK0250')
# if ret == RET_OK:
#     print(data)
