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
import pandas as pd


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
    ret, data = fu.quote_context.get_user_security('多')
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
    tips = '买入信号：' + ';'.join(resultNameBuy)
    print(tips)
    logging.info(tips)
    if resultNameBuy and fu.is_ch_normal_trading_time():
        dd.send_notice(tips)


def sell_tip():
    # 取出列表
    ret, data = fu.quote_context.get_user_security('空')
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
    tips = '卖出信号：' + ';'.join(resultNameSell)
    print(tips)
    logging.info(tips)
    if resultNameSell and fu.is_ch_normal_trading_time():
        dd.send_notice(tips)


# 超跌
def overfall():
    selectName = []
    selectCode = []
    selectDayName = []
    selectDayCode = []
    group_name = "超"
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


def is_in_trend(code):
    fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 200, SubType.K_WEEK)
    if ret != RET_OK:
        print(data)
    return ret == RET_OK and su.qushi_dibu(data['close'])


def select_stock_in_plate(plate_list=None):
    if plate_list is None:
        plate_list = ['SZ.399997', 'SH.000300', 'SZ.399673']
        # , 'SH.BK0932', 'SH.BK0068', 'SH.BK0092', 'SH.BK0350',
        #           'SH.BK0652', 'SH.000807', 'SH.BK0637', 'SH.000069', 'SH.000126', 'SZ.399364']
    # plate_list = ['SH.BK0800']
    selectName = []
    selectCode = []
    count = 0
    fu.quote_context.unsubscribe_all()
    for plate in plate_list:
        ret, data = fu.quote_context.get_plate_stock(plate)
        if ret == RET_OK:
            print(len(data))
            for row in data.itertuples():
                count = count + 1
                print(getattr(row, 'code'))
                if is_in_trend(getattr(row, 'code')):
                    selectCode.append(getattr(row, 'code'))
                    selectName.append(getattr(row, 'stock_name'))
                if count % 300 == 0:
                    count = 0
                    time.sleep(60)
                    fu.quote_context.unsubscribe_all()

        print(plate)
        print(selectName)
    fu.quote_context.modify_user_security("重点", ModifyUserSecurityOp.ADD, selectCode[::-1])


# 选择回踩低点的，区间震荡股票
def select_stock_in_interval():
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security('沪深')
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            print(code)
            fu.quote_context.subscribe(code, SubType.K_WEEK)
            ret, data = fu.quote_context.get_cur_kline(code, 100, SubType.K_WEEK)
            if ret == RET_OK and len(data) > 90:
                print(min(data['low'][50:90]))
                min_low = min(data['low'][50:90])
                if abs((data['low'].iloc[-1] - min_low) / min_low) < 0.1:
                    selectCode.append(getattr(row, 'code'))
                    selectName.append(getattr(row, 'name'))
        fu.quote_context.modify_user_security('前低', ModifyUserSecurityOp.ADD, selectCode[::-1])


def is_in_day_trend(code):
    fu.quote_context.subscribe(code, SubType.K_DAY)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
    if ret == RET_OK:
        return su.over_bought(data['close'], data['high'], 50) and su.macd_king_cross(data['close'])
    else:
        print(code, data)
        return False


def select_stock_day_trend(plate_list=None):
    if plate_list is None:
        plate_list = ['SZ.399997', 'SH.000300', 'SZ.399673']

    selectName = []
    selectCode = []
    count = 0
    fu.quote_context.unsubscribe_all()
    for plate in plate_list:
        ret, data = fu.quote_context.get_plate_stock(plate)
        if ret == RET_OK:
            print(len(data))
            for row in data.itertuples():
                count = count + 1
                print(getattr(row, 'code'))
                if is_in_day_trend(getattr(row, 'code')):
                    selectCode.append(getattr(row, 'code'))
                    selectName.append(getattr(row, 'stock_name'))
                if count % 300 == 0:
                    print(selectName)
                    count = 0
                    time.sleep(60)
                    fu.quote_context.unsubscribe_all()
        print(plate)
        print(selectName)
    fu.quote_context.modify_user_security("重点", ModifyUserSecurityOp.ADD, selectCode[::-1])
    print('select_stock_day_trend done')


# select_stock_day_trend()
# select_stock_in_plate(['SH.BK0594'])

# ret, data = fu.quote_context.get_plate_stock('SH.BK0637')
# print(data)

# ret, data1 = fu.quote_context.get_plate_stock('SH.000069')
# ret, data2 = fu.quote_context.get_plate_stock('SH.000126')
# ret, data3 = fu.quote_context.get_plate_stock('SZ.399364')
# result = pd.concat([data1, data2, data3], ignore_index=True)
# result = result.drop_duplicates(subset=['code'])
# print(result)


def select_up_and_down():
    ret, data = fu.quote_context.get_user_security("沪深")
    king_cross_name = []
    death_cross_name = []
    up_code = []
    down_code = []
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            fu.quote_context.subscribe(code, SubType.K_15M)
            ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_15M)
            if ret == RET_OK:
                if su.ema_above_base(data['close']):
                    up_code.append(code)
                else:
                    down_code.append(code)
                if su.ema_king_cross(data['close']):
                    king_cross_name.append(getattr(row, 'name'))
                elif su.ema_death_cross(data['close']):
                    death_cross_name.append(getattr(row, 'name'))

    fu.quote_context.modify_user_security('多', ModifyUserSecurityOp.MOVE_OUT, down_code)
    fu.quote_context.modify_user_security('空', ModifyUserSecurityOp.MOVE_OUT, up_code)
    fu.quote_context.modify_user_security('多', ModifyUserSecurityOp.ADD, up_code[::-1])
    fu.quote_context.modify_user_security('空', ModifyUserSecurityOp.ADD, down_code[::-1])
    if fu.is_ch_normal_trading_time() and (king_cross_name or death_cross_name):
        tips = '15分钟金叉：' + ';'.join(king_cross_name) + '\n' + '15分钟死叉：' + ';'.join(death_cross_name)
        dd.send_notice(tips)


