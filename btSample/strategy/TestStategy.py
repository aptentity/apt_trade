import backtrader as bt


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bar_executed = 0
        self.log('--init--')

        self.sma5 = bt.indicators.SimpleMovingAverage(period=5)  # 5日均线
        self.sma10 = bt.indicators.SimpleMovingAverage(period=10)  # 10日均线
        self.buy_sig = self.sma5 > self.sma10  # 5日均线上穿10日均线

        # print("-------------self.datas-------------")
        # print(self.datas)
        # print("-------------self.data-------------")
        # print(self.data._name, self.data) # 返回第一个导入的数据表格，缩写形式
        # print("-------------self.data0-------------")
        # print(self.data0._name, self.data0) # 返回第一个导入的数据表格，缩写形式
        # print("-------------self.datas[0]-------------")
        # print(self.datas[0]._name, self.datas[0]) # 返回第一个导入的数据表格，常规形式

        # print("--------- 打印 self 策略本身的 lines ----------")
        # print(self.lines.getlinealiases())
        # print("--------- 打印 self.datas 第一个数据表格的 lines ----------")
        # print(self.datas[0].lines.getlinealiases())
        # # 计算第一个数据集的s收盘价的20日均线，返回一个 Data feed
        # self.sma = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=20)
        # print("--------- 打印 indicators 对象的 lines ----------")
        # print(self.sma.lines.getlinealiases())
        # print("---------- 直接打印 indicators 对象的所有 lines -------------")
        # print(self.sma.lines)
        # print("---------- 直接打印 indicators 对象的第一条 lines -------------")
        # print(self.sma.lines[0])

    def notify_order(self, order):
        # 未被处理的订单
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 已经处理的订单
        # 注意，如果现金不够的话，订单会被拒接
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, ref:%.0f，Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
                    (order.ref,  # 订单编号
                     order.executed.price,  # 成交价
                     order.executed.value,  # 成交额
                     order.executed.comm,  # 佣金
                     order.executed.size,  # 成交量
                     order.data._name))  # 股票名称
            elif order.issell():
                self.log('SELL EXECUTED, ref:%.0f, Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
                         (order.ref,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          order.executed.size,
                          order.data._name))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(order.status)
            self.log(order.Margin)
            self.log('Order Canceled/Margin/Rejected')

        # 记录没有挂起的订单
        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        # print('sma5', self.sma5[0], self.sma5)
        # print('sma10', self.sma10[0], self.sma10)
        # print('buy_sig', self.buy_sig[0], self.buy_sig)

        # 检查是否有挂起的订单，如果有的话，不能再发起一个订单
        if self.order:
            return

        # 检查是否在市场（有持仓）
        if not self.position:
            # 不在，那么连续3天价格下跌就买点
            if self.dataclose[0] < self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()
                # self.order_target_percent(target=0.95)

        else:
            # 已经在市场，5天后就卖掉。
            if len(self) >= (
                    self.bar_executed + 5):  # 这里注意，Len(self)返回的是当前执行的bar数量，每次next会加1.而Self.bar_executed
                # 记录的最后一次交易执行时的bar位置。
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                data = self.getdatabyname('000001')
                # Keep track of the created order to avoid a 2nd order
                self.order = self.close(data=data)
