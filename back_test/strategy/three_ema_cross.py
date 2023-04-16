import backtrader as bt


class ThreeEmaCross(bt.Strategy):
    params = dict(pfast=5, pmiddle=20, pslow1=60, pslow2=60)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        # print(dir(self.datas[0].datetime))
        print('%s, %s' % (dt, txt))

    def __init__(self):
        self.ema_fast = bt.ind.EMA(period=self.p.pfast)
        self.ema_middle = bt.ind.EMA(period=self.p.pmiddle)
        self.ema_slow = (bt.ind.EMA(period=self.p.pslow1) + bt.ind.EMA(period=self.p.pslow2)) / 2
        self.crossover_slow = bt.ind.CrossOver(self.ema_middle, self.ema_slow)
        self.crossover_fast = bt.ind.CrossOver(self.ema_fast, self.ema_middle)

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
                          order.executed.comm))

    def next(self):
        if not self.position:
            if self.ema_middle > self.ema_slow and self.crossover_fast > 0:
                # self.buy()
                self.order_target_percent(target=0.80)
        elif self.crossover_slow < 0 or self.crossover_fast < 0:
            self.close()

        # 打印仓位信息
        print('**************************************************************')
        print(self.data.datetime.date())
        for i, d in enumerate(self.datas):
            pos = self.getposition(d)
            if len(pos):
                print('{}, 持仓:{}, 成本价:{}, 当前价:{}, 盈亏:{:.2f}'.format(d._name, pos.size, pos.price, pos.adjbase,
                                                                              pos.size * (pos.adjbase - pos.price)))