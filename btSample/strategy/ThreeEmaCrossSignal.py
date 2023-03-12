import backtrader as bt


# 三均线：
# 交易信号是由短期均线、中期均线、长期均线这 3 条均线共同确定的。
# 如果只考虑做多的情况，一般是短期均线>中期均线>长期均线，呈多头排列时，买入开仓；出现短期均线下穿中期均线时，卖出平仓。
# 下面是案例具体的策略逻辑：
# 均线：5 日均线为短期均线、20 日均线为中期均线、60 日均线为长期均线；
# 买入开仓：当前无持仓，当开始出现 5 日均线>20 日均线>60 日均线多头排列时，第二天以市价单买入，开仓；
# 卖出平仓：当前持有多单，当日 5 日均线下穿 20 日均线，第二天以市价单卖出，平仓。
class MySignal(bt.Indicator):
    lines = ('signal',)  # 声明 signal 线，交易信号放在 signal line 上
    params = dict(
        short_period=5,
        median_period=20,
        long_period=60)

    def __init__(self):
        self.s_ma = bt.ind.SMA(period=self.p.short_period)
        self.m_ma = bt.ind.SMA(period=self.p.median_period)
        self.l_ma = bt.ind.SMA(period=self.p.long_period)
        # 短期均线在中期均线上方，且中期均取也在长期均线上方，三线多头排列，取值为1；反之，取值为0
        self.signal1 = bt.And(self.m_ma > self.l_ma, self.s_ma > self.m_ma)
        # 求上面 self.signal1 的环比增量，可以判断得到第一次同时满足上述条件的时间，第一次满足条件为1，其余条件为0
        self.buy_signal = bt.If((self.signal1 - self.signal1(-1)) > 0, 1, 0)
        # 短期均线下穿长期均线时，取值为1；反之取值为0
        self.sell_signal = bt.ind.CrossDown(self.s_ma, self.m_ma)
        # 将买卖信号合并成一个信号
        self.lines.signal = bt.Sum(self.buy_signal, self.sell_signal * (-1))
