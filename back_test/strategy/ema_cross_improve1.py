import backtrader as bt


# 改进，增加止损和止盈

class EmaCross(bt.Strategy):
    params = dict(pfast=20, pslow1=30, pslow2=72)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        # print(dir(self.datas[0].datetime))
        print('%s, %s' % (dt, txt))

    def __init__(self):
        ema_fast = bt.ind.EMA(period=self.p.pfast)
        ema_slow = (bt.ind.EMA(period=self.p.pslow1) + bt.ind.EMA(period=self.p.pslow2)) / 2
        self.crossover = bt.ind.CrossOver(ema_fast, ema_slow)
        self.highest = -1

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
        sell = False
        position = self.position
        if not position:
            if self.crossover > 0:
                # self.buy()
                self.order_target_percent(target=0.80)
                self.highest = -1
                self.log('buy')
        else:
            if self.crossover < 0:  # 卖出信号
                sell = True
            elif position.adjbase / position.price < 0.92:  # 止损
                self.log('=========止损')
                sell = True
            elif position.adjbase / position.price > 1.08 and position.adjbase > self.highest:
                self.highest = position.adjbase
            if position.adjbase - position.price < (self.highest - position.price) / 2:  # 止盈
                self.log('=========止盈')
                sell = True
        if sell:
            self.log('sell')
            self.close()

        # # 打印仓位信息
        # print('**************************************************************')
        # print(self.data.datetime.date())
        # for i, d in enumerate(self.datas):
        #     pos = self.getposition()
        #     if len(pos):
        #         print('{}, 持仓:{}, 成本价:{}, 当前价:{}, 盈亏:{:.2f}'.format(d._name, pos.size, pos.price, pos.adjbase,
        #                                                                       pos.size * (pos.adjbase - pos.price)))
