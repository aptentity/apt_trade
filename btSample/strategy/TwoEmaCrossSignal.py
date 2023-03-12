import backtrader as bt


# 双均线
class MySignal(bt.Indicator):
    lines = ('signal',)  # 声明 signal 线，交易信号放在 signal line 上
    params = dict(
        short_period=5,
        long_period=20)

    def __init__(self):
        self.s_ma = bt.ind.SMA(period=self.p.short_period)
        self.l_ma = bt.ind.SMA(period=self.p.long_period)
        # 短期均线上穿长期均线，取值为1；反之，短期均线下穿长期均线，取值为-1
        self.lines.signal = bt.ind.CrossOver(self.s_ma, self.l_ma)
