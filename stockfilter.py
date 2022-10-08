# 做多的股票
# 15分钟ema
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding

fu.clear_user_security('普通做多')

# 取出列表
ret, data = fu.quote_context.get_user_security('沪深')
if ret == RET_OK:
    print(data)

resultCode = []
result = []
for row in data.itertuples():
    code = getattr(row, 'code')
    print(code)

    fu.quote_context.subscribe(code, SubType.K_15M)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
    if ret == RET_OK:
        # print(data)
        ema20 = ta.ma('ema', data['close'], length=20)
        ema30 = ta.ma('ema', data['close'], length=30)
        ema72 = ta.ma('ema', data['close'], length=72)
        base = (ema30 + ema72) / 2
        if ema20.iloc[-1] > base.iloc[-1]:
            print(row)
            result.append(row)
            resultCode.append(code)
    else:
        print('error:', data)

# fu.quote_context.modify_user_security('普通做多', ModifyUserSecurityOp.ADD, resultCode)
print(result)
