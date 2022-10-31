import os

import trade_notice
import trend_bull
from utils import futuUtils as fu
import shelve

# trend_bull.trend_bull(0)

# trade_notice.trade_notice_us()

# print(fu.is_ch_normal_trading_time())
# print(fu.is_us_normal_trading_time())
# trade_notice.trade_notice_cn()

# os.rename('test.txt', 'high.txt')
# os.remove('high.txt')

# import logging
# logging.basicConfig(level=logging.INFO,
#                     filename='./log.txt',
#                     filemode='a',
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d]: %(message)s')
# # use logging
# logging.info('这是 loggging info message')
# logging.debug('这是 loggging debug message')
# logging.warning('这是 loggging a warning message')
# logging.error('这是 an loggging error message')
# logging.critical('这是 loggging critical message')

# array = ['12', 'ab', 'cc']
# print('ab' in array)

alien_0 = {'color': 'green', 'points':5}
a = 'color'
print(f"get color {alien_0[a]}")
print(f"get points {alien_0['points']}")

