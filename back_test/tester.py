import logging
import os
import sys
from datetime import datetime
import backtrader as bt
import pandas as pd
from strategy import ema_cross
from strategy import three_ema_cross
from strategy import three_ema_cross_signal
from strategy import ema_cross_improve1
from strategy import fix_time
from strategy import macd_cross

# SH.600702  HK.07552  HK.07226
# SZ.300759
#
name = 'SZ.159949'
file_name = name + '_day.csv'
from_date = datetime(2016, 10, 1)
to_date = datetime(2021, 10, 1)
strategy = macd_cross.MACDCross

logging.basicConfig(level=logging.INFO,
                    filename='tester_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
logging.info('% s,% s, % s' % (file_name, from_date, to_date))

logging.info(strategy)

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
cerebro.broker.set_slippage_perc(perc=0.002)
# Add the data feed
cerebro.adddata(data, name=name)
# Add the trading strategy
cerebro.addstrategy(strategy)
# cerebro.addstrategy(three_ema_cross.ThreeEmaCross)
# cerebro.add_signal(bt.SIGNAL_LONG, three_ema_cross_signal.ThreeEmaCrossSignal)

cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.TimeReturn)

cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, _name='pnl')  # 返回收益率时序数据
cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years, data=data, _name='BenchTimeReturn')
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
print("--------------- TimeReturn -----------------")
print(strat.analyzers.pnl.get_analysis())
print("--------------- BenchTimeReturn -----------------")
print(strat.analyzers.BenchTimeReturn.get_analysis())

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
logging.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
logging.info('=========================================')
logging.info('=========================================')

# cerebro.plot()  # and plot it with a single command
cerebro.plot(iplot=False, style='candel')
