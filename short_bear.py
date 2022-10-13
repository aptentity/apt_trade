# 短线超卖
# 15分钟跌破CB1，在1分钟金叉后，选择向上趋势或者震荡中，不能选择下跌趋势
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def short_bear(grop='特别关注'):
    print('short_bear doing')
    tips = '1、短期内第二次出现就卖出一部分\n' \
           '2、需要等待至少1分钟死叉后卖出\n' \
           '3、涨停股票不用操作\n' \

    group_name = '短线空'

    fu.clear_user_security(group_name)

    # 取出列表
    ret, data = fu.quote_context.get_user_security(grop)
    if ret != RET_OK:
        print(data)

    resultCode = []
    resultName = []
    for row in data.itertuples():
        code = getattr(row, 'code')
        # print(code)
        fu.quote_context.subscribe(code, SubType.K_15M, extended_time=True)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=20)
            if ema20.iloc[-1] * 1.05 < data['high'].iloc[-1]:
                # print(row)
                resultName.append(getattr(row, 'name'))
                resultCode.append(code)
        else:
            print('error:', data)
    print(resultName)
    if resultName:
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
        dd.send_short_bear(tips + '\n' + ';'.join(resultName))
