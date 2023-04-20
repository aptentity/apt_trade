# 相关走势
import logging

import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import kendalltau

logging.basicConfig(level=logging.INFO,
                    filename='corr_log.txt',
                    filemode='a',
                    format='%(message)s')

logging.info('--------------------------------------')
logging.info('--------------------------------------')
week_data = pd.read_csv('../data/SH.000001_mon.csv')


# print(day_data)

def get_corr(data, column):
    result = []
    result_5 = []
    start_index = 30
    long_size = 30
    middle_size = 10
    short_size = 5
    threshold = 0.6
    data_calculate = data[column]
    length = len(data_calculate)

    for n in range(length - start_index - long_size):
        max_pearsonr = 0
        index = 0
        begin = start_index + n
        today_index = begin + long_size
        # print(data['time_key'].iloc[today_index])
        for i in range(begin - long_size):
            long_pc = spearmanr(data_calculate.iloc[i:i + long_size],
                                data_calculate.iloc[today_index - long_size:today_index])
            middle_pc = spearmanr(data_calculate.iloc[i + long_size - middle_size:i + long_size],
                                  data_calculate.iloc[today_index - middle_size:today_index])
            short_pc = spearmanr(data_calculate.iloc[i + long_size - short_size:i + long_size],
                                 data_calculate.iloc[today_index - short_size:today_index])
            if long_pc[0] > threshold and middle_pc[0] > threshold and short_pc[0] > threshold:
                if long_pc[0] + middle_pc[0] + short_pc[0] > max_pearsonr:
                    max_pearsonr = long_pc[0] + middle_pc[0] + short_pc[0]
                    index = i
        if max_pearsonr > threshold * 3:
            log_text = str(data['time_key'].iloc[today_index]) + ';' + str(
                data['time_key'].iloc[index + long_size])
            print(log_text)
            logging.info(log_text)
            if today_index + 10 < length:
                pc10 = spearmanr(data_calculate.iloc[index + long_size:index + long_size + 10],
                                 data_calculate.iloc[today_index:today_index + 10])
                pc5 = spearmanr(data_calculate.iloc[index + long_size:index + long_size + 5],
                                data_calculate.iloc[today_index:today_index + 5])
                print(' 相关系数：' + str(pc10[0]), ';', pc5[0])
                result.append(pc10[0])
                result_5.append(pc5[0])

    if len(result) > 0:
        print(sum(result) / len(result))
        print(sum(result_5) / len(result))
        print(len(result))


get_corr(week_data, 'close')

