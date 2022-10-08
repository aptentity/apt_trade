from futu import *
from utils import futuUtils as fu

# fu.unlock_trade()

# fu.is_normal_trading_time('HK.07226')

# fu.get_holding_position('US.SOXL')

# print(fu.get_ask_and_bid('US.SOXL'))
# quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
# print(quote_ctx.get_market_snapshot('HK.00700'))  # 获取港股 HK.00700 的快照数据
# quote_ctx.close() # 关闭对象，防止连接条数用尽
#
#
# trd_ctx = OpenSecTradeContext(host='127.0.0.1', port=11111)  # 创建交易对象
# print(trd_ctx.place_order(price=500.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE))  # 模拟交易，下单（如果是真实环境交易，在此之前需要先解锁交易密码）
#
# trd_ctx.close()  # 关闭对象，防止连接条数用尽

# ret, data = fu.quote_context.get_user_security_group()
# if ret == RET_OK:
#     print(data)

ret, data = fu.quote_context.get_user_security('沪深')
if ret == RET_OK:
    print(data)

print(data.iloc[0, 0])
#
# for row in data.itertuples():
#     print(row[1])

fu.quote_context.subscribe(data.iloc[0, 0], SubType.K_15M)
ret, data = fu.quote_context.get_cur_kline(data.iloc[0, 0], 1000, SubType.K_15M)
if ret == RET_OK:
    print('111111111')
    print(data)
else:
    print('error:', data)

