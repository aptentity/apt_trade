# 昨日涨停
import pandas as pd
from utils import futuUtils as fu
from futu import *
import time
from utils import time_utils as tu


def get_and_save():
    ret, data = fu.quote_context.get_plate_stock('SH.BK0722')
    if ret == RET_OK:
        data['day'] = tu.getdate(0)
        data = data[~data['stock_name'].str.contains('ST')]
        # data.to_csv('../object/yesterday_limit.csv', encoding='utf-8-sig')
        old_data = pd.read_csv('../object/yesterday_limit.csv', index_col=0)
        old_data = old_data[old_data['day'] > tu.getdate(180)]
        new_data = pd.concat([data, old_data], ignore_index=True)
        new_data = new_data.drop_duplicates(subset=['code', 'day'], keep='first')
        new_data.to_csv('../object/yesterday_limit.csv', encoding='utf-8-sig')

