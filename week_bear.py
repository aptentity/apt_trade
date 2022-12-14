# 短线超卖
# 15分钟跌破CB1，在1分钟金叉后，选择向上趋势或者震荡中，不能选择下跌趋势
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def week_bear():
    print('week_bear doing')
    tips = '1、涨幅较大，需要注意减仓\n' \

    group_name = '周空'

    fu.clear_user_security(group_name)

    # 取出列表
    ret, data = fu.quote_context.get_user_security('特别关注')
    if ret == RET_OK:
        print(data)

    resultCode = []
    resultName = []
    for row in data.itertuples():
        code = getattr(row, 'code')
        print(code)
        fu.quote_context.subscribe(code, SubType.K_WEEK)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_WEEK)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=20)
            try:
                if ema20.iloc[-1] * 1.25 < data['high'].iloc[-1]:
                    print(row)
                    resultName.append(getattr(row, 'name'))
                    resultCode.append(code)
            except:
                print('error')
        else:
            print('error:', data)
    print(resultName)
    if resultName:
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
        # dd.send_week_bear(tips + '\n' + ';'.join(resultName))
    return '周线级别涨幅较大：' + ';'.join(resultName)
