from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
import pandas as pd
# import requests

# 抓取數據
url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
# url = 'https://www.ptt.cc/bbs/NBA/index.html'
form_data = {}
form_data['erectDate'] = ''
form_data['nothing'] = ''
form_data['pjname'] = '港币'
data = parse.urlencode(form_data).encode('utf-8')
# print(data)
html = request.urlopen(url, data).read()
# print(html)
# html = requests.get(url)
# print(html)
soup = BeautifulSoup(html,'html.parser')
# soup = BeautifulSoup(html.text, 'lxml')
# print(soup)
                   
# 解析數據
div = soup.find('div', attrs={'class':'BOC_main publish'})
table = div.find('table')
# th = table.find_all('th')
# tr = table.find_all('tr')
# td = table.find_all('td')
item_list = table.find_all('td')
# print(item_list)
num=len(item_list)
# print(num)

names = [] # 货币名称
remittance_buying = [] # 现汇买入价
cash_buying = [] # 现钞买入价
remittance_selling = [] # 现汇卖出价
cash_selling = [] # 现钞卖出价
boc_discount = [] # 中行折算价
release_time = [] # 发布时间

for i in range(0, num):
    names.append(item_list[i].text)
print(names)