def select_etf():
    etf = pd.read_csv('./object/etf_new.csv')
    selectName = []
    selectCode = []
    select_day_code = []
    select_day_name = []

    chaodie = []
    for item in etf.itertuples():
        code = str(getattr(item, 'code'))
        if not code.__contains__('.'):
            new_code = 'SH.' + code if code.startswith('5') else 'SZ.' + code
        else:
            new_code = code
        fu.quote_context.subscribe(new_code, SubType.K_WEEK)
        ret, data = fu.quote_context.get_cur_kline(new_code, 200, SubType.K_WEEK)
        if ret != RET_OK:
            print(code, data)
        else:
            # 超跌
            if su.chaodie(data['close'], data['low']):
                chaodie.append(new_code)

            # 周线向上
            if su.macd_up(data['close']):
                selectCode.append(new_code)
                selectName.append(getattr(item, 'name'))

            if su.ema_above_base(data['close']):
                print(new_code, getattr(item, 'name'))
                fu.quote_context.subscribe(new_code, SubType.K_DAY)
                ret1, data1 = fu.quote_context.get_cur_kline(new_code, 1000, SubType.K_DAY)
                if ret != RET_OK:
                    print(code, data)
                elif su.macd_up(data1['close']):
                    select_day_code.append(new_code)
                    selectName.append(getattr(item, 'name'))

    print('chaodie', chaodie)
    print('selectCode', selectCode)
    print('selectName', selectName)
    print('select_day_code:', select_day_code)
    print('select_day_name:', select_day_name)

    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, chaodie[::-1])
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, select_day_code[::-1])


# 周线和日线均良好
def is_in_week_day_trend(code):
    fu.quote_context.subscribe(code, SubType.K_WEEK)
    ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_WEEK)
    if ret != RET_OK:
        print(code, data)
    elif su.ema_above_base(data['close']):
        fu.quote_context.subscribe(code, SubType.K_DAY)
        ret, data = fu.quote_context.get_cur_kline(code, 1000, SubType.K_DAY)
        if ret != RET_OK:
            print(code, data)
        elif su.ema_above_base2(data['close'], day=5) and su.macd_up(data['close']):
            if data['close'].iloc[-1] / data['open'].iloc[-1] < 1.05 and data['close'].iloc[-1] / data['open'].iloc[
                -3] < 1.12:
                return True
    return False


def select_object_in_trend():
    def check_length():
        if len(allCode) % 150 == 0:
            print(allCode)
            print(len(allCode))
            time.sleep(60)
            fu.quote_context.unsubscribe_all()

    allCode = []
    selectName = []
    selectCode = []
    ret, data = fu.quote_context.get_user_security("沪深")
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            allCode.append(code)
            check_length()
            if is_in_week_day_trend(getattr(row, 'code')):
                selectCode.append(getattr(row, 'code'))
                selectName.append(getattr(row, 'name'))

    etf = pd.read_csv('./object/etf_new.csv')
    stock = pd.read_csv('./object/stock.csv')
    stock_low = pd.read_csv('./object/stock_low.csv')
    new_list = pd.concat([etf, stock, stock_low])
    for row in new_list.itertuples():
        code = str(getattr(row, 'code'))
        if not code.__contains__('.'):
            code = 'SH.' + code if code.startswith('5') else 'SZ.' + code
        if code in allCode:
            print(code)
        else:
            allCode.append(code)
            check_length()
            if is_in_week_day_trend(code):
                selectCode.append(code)
                selectName.append(getattr(row, 'name'))

    plate = pd.read_csv('./object/plate.csv')
    plate_list = plate[plate['enable'] != 'n']

    for plate in plate_list:
        ret, data = fu.quote_context.get_plate_stock(plate)
        if ret == RET_OK:
            for row in data.itertuples():
                code = getattr(row, 'code')
                if code in allCode:
                    print(code)
                else:
                    allCode.append(code)
                    check_length()
                    if is_in_week_day_trend(code):
                        selectCode.append(code)
                        selectName.append(getattr(row, 'stock_name'))
        else:
            print(plate, data)

    print(selectName)
    print(selectCode)
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, selectCode[::-1])


def select_object_in_trend_in_plate(plate_list):
    def check_length():
        if len(allCode) % 150 == 0:
            print(allCode)
            print(len(allCode))
            time.sleep(60)
            fu.quote_context.unsubscribe_all()

    allCode = []
    selectName = []
    selectCode = []
    for plate in plate_list:
        ret, data = fu.quote_context.get_plate_stock(plate)
        if ret == RET_OK:
            for row in data.itertuples():
                code = getattr(row, 'code')
                print(code)
                if code in allCode:
                    print(code)
                else:
                    allCode.append(code)
                    check_length()
                    if is_in_week_day_trend(code):
                        selectCode.append(code)
                        selectName.append(getattr(row, 'stock_name'))
        else:
            print(data)

    print(selectName)
    print(selectCode)
