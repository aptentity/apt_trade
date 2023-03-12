import os
import sys
from datetime import datetime
import backtrader as bt
import pandas as pd
import strategy.TestStategy as teststategy
import strategy.TwoEmaCrossSignal as tec
import strategy.ThreeEmaCrossSignal as three_ec

# Create a data feed
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, 'data/000002.csv')
data = bt.feeds.GenericCSVData(
    dataname=datapath,
    fromdate=datetime(2022, 2, 8),
    todate=datetime(2023, 2, 7),
    dtformat='%Y-%m-%d',
    datetime=1,
    open=6,
    high=4,
    low=5,
    close=2,
    volume=3,
    reverse=False)

# 实例化回测系统，Cerebro翻译为大脑，回测系统是整个backtrader控制中枢
# cerebro = bt.Cerebro(stdstats=False)
cerebro = bt.Cerebro()
# 初始资金 10000
cerebro.broker.setcash(100000)
# 佣金
cerebro.broker.setcommission(commission=0.002)
cerebro.addsizer(bt.sizers.FixedSizeTarget, stake=5000)
# 滑点：双边各 0.0001
cerebro.broker.set_slippage_perc(perc=0.001)
# Add the data feed
cerebro.adddata(data, name='000001')
# Add the trading strategy
# cerebro.addstrategy(teststategy.TestStrategy)
cerebro.add_signal(bt.SIGNAL_LONG, tec.MySignal)

# cerebro.addobserver(bt.observers.Broker)
# cerebro.addobserver(bt.observers.Trades)
# cerebro.addobserver(bt.observers.BuySell)
cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.TimeReturn)

cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

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
