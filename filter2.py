import time
from futu import *

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
simple_filter = SimpleFilter()
simple_filter.filter_min = 200*100000000
# simple_filter.filter_max = 100*10000
simple_filter.stock_field = StockField.MARKET_VAL
simple_filter.is_no_filter = False
# simple_filter.sort = SortDir.ASCEND

simple_filter2 = SimpleFilter()
simple_filter2.filter_min = 0
simple_filter2.filter_max = 100
simple_filter2.stock_field = StockField.PE_TTM
simple_filter2.is_no_filter = False
simple_filter2.sort = SortDir.ASCEND

financial_filter = FinancialFilter()
financial_filter.filter_min = 0.5
financial_filter.filter_max = 50
financial_filter.stock_field = StockField.CURRENT_RATIO
financial_filter.is_no_filter = False
financial_filter.sort = SortDir.ASCEND
financial_filter.quarter = FinancialQuarter.ANNUAL

custom_filter = CustomIndicatorFilter()
custom_filter.ktype = KLType.K_DAY
custom_filter.stock_field1 = StockField.MA10
custom_filter.stock_field2 = StockField.MA60
custom_filter.relative_position = RelativePosition.MORE
custom_filter.is_no_filter = False

accumulate_filter2 = AccumulateFilter()
accumulate_filter2.stock_field = StockField.CHANGE_RATE
accumulate_filter2.filter_max = 20
accumulate_filter2.filter_min = 10
accumulate_filter2.days = 5


nBegin = 0
last_page = False
ret_list = list()
while not last_page:
    nBegin += len(ret_list)
    ret, ls = quote_ctx.get_stock_filter(market=Market.SH, filter_list=[simple_filter,simple_filter2], begin=nBegin)  # 对香港市场的股票做简单、财务和指标筛选
    if ret == RET_OK:
        last_page, all_count, ret_list = ls
        print('all count = ', all_count)
        for item in ret_list:
            print(item.stock_code)  # 取股票代码
            print(item.stock_name)  # 取股票名称
            # print(item[simple_filter])   # 取 simple_filter 对应的变量值
            # print(item[financial_filter])   # 取 financial_filter 对应的变量值
            # print(item[custom_filter])  # 获取 custom_filter 的数值
    else:
        print('error: ', ls)
    time.sleep(3)  # 加入时间间隔，避免触发限频

quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