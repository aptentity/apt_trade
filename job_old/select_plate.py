"""
选择板块，根据月MACD
"""
from utils import futuUtils as fu
from futu import *
from utils import dingding as dd
from utils import signal_utils as su


def selected(code):
    try:
        fu.quote_context.subscribe(code, SubType.K_WEEK)
        ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
        if ret == RET_OK and (su.qushi_dibu(data['close']) or su.chaodie(data['close'], data['low'])):
            return 1
    except Exception as e:
        print('Error:', e, code)
    return 0


def select_plate():
    group_name = '板块'
    resultCode = []
    resultName = []

    fu.delete_user_security(group_name)
    ret, data = fu.quote_context.get_plate_list(Market.SH, Plate.ALL)
    if ret == RET_OK:
        count = 0
        for row in data.itertuples():
            count = count + 1
            code = getattr(row, 'code')
            result = selected(code)
            print(code, result)
            if result == 1:
                resultCode.append(code)
                resultName.append(getattr(row, 'plate_name'))

            if count % 300 == 0:
                time.sleep(60)
                fu.quote_context.unsubscribe_all()
    else:
        print('error:', data)
    print(resultName)
    fu.quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, resultCode[::-1])

    time.sleep(60)
    fu.quote_context.unsubscribe_all()

    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security('全部')
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            result = selected(code)
            if result == 1:
                selectName.append(getattr(row, 'name'))
                selectCode.append(code)
    fu.quote_context.modify_user_security("重点", ModifyUserSecurityOp.ADD, selectCode[::-1])
    print('select:', selectName)
    tips = '选股：' + ';'.join(selectName)
    dd.send_week_bull(tips)

# print(select_plate())
