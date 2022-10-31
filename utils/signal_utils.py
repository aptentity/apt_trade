# 获取EMA数据 , cps：close_prices 收盘价集合 days:日期 days=5 5日线
def get_EMA(cps, days):
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