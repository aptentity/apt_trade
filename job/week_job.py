from strategy import object_filter
from strategy import filter_strategy
from datasource import yesterday_limit
from datasource import status_checker


def week_job():
    object_filter.select_object_from_etf(filter_strategy.is_in_week_trend)
    # object_filter.select_plate(filter_strategy.is_in_week_trend)


def week_job2():
    object_filter.select_object_from_my(filter_strategy.is_in_week_trend_buy)
    object_filter.select_object_from_etf(filter_strategy.is_in_week_trend_buy)
    object_filter.select_object_from_plate(filter_strategy.is_in_week_trend_buy)
    object_filter.select_plate(filter_strategy.is_in_week_trend_buy)


status_checker.check_status()
# yesterday_limit.get_and_save()
# print(object_filter.get_hot_plate())
object_filter.select_object_from_etf(filter_strategy.is_in_week_trend_buy)
object_filter.select_object_from_my(filter_strategy.is_in_week_trend_buy)
# object_filter.select_plate(filter_strategy.is_in_week_trend)
print('end')
