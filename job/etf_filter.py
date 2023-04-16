import requests
import pandas as pd


def get_etf_list():
    r = requests.get('http://www.etf.group/data/api1.php?page=1&limit=10')
    print(r)
    response_dict = r.json()
    data = response_dict['rows']['item']
    print(data)
    b = pd.DataFrame(data)
    print(b)
    b.to_csv('etf.csv')


def get_lof_list():
    r = requests.get('http://www.etf.group/data/api1.php?page=1&limit=10')
    print(r)
    response_dict = r.json()
    data = response_dict['rows']['item']
    print(data)
    b = pd.DataFrame(data)
    print(b)
    b.to_csv('lof.csv')


etf = pd.read_csv('etf_new.csv')
new_etf = etf[etf['avgamount'] > 5000]
# new_etf = new_etf.sort_values(by='name')
print(new_etf)
