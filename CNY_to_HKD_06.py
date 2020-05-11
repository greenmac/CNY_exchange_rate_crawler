import pandas as pd
import time
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
from urllib import request
from urllib import parse


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
    # CNY_exchange_rate_data = {}
    # CNY_exchange_rate_data['货币名称'] = CNY_exchange_rate.iloc[i][0]
    # CNY_exchange_rate_data['现汇买入价'] = CNY_exchange_rate.iloc[i][1]
    # CNY_exchange_rate_data['现钞买入价'] = CNY_exchange_rate.iloc[i][2]
    # CNY_exchange_rate_data['现汇卖出价'] = CNY_exchange_rate.iloc[i][3]
    # CNY_exchange_rate_data['现钞卖出价'] = CNY_exchange_rate.iloc[i][4]
    # CNY_exchange_rate_data['中行折算价'] = CNY_exchange_rate.iloc[i][5]
    # CNY_exchange_rate_data['发布时间'] = CNY_exchange_rate.iloc[i][6]
    # print(CNY_exchange_rate_data)
    # CNY_exchange_rate_list.append(CNY_exchange_rate_data)
# print(CNY_exchange_rate_list)
    # # 數據格式
    # # release_time = time.mktime(time.strptime(exchange_rate_data['发布时间'], '%Y.%m.%d %H:%M:%S'))
    
    # 存入influxdb dict
    CNY_exchange_rate_data = [
        {
            'measurement': 'exchange_rate',
            'tags': {
                'currency': 'HKD',
            },
            'fields': {
                'names': CNY_exchange_rate.iloc[i][0],
                'buy': CNY_exchange_rate.iloc[i][1],
                'sell': CNY_exchange_rate.iloc[i][3],
            }
        }
    ]
    # print(CNY_exchange_rate_data)
    CNY_exchange_rate_list.append(CNY_exchange_rate_data)    
# print(CNY_exchange_rate_list)
# print(len(CNY_exchange_rate_list))
# print(CNY_exchange_rate_data)
# # 寫入influxdb
client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb')
client.drop_database('testdb')
client.create_database('testdb')

for i in range(len(CNY_exchange_rate_list)):
    client.write_points(CNY_exchange_rate_list[i])

result = client.query('select * from exchange_rate;')
print(list(result.get_points()))
# for point in result.get_points():
#     print('now_time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     print(point)
# time.sleep(30)

# while True:
#     exchange_crawler()
    
# influxdb操作
# client = InfluxDBClient('localhost', 8086, 'root', '', 'wetrade')
# print(client.get_list_database()) # 顯示所有數據庫名稱
# client.create_database('testdb') # 創建資料庫
# client.drop_database('testdb') # 刪除資料庫
# print(client.get_list_database()) # 顯示目前有哪些資料庫

# measurements操作
# print(client.query('show measurements')) # 顯示資料庫中目前有那些 measurement
# client.query('drop measurement exchange_rate') # 刪除measurement