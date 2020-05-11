import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
from influxdb import InfluxDBClient


def exchange_crawler():
    # 抓取數據
    url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
    form_data = {}
    form_data['erectDate'] = ''
    form_data['nothing'] = ''
    form_data['pjname'] = '港币'
    data = parse.urlencode(form_data).encode('utf-8')
    html = request.urlopen(url, data).read().decode('utf-8')
    soup = BeautifulSoup(html,'html.parser')

    # 解析數據
    div = soup.find('div', attrs = {'class':'BOC_main publish'})
    table = div.find('table')
    tr = table.find_all('tr')
    exchange_rate_last = tr[1].find_all('td')

    exchange_rate_data = {}
    exchange_rate_data['货币名称'] = exchange_rate_last[0].get_text()
    exchange_rate_data['现汇买入价'] = exchange_rate_last[1].get_text()
    exchange_rate_data['现钞买入价'] = exchange_rate_last[2].get_text()
    exchange_rate_data['现汇卖出价'] = exchange_rate_last[3].get_text()
    exchange_rate_data['现钞卖出价'] = exchange_rate_last[4].get_text()
    exchange_rate_data['中行折算价'] = exchange_rate_last[5].get_text()
    exchange_rate_data['发布时间'] = exchange_rate_last[6].get_text()

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
    # print(type(data[0]['fields']['names']))
    # print(type(data[0]['fields']['remittance_buying']))
    # print(type(data[0]['fields']['cash_buying']))
    # print(type(data[0]['fields']['remittance_selling']))
    # print(type(data[0]['fields']['cash_selling']))
    # print(type(data[0]['fields']['boc_discount']))
    # print(type(data[0]['fields']['release_time']))
    
    
    # 寫入influxdb
    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb')
    client.create_database('testdb')
    
    result_data = client.query(f'select * from exchange_rate where release_time={release_time};')
    if not result_data:
        client.write_points(data)

    result = client.query('select * from exchange_rate order by time desc limit 1;')
    # result = client.query('select * from exchange_rate;')
    for point in result.get_points():
        print('now_time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(point)
        # pass
    time.sleep(1)

while True:
    exchange_crawler()
# exchange_crawler()

# influxdb操作
# client = InfluxDBClient('localhost', 8086, 'root', '', 'wetrade')
# print(client.get_list_database()) # 顯示所有數據庫名稱
# client.create_database('testdb') # 創建資料庫
# client.drop_database('testdb') # 刪除資料庫
# print(client.get_list_database()) # 顯示目前有哪些資料庫

# measurements操作
# print(client.query('show measurements')) # 顯示資料庫中目前有那些 measurement
# client.query('drop measurement exchange_rate') # 刪除measurement