# 获取EMA数据 , cps：close_prices 收盘价集合 days:日期 days=5 5日线
def get_EMA(cps, days):
    print(cps)
    emas = cps.copy()  # 创造一个和cps一样大小的集合
    for i in range(len(cps)):
        if i == 0:
            emas[i] = cps[i]
        if i > 0:
            emas[i] = ((days - 1) * emas[i - 1] + 2 * cps[i]) / (days + 1)
    return emas


def cal_macd(close):
    ema12 = get_EMA(close, 12)
    ema26 = get_EMA(close, 26)
    # ema12 = ta.ma('ema', close, length=12)
    # ema26 = ta.ma('ema', close, length=26)
    dif = ema12 - ema26
    dea = get_EMA(dif, 9)
    macd = (dif - dea) * 2
    return macd


def macd_down(close):
    result = cal_macd(close)
    if result.iloc[-1] < result.iloc[-2] < result.iloc[-3]:
        return True
    return False


def macd_up(close):
    result = cal_macd(close)
    if len(result) < 4:
        return False
    return result.iloc[-1] > result.iloc[-2] > result.iloc[-3] < result.iloc[-4] and result.iloc[-3] < 0


def macd_death_cross(close):
    result = cal_macd(close)
    if result.iloc[-1] < 0 < result.iloc[-2]:
        return True
    return False


def macd_king_cross(close):
    result = cal_macd(close)
    if result.iloc[-1] > 0 > result.iloc[-2]:
        return True
    return False


def ema_king_cross(close):
    ema10 = get_EMA(close, 10)
    ema30 = get_EMA(close, 30)
    ema72 = get_EMA(close, 72)
    base = (ema30 + ema72) / 2
    return ema10.iloc[-1] > base.iloc[-1] and ema10.iloc[-2] < base.iloc[-2]


def ema_death_cross(close):
    ema10 = get_EMA(close, 10)
    ema30 = get_EMA(close, 30)
    ema72 = get_EMA(close, 72)
    base = (ema30 + ema72) / 2
    return ema10.iloc[-1] < base.iloc[-1] and ema10.iloc[-2] > base.iloc[-2]


def ema_below_base2(close, short=10, middle=30, high=72, day=1):
    ema10 = get_EMA(close, short)
    ema30 = get_EMA(close, middle)
    ema72 = get_EMA(close, high)
    base = (ema30 + ema72) / 2
    for i in range(day):
        if ema10.iloc[-1 - i] > base.iloc[-1]:
            return False
    return True


def ema_above_base2(close, short=10, middle=30, high=72, day=1):
    ema10 = get_EMA(close, short)
    ema30 = get_EMA(close, middle)
    ema72 = get_EMA(close, high)
    base = (ema30 + ema72) / 2
    for i in range(day):
        if ema10.iloc[-1 - i] < base.iloc[-1]:
            return False
    return True


def ema_above_base(close):
    ema10 = get_EMA(close, 10)
    ema30 = get_EMA(close, 30)
    ema72 = get_EMA(close, 72)
    base = (ema30 + ema72) / 2
    return ema10.iloc[-1] > base.iloc[-1]


def ema_below_base(close):
    ema10 = get_EMA(close, 10)
    ema30 = get_EMA(close, 30)
    ema72 = get_EMA(close, 72)
    base = (ema30 + ema72) / 2
    return ema10.iloc[-1] < base.iloc[-1]

    # 趋势底部


def qushi_dibu(close):
    ema10 = get_EMA(close, 10)
    ema30 = get_EMA(close, 30)
    ema72 = get_EMA(close, 72)
    base = (ema30 + ema72) / 2
    count = 0
    for i in range(0, 5):
        if base.iloc[-1 - i] > ema10.iloc[-1 - i]:
            count = count + 1
    if count < 3:
        result = cal_macd(close)
        if result.iloc[-1] > result.iloc[-2] and result.iloc[-2] < 0:
            return True
    return False

    # 超跌


def chaodie(close, low):
    ema20 = get_EMA(close, 20)
    return low.iloc[-1] < ema20.iloc[-1] * 0.8

    # count天内出现超卖


def over_sold(close, low, count=1):
    ema20 = get_EMA(close, 20)
    for i in range(count):
        if low.iloc[-1 - i] < ema20.iloc[-1 - i] * 0.8:
            return True
    return False

    # count天内出现超买


def over_bought(close, high, count=1):
    ema20 = get_EMA(close, 20)
    for i in range(count):
        if high.iloc[-1 - i] > ema20.iloc[-1 - i] * 1.2:
            return True
    return False
