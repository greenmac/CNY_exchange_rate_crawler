import requests
import pandas as pd
from bs4 import BeautifulSoup
#from lxml import etree
#import time
#from time import sleep
url = 'http://quote.fx678.com/exchange/WH'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

response=requests.get(url,headers=headers)
soup=BeautifulSoup(response.content, 'lxml')

item_list=soup.find_all('td')#找到网页表格中的所有内容
print(item_list)
num=len(item_list)
# print(num)

names=[]                  #存放外汇产品的名称
price_new=[]              #外汇产品的最新价格
price_change=[]           #外汇产品涨跌值
price_percentage=[]       #外汇产品的涨跌幅度
price_high=[]             #外汇产品当日最高价
price_low=[]              #外汇产品当日最低价
price_yesterday=[]        #外汇产品昨日收盘价
time_update=[]            #更新时间

for i in range(0,num,8):#从0位置开始，每隔7个位置就是产品名称
    names.append(item_list[i].text)
# print(names)