from strategy import object_filter
from strategy import filter_strategy
from datasource import yesterday_limit
from datasource import status_checker
from datasource import yesterday_limit as yl


def week_job():
    object_filter.select_object_from_etf(filter_strategy.is_in_week_trend)
    # object_filter.select_plate(filter_strategy.is_in_week_trend)


def week_job2():
    object_filter.select_object_from_my(filter_strategy.is_in_week_trend_buy)
    object_filter.select_object_from_etf(filter_strategy.is_in_week_trend_buy)
    object_filter.select_object_from_plate(filter_strategy.is_in_week_trend_buy)
    object_filter.select_plate(filter_strategy.is_in_week_trend_buy)


status_checker.check_status()
yl.get_and_save()
object_filter.select_object_from_etf(filter_strategy.is_in_week_trend_buy)
# object_filter.select_object_from_my(filter_strategy.is_in_week_trend_buy)
# object_filter.select_plate(filter_strategy.is_in_week_trend)
print('end')
