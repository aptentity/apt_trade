# 短线超卖
# 15分钟跌破CB1，在1分钟金叉后，选择向上趋势或者震荡中，不能选择下跌趋势
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta

# 取出列表
ret, data = fu.quote_context.get_user_security('沪深')
if ret == RET_OK:
    print(data)

resultCode = []
result = []
for row in data.itertuples():
    code = getattr(row, 'code')

    fu.quote_context.subscribe(code, SubType.K_15M)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
    if ret == RET_OK:
        ema20 = ta.ma('ema', data['close'], length=20)
        print(code)
        print(data['high'].iloc[-1])
        if ema20.iloc[-1] * 1.01 < data['high'].iloc[-1]:
            print(row)
            result.append(row)
            resultCode.append(code)
    else:
        print('error:', data)

fu.quote_context.modify_user_security('短线超买', ModifyUserSecurityOp.ADD, resultCode)
print(result)
