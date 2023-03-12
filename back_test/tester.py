import os
import sys
from datetime import datetime
import backtrader as bt
import pandas as pd
from strategy import ema_cross

name = 'HK.07226'
file_name = name + '_day.csv'
from_date = datetime(2021, 1, 1)
to_date = datetime(2023, 3, 12)

# Create a data feed
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, '../data/' + file_name)
data = bt.feeds.GenericCSVData(
    dataname=datapath,
    fromdate=from_date,
    todate=to_date,
    timeframe=bt.TimeFrame.Minutes,
    dtformat='%Y-%m-%d %H:%M:%S',
    tmformat='%H:%M:%S',
    datetime=2,
    open=3,
    high=5,
    low=6,
    close=4,
    volume=9,
    reverse=False)

# 实例化回测系统，Cerebro翻译为大脑，回测系统是整个backtrader控制中枢
# cerebro = bt.Cerebro(stdstats=False)
cerebro = bt.Cerebro()
# 初始资金
cerebro.broker.setcash(1000000)
# 佣金
cerebro.broker.setcommission(commission=0.002)
cerebro.addsizer(bt.sizers.FixedSizeTarget, stake=20000)
# 滑点：双边各 0.0001
cerebro.broker.set_slippage_perc(perc=0.001)
# Add the data feed
cerebro.adddata(data, name=name)
# Add the trading strategy
cerebro.addstrategy(ema_cross.EmaCross)

cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.TimeReturn)

cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
# cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, timeframe=bt.TimeFrame.Minutes, _name="_SharpeRatio")
cerebro.addanalyzer(bt.analyzers.Transactions, _name="trans")

# 启动回测
result = cerebro.run()
# 从返回的 result 中提取回测结果
strat = result[0]
# 返回日度收益率序列
daily_return = pd.Series(strat.analyzers.pnl.get_analysis())
# 打印评价指标
print("--------------- AnnualReturn -----------------")
print(strat.analyzers._AnnualReturn.get_analysis())
print("--------------- SharpeRatio -----------------")
print(strat.analyzers._SharpeRatio.get_analysis())
print("--------------- DrawDown -----------------")
print(strat.analyzers._DrawDown.get_analysis())

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.plot()  # and plot it with a single command
cerebro.plot(iplot=False, style='candel')
