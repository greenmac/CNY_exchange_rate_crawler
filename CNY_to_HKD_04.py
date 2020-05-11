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
    exchange_rate = pd.read_html(html)[1]
    exchange_rate = exchange_rate.iloc[:, :7]
    exchange_rate_last = exchange_rate.iloc[0]

    exchange_rate_data = {}
    exchange_rate_data['货币名称'] = exchange_rate_last[0]
    exchange_rate_data['现汇买入价'] = exchange_rate_last[1]
    exchange_rate_data['现钞买入价'] = exchange_rate_last[2]
    exchange_rate_data['现汇卖出价'] = exchange_rate_last[3]
    exchange_rate_data['现钞卖出价'] = exchange_rate_last[4]
    exchange_rate_data['中行折算价'] = exchange_rate_last[5]
    exchange_rate_data['发布时间'] = exchange_rate_last[6]

    # 數據格式
    release_time = time.mktime(time.strptime(exchange_rate_data['发布时间'], '%Y.%m.%d %H:%M:%S'))
    data = [
        {
            'measurement': 'exchange_rate',
            'tags': {
                'currency': 'HKD',
            },
            'fields': {
                'names': exchange_rate_data['货币名称'],
                'remittance_buying': exchange_rate_data['现汇买入价'],
                'cash_buying': exchange_rate_data['现钞买入价'],
                'remittance_selling': exchange_rate_data['现汇卖出价'],
                'cash_selling': exchange_rate_data['现钞卖出价'],
                'boc_discount': exchange_rate_data['中行折算价'],
                'release_time': release_time,
            }
        }
    ]

    # 寫入influxdb
    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb')
    client.create_database('testdb')

    result_data = client.query(f'select * from exchange_rate where release_time={release_time};')
    if not result_data:
        client.write_points(data)

    result = client.query('select * from exchange_rate limit 1;')
    for point in result.get_points():
        print('now_time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(point)
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