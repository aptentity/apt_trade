# 短线超卖
# 15分钟跌破CB1，在1分钟金叉后，选择向上趋势或者震荡中，不能选择下跌趋势
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def day_bull():
    print('day_bull doing')
    tips = '1、日线超跌博反弹，等待日macd向上，标志性k线\n' \

    group_name = '日多'

    fu.clear_user_security(group_name)

    # 取出列表
    ret, data = fu.quote_context.get_user_security('沪深')
    if ret != RET_OK:
        print(data)
        return

    resultCode = []
    resultName = []
    for row in data.itertuples():
        code = getattr(row, 'code')
        print(code)
        fu.quote_context.subscribe(code, SubType.K_DAY)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=20)
            if ema20.iloc[-1] * 0.8 > data['low'].iloc[-1]:
                print(row)
                resultName.append(getattr(row, 'name'))
                resultCode.append(code)
        else:
            print('error:', data)
    print(resultName)
    if resultName:
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
        # dd.send_day_bull(tips + '\n' + ';'.join(resultName))

    return '日线级别跌幅较大：' + ';'.join(resultName)
