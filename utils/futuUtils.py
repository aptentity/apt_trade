from futu import *
import pandas as pd

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 1000)

TRADING_ENVIRONMENT = TrdEnv.REAL  # 交易环境：真实 / 模拟
TRADING_MARKET = TrdMarket.HK  # 交易市场权限，用于筛选对应交易市场权限的账户
TRADING_PWD = '889406'  # 交易密码，用于解锁交易
FUTUOPEND_ADDRESS = '127.0.0.1'  # FutuOpenD 监听地址
FUTUOPEND_PORT = 11111  # FutuOpenD 监听端口

quote_context = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象
trade_context = OpenSecTradeContext(filter_trdmarket=TRADING_MARKET, host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT,
                                    security_firm=SecurityFirm.FUTUSECURITIES)  # 交易对象，根据交易品种修改交易对象类型
trade_us_context = OpenSecTradeContext(filter_trdmarket=TrdMarket.US, host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT,
                                       security_firm=SecurityFirm.FUTUSECURITIES)  # 交易对象，根据交易品种修改交易对象类型


# 解锁交易
def unlock_trade():
    if TRADING_ENVIRONMENT == TrdEnv.REAL:
        ret, data = trade_context.unlock_trade(TRADING_PWD)
        if ret != RET_OK:
            print('解锁交易失败：', data)
            return False
        print('解锁交易成功！')
        ret, data = trade_us_context.unlock_trade(TRADING_PWD)
        if ret != RET_OK:
            print('解锁交易失败：', data)
            return False
        print('解锁交易成功！')
    return True


def is_ch_normal_trading_time():
    ret, data = quote_context.get_market_state(['SH.000001', 'HK.07226'])
    if ret != RET_OK:
        print('获取市场状态失败：', data)
        return False
    market_state = data['market_state'][0]
    print(data['market_state'])
    if market_state == MarketState.MORNING or \
            market_state == MarketState.AFTERNOON:
        return True
    # market_state = data['market_state'][1]
    # if market_state == MarketState.MORNING or \
    #         market_state == MarketState.AFTERNOON:
    #     return True
    return False


def is_us_normal_trading_time():
    ret, data = quote_context.get_market_state(['US.AAPL'])
    if ret != RET_OK:
        print('获取市场状态失败：', data)
        return False
    market_state = data['market_state'][0]
    print(market_state)
    if market_state == MarketState.AFTERNOON or \
            market_state == MarketState.PRE_MARKET_BEGIN or \
            market_state == MarketState.AFTER_HOURS_BEGIN:
        return True
    return False


def is_us_trading_time():
    ret, data = quote_context.get_market_state(['US.AAPL'])
    if ret != RET_OK:
        print('获取市场状态失败：', data)
        return False
    market_state = data['market_state'][0]
    print(market_state)
    if market_state == MarketState.AFTERNOON:
        return True
    return False


# 买入操作时间段
def is_buy_trading_time(code):
    ret, data = quote_context.get_market_state(code)
    if ret != RET_OK:
        print('获取市场状态失败：', data)
        return False
    market_state = data['market_state'][0]
    print(market_state)
    if "US" in code and market_state == MarketState.AFTERNOON:
        return True
    elif "HK" in code and (market_state == MarketState.MORNING or market_state == MarketState.AFTERNOON):
        return True
    else:
        return False


def is_sell_trading_time(code):
    ret, data = quote_context.get_market_state(code)
    if ret != RET_OK:
        print('获取市场状态失败：', data)
        return False
    market_state = data['market_state'][0]
    print(market_state)
    if "US" in code and (market_state == MarketState.AFTERNOON or
                         market_state == MarketState.PRE_MARKET_BEGIN or
                         market_state == MarketState.AFTER_HOURS_BEGIN):
        return True
    elif "HK" in code and (market_state == MarketState.MORNING or market_state == MarketState.AFTERNOON):
        return True
    else:
        return False


# 获取市场状态
def is_normal_trading_time(code):
    ret, data = quote_context.get_market_state([code])
    if ret != RET_OK:
        print('获取市场状态失败：', data)
        return False
    market_state = data['market_state'][0]
    print(market_state)
    '''
    MarketState.MORNING            港、A 股早盘
    MarketState.AFTERNOON          港、A 股下午盘，美股全天
    MarketState.FUTURE_DAY_OPEN    港、新、日期货日市开盘
    MarketState.FUTURE_OPEN        美期货开盘
    MarketState.NIGHT_OPEN         港、新、日期货夜市开盘
    '''
    if market_state == MarketState.MORNING or \
            market_state == MarketState.AFTERNOON or \
            market_state == MarketState.FUTURE_DAY_OPEN or \
            market_state == MarketState.FUTURE_OPEN or \
            market_state == MarketState.PRE_MARKET_BEGIN or \
            market_state == MarketState.AFTER_HOURS_BEGIN or \
            market_state == MarketState.NIGHT_OPEN:
        return True
    print('现在不是持续交易时段。')
    return False


# 获取持仓数量(只可以获取trade_context指定市场的股票)
def get_holding_position(code):
    holding_position = 0
    ret, data = trade_context.position_list_query(code=code, trd_env=TRADING_ENVIRONMENT)
    if ret != RET_OK:
        print('获取持仓数据失败：', data)
        return None
    else:
        if data.shape[0] > 0:
            holding_position = data['qty'][0]
        print('【持仓状态】 {} 的持仓数量为：{}'.format(code, holding_position))
    return holding_position


# 获取一档摆盘的 ask1 和 bid1
def get_ask_and_bid(code):
    quote_context.subscribe([code], [SubType.ORDER_BOOK], subscribe_push=False)
    ret, data = quote_context.get_order_book(code, num=1)
    if ret != RET_OK:
        print('获取摆盘数据失败：', data)
        return None, None
    return data['Ask'][0][0], data['Bid'][0][0]


def add_user_security(group_name, code_list):
    quote_context.modify_user_security(group_name, ModifyUserSecurityOp.ADD, code_list)


# 清空分组中股票
def clear_user_security(group_name):
    ret, data = quote_context.get_user_security(group_name)
    result = []
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            result.append(code)
    quote_context.modify_user_security(group_name, ModifyUserSecurityOp.MOVE_OUT, result)


# 清空分组中股票
def delete_user_security(group_name):
    ret, data = quote_context.get_user_security(group_name)
    result = []
    if ret == RET_OK:
        for row in data.itertuples():
            code = getattr(row, 'code')
            result.append(code)
    quote_context.modify_user_security(group_name, ModifyUserSecurityOp.DEL, result)


def get_trade_context(code):
    if "US" in code:
        return trade_us_context
    if "HK" in code:
        return trade_context


def query_subscription():
    ret, data = quote_context.query_subscription()
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
