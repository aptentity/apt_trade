import schedule
from futu import *
from job_old import stock_filter
from strategy import object_filter
from strategy import filter_strategy
from utils import futuUtils as fu
from utils import dingding as dd
from datasource import yesterday_limit as yl
import pandas as pd

week_subject_df = pd.DataFrame(columns=['name', 'code'])
week_subject_df.loc[len(week_subject_df)] = ['千禾味业', 'SH.603027']
week_subject_df.loc[len(week_subject_df)] = ['中国人保', 'SH.601309']
print(week_subject_df)


def day_job():
    yl.get_and_save()

    # 选择周线走好的ETF
    # fu.delete_user_security('ETF')
    object_filter.select_from_subject_good(filter_strategy.is_in_day_trend_buy)
    object_filter.select_from_subject_good(filter_strategy.is_day_start_up)
    # object_filter.select_object_from_plate(filter_strategy.is_in_day_week_trend_buy)
    # object_filter.select_object_from_etf(filter_strategy.is_in_week_trend_buy)
    # object_filter.select_object_from_etf(filter_strategy.is_in_day_trend_buy)
    # object_filter.select_object_from_etf(filter_strategy.is_in_week_trend)

    object_filter.select_object_from_yesterday_limit(40, 7, filter_strategy.is_in_day_trend_buy, '选股')
    object_filter.select_object_from_yesterday_limit(90, 50, filter_strategy.is_in_week_trend_buy, '选股')
    fu.quote_context.modify_user_security('选股', ModifyUserSecurityOp.ADD, object_filter.get_hot_plate())

    print("day_job done")


def short_job():
    selectCode = object_filter.select_object_from_my_select(filter_strategy.is_in_short_buy)
    if selectCode and len(selectCode) > 0:
        fu.quote_context.modify_user_security('超短', ModifyUserSecurityOp.ADD, selectCode[::-1])
        dd.send_notice('有买入信号')
    print("short_job done")


logging.basicConfig(level=logging.INFO,
                    filename='./main_log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')

day_job()
schedule.every(20).minutes.do(short_job)
schedule.every().day.at("14:30").do(day_job)

while True:
    # print('---------------')
    schedule.run_pending()
    time.sleep(10)
