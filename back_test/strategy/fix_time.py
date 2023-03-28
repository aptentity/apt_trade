# 用于测试恒生期货在美股开盘15分钟内的表现
# 结论是没有明显的时机特征
import backtrader as bt


class FixTime(bt.Strategy):
    params = dict(pfast=10, pslow1=30, pslow2=72)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        # print(dir(self.datas[0].datetime))
        print('%s, %s' % (dt, txt))

    def __init__(self):
        ema_fast = bt.ind.EMA(period=self.p.pfast)
        ema_slow = (bt.ind.EMA(period=self.p.pslow1) + bt.ind.EMA(period=self.p.pslow2)) / 2
        self.crossover = bt.ind.CrossOver(ema_fast, ema_slow)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Size：%.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.size,
                          order.executed.value,
                          order.executed.comm))
            else:
                self.log('SELL EXECUTED, Price: %.2f, Size：%.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.size,
                          order.executed.value,
                          order.executed.comm,))

    def next(self):
        print(self.datas[0].datetime.datetime(0))
        aa = self.datas[0].datetime.time(0).strftime('%H:%M:%S')
        date_run = self.datas[0].datetime.date(0).strftime('%Y:%m:%d')
        print(aa)
        if not self.position:
            if aa == '15:00:00':
                self.order_target_percent(target=0.80)
        elif aa == '16:00:00':
            self.close()
