import schedule
from futu import *
from job_old import stock_filter
from strategy import object_filter
from strategy import filter_strategy
from utils import futuUtils as fu
from utils import dingding as dd
from datasource import yesterday_limit as yl


def day_job():
    object_filter.select_object_from_my(filter_strategy.is_in_day_week_trend_buy)
    object_filter.select_object_from_etf(filter_strategy.is_in_day_week_trend_buy)
    object_filter.select_object_from_plate(filter_strategy.is_in_day_week_trend_buy,object_filter.get_hot_plate())
    object_filter.select_plate(filter_strategy.is_in_day_week_trend_buy)
    # selectCode = object_filter.select_object_from_hot_plate(filter_strategy.is_in_day_week_trend_buy)
    # fu.quote_context.modify_user_security("选股", ModifyUserSecurityOp.ADD, selectCode[::-1])

    print("day_job done")


def day_job2():
    object_filter.select_object_from_my(filter_strategy.is_in_day_trend_buy)
    object_filter.select_object_from_etf(filter_strategy.is_in_day_trend_buy)
    object_filter.select_object_from_yesterday_limit(40, 7, filter_strategy.is_in_day_trend_buy, '选股')

    object_filter.select_object_from_my(filter_strategy.is_in_week_trend_buy)
    object_filter.select_object_from_etf(filter_strategy.is_in_week_trend_buy)
    object_filter.select_object_from_yesterday_limit(90, 30, filter_strategy.is_in_week_trend_buy, '选股')

    object_filter.select_object_from_etf(filter_strategy.is_week_over_fall)
    object_filter.select_plate(filter_strategy.is_week_over_fall)

    object_filter.select_object_from_my(filter_strategy.is_back_low_before)
    object_filter.select_object_from_etf(filter_strategy.is_back_low_before)

    print("day_job2 done")


def short_job():
    yl.get_and_save()
    selectCode = object_filter.select_object_from_yesterday_limit(10, 0, filter_strategy.is_in_short_buy)
    selectCode2 = object_filter.select_object_from_my_select(filter_strategy.is_in_short_buy)
    print(selectCode)
    print(selectCode2)
    selectCode = selectCode + selectCode2
    print(selectCode)
    if selectCode and len(selectCode) > 0:
        fu.quote_context.modify_user_security('超短', ModifyUserSecurityOp.ADD, selectCode[::-1])
        dd.send_notice('有买入信号')
    print("short_job done")


logging.basicConfig(level=logging.INFO,
                    filename='./main_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')

object_filter.select_object_from_plate(filter_strategy.is_in_day_week_trend_buy, object_filter.get_hot_plate())

schedule.every(20).minutes.do(short_job)
schedule.every().day.at("14:10").do(day_job2)
schedule.every().day.at("14:30").do(day_job)

while True:
    print('---------------')
    schedule.run_pending()
    time.sleep(10)
