# 第二波战法
# 板块：选择20周内突破过AT1，10日线没有跌破base，macd向上
# 个股：选择50个交易日内突破过AT1，10日线没有跌破base，macd向上
from utils import futuUtils as fu
from futu import *
from utils import signal_utils as su


def stock_second_wave():
    group_name = "超"
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security("沪深")
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_DAY)
            ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
            if ret == RET_OK and su.over_bought(data['close'], data['high'], 50) and su.qushi_dibu(data['close']):
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    # fu.clear_user_security(group_name)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectCode[::-1])


def plate_second_wave():
    group_name = "超"
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security("板块")
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_WEEK)
            ret, data = fu.quote_context.get_cur_kline(code, 100, SubType.K_WEEK)
            if ret == RET_OK and su.over_bought(data['close'], data['high'], 20):
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, selectCode[::-1])
