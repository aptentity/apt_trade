# 昨日涨停
import pandas as pd
from utils import futuUtils as fu
from futu import *
import time
from utils import time_utils as tu


def get_and_save():
    ret, data = fu.quote_context.get_plate_stock('SH.BK0722')
    if ret != RET_OK:
        print('error:', data)
        return
    # 保存昨日连板的股票
    data['day'] = tu.get_today()
    data = data[~data['stock_name'].str.contains('ST')]
    old_data = pd.read_csv('../object/yesterday_limit.csv', index_col=0)
    old_data = old_data[old_data['day'] > tu.getdate(180)]
    new_data = pd.concat([data, old_data], ignore_index=True)
    new_data = new_data.drop_duplicates(subset=['code', 'day'], keep='first')
    new_data.to_csv('../object/yesterday_limit.csv', encoding='utf-8-sig')

    # 保存股票的所属板块
    ret, data_plate = fu.quote_context.get_owner_plate(data['code'].values.tolist())
    if ret != RET_OK:
        print('error:', data_plate)
        return
    data_plate = data_plate[
        (data_plate['plate_type'].isin(['CONCEPT', 'INDUSTRY'])) & ~data_plate['plate_code'].isin(
            ['SH.BK0722', 'SH.BK0439', 'SH.BK0338', 'SH.BK0621', 'SH.BK0344', 'SH.BK0551'])]
    data_plate['day'] = tu.get_today()
    old_data_plate = pd.read_csv('../object/yesterday_limit_plate.csv', index_col=0)
    old_data_plate = old_data_plate[old_data_plate['day'] > tu.getdate(180)]
    new_data_plate = pd.concat([data_plate, old_data_plate], ignore_index=True)
    new_data_plate = new_data_plate.drop_duplicates(subset=['code', 'plate_code', 'day'], keep='first')
    new_data_plate.to_csv('../object/yesterday_limit_plate.csv', encoding='utf-8-sig')
    # data_plate.to_csv('../object/yesterday_limit_plate.csv', encoding='utf-8-sig')


# get_and_save()
