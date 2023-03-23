# 用于过滤股票，规则：
# 1、沪深->自选：周均线金叉
# 2、自选->重点：最近5个交易日内，10日均线有3天高于base，且macd在零轴下拐头向上(增量)；周线
# 3、重点->操作：15分钟均线金叉后
# 4、操作->买点：重点中15分钟macd零轴下拐头向上
# 5、卖点：自选股中15分钟macd零轴上拐头向下
# 6、超跌：日或者周跌破AB1

from utils import futuUtils as fu
from futu import *
from utils import signal_utils as su
from utils import dingding as dd


# 沪深->自选
def select_my(name='沪深'):
    group_name = "自选"
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security(name)
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_WEEK)
            ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
            if ret == RET_OK and su.ema_above_base(data['close']):
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectCode[::-1])
    print('select_my:', selectName)


# 自选->重点
def select_focus():
    selectName = []
    selectCode = []
    selectDayName = []
    selectDayCode = []
    group_name = "重点"
    ret, data = fu.quote_context.get_user_security('自选')
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_WEEK)
            ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
            if ret == RET_OK and su.qushi_dibu(data['close']):
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
            else:
                fu.quote_context.subscribe(code, SubType.K_DAY)
                ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_DAY)
                if ret == RET_OK and su.qushi_dibu(data['close']):
                    selectDayName.append(getattr(row, 'name'))
                    selectDayCode.append(code)

    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectDayCode[::-1])
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectCode[::-1])
    print('select_focus:', selectName)
    print('select_day_focus', selectDayName)


# 重点->操作
def select_operation():
    group_name = "操作"
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security("重点")
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_15M)
            ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
            if ret == RET_OK and su.ema_above_base(data['close']):
                # 判断日线
                fu.quote_context.subscribe(code, SubType.K_DAY)
                ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_DAY)
                if ret == RET_OK:
                    result = su.cal_macd(data['close'])
                    amount = 0
                    for i in range(0, 2):
                        if result.iloc[(-1 - i)] > result.iloc[(-2 - i)]:
                            amount = amount + 1
                    if amount > 0 and min(result.iloc[-1], result.iloc[-2], result.iloc[-3]) < 0:
                        selectName.append(getattr(row, 'name'))
                        selectCode.append(code)
    fu.clear_user_security(group_name)
    fu.add_user_security(group_name, selectCode[::-1])
    print('select_operation:', selectName)


# 15分钟金叉提醒
def ema_king_cross_tip():
    group_from = '重点'
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security(group_from)
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_15M)
            ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
            if ret == RET_OK and su.ema_king_cross(data['close']):
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    if selectName:
        tips = '15分钟金叉：' + ';'.join(selectName)
        if fu.is_ch_normal_trading_time():
            dd.trend_bull(tips)
        logging.info(tips)


# 15分钟金叉提醒
def ema_death_cross_tip():
    group_from = '特别关注'
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security(group_from)
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_15M)
            ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
            if ret == RET_OK and su.ema_death_cross(data['close']):
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    if selectName:
        tips = '15分钟死叉：' + ';'.join(selectName)
        if fu.is_ch_normal_trading_time():
            dd.trend_bear(tips)
        logging.info(tips)


def buy_tip():
    # 取出列表
    ret, data = fu.quote_context.get_user_security('操作')
    resultNameBuy = []
    resultCode = []
    group_name = '买点'
    if ret != RET_OK:
        print(data)
        return
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK:
            result = su.cal_macd(data['close'])
            if result.iloc[-3] < 0 and result.iloc[-1] > result.iloc[-2] > result.iloc[-3] < result.iloc[-4]:
                # or (result.iloc[-1] > result.iloc[-2] < result.iloc[-3] and result.iloc[-2] > 0):
                resultNameBuy.append(getattr(row, 'name'))
                resultCode.append(code)
        else:
            print('error:', data)

    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])
    if resultNameBuy and fu.is_ch_normal_trading_time():
        tips = '买入信号：' + ';'.join(resultNameBuy)
        dd.trend_bull(tips)
        logging.info(tips)


def sell_tip():
    # 取出列表
    ret, data = fu.quote_context.get_user_security('特别关注')
    resultNameSell = []
    resultCode = []
    group_name = '卖点'
    if ret != RET_OK:
        print(data)
        return
    for row in data.itertuples():
        code = getattr(row, 'code')
        fu.quote_context.subscribe(code, SubType.K_15M)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
        if ret == RET_OK and su.ema_below_base(data['close']):
            result = su.cal_macd(data['close'])
            if result.iloc[-3] > 0 and result.iloc[-1] < result.iloc[-2] < result.iloc[-3] > result.iloc[-4]:
                resultNameSell.append(getattr(row, 'name'))
                resultCode.append(code)

    fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])
    if resultNameSell and fu.is_ch_normal_trading_time():
        tips = '卖出信号：' + ';'.join(resultNameSell)
        dd.trend_bear(tips)
        logging.info(tips)


# 超跌
def overfall():
    selectName = []
    selectCode = []
    selectDayName = []
    selectDayCode = []
    group_name = "超跌"
    ret, data = fu.quote_context.get_user_security("全部")
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_WEEK)
            ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
            if ret == RET_OK:
                ema30 = su.get_EMA(data['close'], 30)
                ema72 = su.get_EMA(data['close'], 72)
                base = (ema30 + ema72) / 2
                if data['low'].iloc[-1] < base.iloc[-1] * 0.8:
                    selectName.append(getattr(row, 'name'))
                    selectCode.append(code)
            else:
                fu.quote_context.subscribe(code, SubType.K_DAY)
                ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_DAY)
                if ret == RET_OK:
                    ema30 = su.get_EMA(data['close'], 30)
                    ema72 = su.get_EMA(data['close'], 72)
                    base = (ema30 + ema72) / 2
                    if data['low'].iloc[-1] < base.iloc[-1] * 0.8:
                        selectDayName.append(getattr(row, 'name'))
                        selectDayCode.append(code)
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectDayCode[::-1])
        fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectCode[::-1])
        print('overfall:', selectName)
        print('overfall_day:', selectDayName)

