# 短线超卖
# 15分钟跌破CB1，在1分钟金叉后，选择向上趋势或者震荡中，不能选择下跌趋势
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def week_bull():
    print('week_bull doing')
    tips = '1、周线超跌博反弹，等待日macd向上，标志性k线\n' \
           '2、日线走出向上趋势' \

    group_name = '周多'

    fu.clear_user_security(group_name)

    # 取出列表
    ret, data = fu.quote_context.get_user_security('沪深')
    if ret == RET_OK:
        print(data)

    resultCode = []
    resultName = []
    for row in data.itertuples():
        code = getattr(row, 'code')
        print(code)
        fu.quote_context.subscribe(code, SubType.K_WEEK)
        ret, data = fu.quote_context.get_cur_kline(code, 100, SubType.K_WEEK)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=20)
            try:
                if ema20.iloc[-1] * 0.75 > data['low'].iloc[-1]:
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
        dd.send_week_bull(tips + '\n' + ';'.join(resultName))

