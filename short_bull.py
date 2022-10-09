# 短线超卖
# 15分钟跌破CB1，在1分钟金叉后，选择向上趋势或者震荡中，不能选择下跌趋势
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def short_bull():
    print('short_bull doing')
    tips = '1、日线级别处于上升趋势，且偏离率并不大，或者是震荡趋势；\n' \
           '2、日线级别超跌严重，接近AB1，不可用连续跌停\n' \
           '3、只是博反弹，小仓位、不论对错，持仓都不可超过2天\n' \
           '4、短期内第二次出现反弹的概率高，快速拉起比较好，平盘的需要等MACD金叉\n' \
           '5、需要等待至少1分钟金叉后回调买入\n'

    group_name = '短线多'

    fu.clear_user_security(group_name)

    # 取出列表
    ret, data = fu.quote_context.get_user_security('沪深')
    if ret != RET_OK:
        print(data)

    resultCode = []
    resultName = []
    for row in data.itertuples():
        code = getattr(row, 'code')
        # print(code)
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            ema20 = ta.ma('ema', data['close'], length=20)
            if ema20.iloc[-1] * 0.95 > data['low'].iloc[-1]:
                # print(row)
                resultName.append(getattr(row, 'name'))
                resultCode.append(code)
        else:
            print('error:', data)
    print('short_bull done')
    print(resultName)
    if resultName:
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
        dd.send_short_bull(tips + '\n' + ';'.join(resultName))
