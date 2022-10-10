# 做多的股票
# 15分钟ema
import select_plate
from utils import futuUtils as fu
from futu import *
import pandas_ta as ta
from utils import dingding as dd


def trend_bull(cross):
    print('trend_bull doing')
    tips = '1、15分钟金叉 \n'

    group_name = '趋势多'

    if cross != 1:
        fu.clear_user_security(group_name)

    # 取出列表
    ret, data = fu.quote_context.get_user_security('沪深')
    if ret != RET_OK:
        print(data)

    resultCode = []
    resultName = []
    resultNew = []
    for row in data.itertuples():
        code = getattr(row, 'code')
        # print(code)

        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            # print(data)
            ema20 = ta.ma('ema', data['close'], length=20)
            ema30 = ta.ma('ema', data['close'], length=30)
            ema72 = ta.ma('ema', data['close'], length=72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] > base.iloc[-1]:
                if cross == 1:
                    if ema20.iloc[-2] < base.iloc[-2]:
                        resultNew.append(getattr(row, 'name'))
                        resultCode.append(code)
                else:
                    resultName.append(getattr(row, 'name'))
                    resultCode.append(code)
        else:
            print('error:', data)
    print(resultName)
    if resultName or resultNew:
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode)
        dd.trend_bull(tips + '\n----\n' + ';'.join(resultNew) + '\n----\n' + ';'.join(resultName))

    if cross == 1:
        return

    day_code = []
    # 根据日线、周线过滤
    for code in resultCode:
        print(code)
        fu.quote_context.subscribe(code, SubType.K_DAY)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
        if ret == RET_OK:
            # ema20 = ta.ma('ema', data['close'], length=20)
            # ema30 = ta.ma('ema', data['close'], length=30)
            # ema72 = ta.ma('ema', data['close'], length=72)
            ema20 = select_plate.get_EMA(data['close'], 20)
            ema30 = select_plate.get_EMA(data['close'], 30)
            ema72 = select_plate.get_EMA(data['close'], 72)
            print(ema72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] > base.iloc[-1]:
                day_code.append(code)
    print(day_code)
    group_name = '趋势多日'
    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, day_code)

    week_code = []
    for code in resultCode:
        fu.quote_context.subscribe(code, SubType.K_WEEK)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_WEEK)
        if ret == RET_OK:
            ema20 = select_plate.get_EMA(data['close'], 20)
            ema30 = select_plate.get_EMA(data['close'], 30)
            ema72 = select_plate.get_EMA(data['close'], 72)
            base = (ema30 + ema72) / 2
            if ema20.iloc[-1] > base.iloc[-1]:
                week_code.append(code)
    print(week_code)
    group_name = '趋势多周'
    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, week_code)
