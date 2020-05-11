import pandas as pd
import time
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
from urllib import request
from urllib import parse

def exchange_crawler():
    # 抓取數據
    url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
    form_data = {}
    form_data['erectDate'] = ''
    form_data['nothing'] = ''
    form_data['pjname'] = '港币'
    data = parse.urlencode(form_data).encode('utf-8')
    html = request.urlopen(url, data).read().decode('utf-8')

    # 解析數據
    CNY_exchange_rate = pd.read_html(html)[1]
    CNY_exchange_rate = CNY_exchange_rate.iloc[:20, :7]
    # print(len(cny_exchange_rate))

    CNY_exchange_rate_list = []
    for i in range(len(CNY_exchange_rate)):
        # 存入一般dict
        CNY_exchange_rate_data = {}
        release_date = time.mktime(time.strptime(CNY_exchange_rate.iloc[i][6], '%Y.%m.%d %H:%M:%S'))
        CNY_exchange_rate_data['货币名称'] = CNY_exchange_rate.iloc[i][0]
        CNY_exchange_rate_data['现汇买入价'] = CNY_exchange_rate.iloc[i][1]
        CNY_exchange_rate_data['现钞买入价'] = CNY_exchange_rate.iloc[i][2]
        CNY_exchange_rate_data['现汇卖出价'] = CNY_exchange_rate.iloc[i][3]
        CNY_exchange_rate_data['现钞卖出价'] = CNY_exchange_rate.iloc[i][4]
        CNY_exchange_rate_data['中行折算价'] = CNY_exchange_rate.iloc[i][5]
        CNY_exchange_rate_data['发布时间'] = release_date
        # print(CNY_exchange_rate_data)
        CNY_exchange_rate_list.append(CNY_exchange_rate_data)
    print('now_time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(CNY_exchange_rate_list[0])
    time.sleep(1)

while True:
    exchange_crawler()
    
# influxdb操作
# client = InfluxDBClient('localhost', 8086, 'root', '', 'wetrade')
# print(client.get_list_database()) # 顯示所有數據庫名稱
# client.create_database('testdb') # 創建資料庫
# client.drop_database('testdb') # 刪除資料庫
# print(client.get_list_database()) # 顯示目前有哪些資料庫

# measurements操作
# print(client.query('show measurements')) # 顯示資料庫中目前有那些 measurement
# client.query('drop measurement exchange_rate') # 刪除measurement