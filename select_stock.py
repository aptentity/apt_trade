"""
# 选择标准
1、月MACD大于0
2、周均线20日大于Base
3、日MACD向上
"""
from utils import futuUtils as fu
from futu import *
from utils import signal_utils as su


def selset_stock():
    ret, data = fu.quote_context.get_user_security('沪深')
    if ret != RET_OK:
        print(data)
        return

    resultCode = []
    resultName = []
    for row in data.itertuples():
        code = getattr(row, 'code')

        fu.quote_context.subscribe(code, SubType.K_MON)
        ret, data = fu.quote_context.get_cur_kline(code, 100, SubType.K_MON)
        if ret != RET_OK:
            print(data)
            return
        result = su.cal_macd(data['close'])
        if result.iloc[-1] > 0:
            resultName.append(getattr(row, 'name'))
            resultCode.append(code)

    if resultName:
        group_name = '月A'
        fu.clear_user_security(group_name)
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
    return "月线强势股:" + ';'.join(resultName)

# selset_stock()
