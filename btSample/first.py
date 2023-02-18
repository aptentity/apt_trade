import os
import sys
from datetime import datetime
import backtrader as bt
import pandas as pd


class SmaCross(bt.Strategy):
    params = dict(pfast=10, pslow=30)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()


class TestStategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bar_executed = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查订单是否成交
        # 注意，如果现金不够的话，订单会被拒接
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(order.status)
            self.log(order.Margin)
            self.log('Order Canceled/Margin/Rejected')

        # 记录没有挂起的订单
        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        # 检查是否有挂起的订单，如果有的话，不能再发起一个订单
        if self.order:
            return

        # 检查是否在市场（有持仓）
        if not self.position:
            # 不在，那么连续3天价格下跌就买点
            if self.dataclose[0] < self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()

        else:
            # 已经在市场，5天后就卖掉。
            if len(self) >= (
                    self.bar_executed + 5):  # 这里注意，Len(self)返回的是当前执行的bar数量，每次next会加1.而Self.bar_executed
                # 记录的最后一次交易执行时的bar位置。
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


# Create a data feed
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(modpath, 'data/000001.csv')
data = bt.feeds.GenericCSVData(
    dataname=datapath,
    fromdate=datetime(2022, 2, 8),
    todate=datetime(2023, 2, 7),
    dtformat='%Y-%m-%d',
    datetime=1,
    open=3,
    high=4,
    low=5,
    close=2,
    volume=3,
    reverse=False)

# 实例化回测系统，Cerebro翻译为大脑，回测系统是整个backtrader控制中枢
cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
# 初始资金 10000
cerebro.broker.setcash(100000)
# 佣金
cerebro.broker.setcommission(commission=0.002)
cerebro.addsizer(bt.sizers.FixedSize, stake=100)
cerebro.adddata(data)  # Add the data feed
# cerebro.addstrategy(SmaCross)  # Add the trading strategy
cerebro.addstrategy(TestStategy)
cerebro.run()  # run it all
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()  # and plot it with a single command
