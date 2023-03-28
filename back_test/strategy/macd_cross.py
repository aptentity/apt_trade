import backtrader as bt


class MACDCross(bt.Strategy):
    params = dict(pfast=10, pslow1=30, pslow2=72)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        # print(dir(self.datas[0].datetime))
        print('%s, %s' % (dt, txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        self.ma5 = bt.indicators.MovingAverageSimple(period=5)
        self.ma10 = bt.indicators.MovingAverageSimple(period=10)
        self.ma20 = bt.indicators.MovingAverageSimple(period=20)
        self.MACD = bt.indicators.MACD(self.datas[0])
        self.macd = self.MACD.macd
        self.signal = self.MACD.signal
        self.rsi = bt.indicators.RSI(self.datas[0])
        self.boll = bt.indicators.BollingerBands(self.datas[0])
        self.atr = bt.indicators.ATR(self.datas[0])
        self.buyprice = None
        self.buycomm = None

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
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            else:
                self.log('SELL EXECUTED, Price: %.2f, Size：%.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.size,
                          order.executed.value,
                          order.executed.comm))

    # 交易完统计
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('利润：%.2f,总利润: %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        condition1 = self.macd[-1] - self.signal[-1]
        condition2 = self.macd[0] - self.signal[0]

        if not self.position:
            if condition1 < 0 and condition2 > 0:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order_target_percent(target=0.80)
                # self.buy()

        elif condition1 > 0 and condition2 < 0:
            self.close()

        # # 打印仓位信息
        # print('**************************************************************')
        # print(self.data.datetime.date())
        # for i, d in enumerate(self.datas):
        #     pos = self.getposition(d)
        #     if len(pos):
        #         print('{}, 持仓:{}, 成本价:{}, 当前价:{}, 盈亏:{:.2f}'.format(d._name, pos.size, pos.price, pos.adjbase,
        #                                                                       pos.size * (pos.adjbase - pos.price)))
