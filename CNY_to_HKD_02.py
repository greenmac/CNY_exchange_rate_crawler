import re
import requests

url = 'http://www.boc.cn/sourcedb/whpj/'
html = requests.get(url).content.decode("utf-8") # 获取网页源码

data = re.findall('<td>(.*?)</td>', html) # 获取所有币种牌价
# dollarData = data[-16:-8] # 获取美元牌价
dollarData = data[56:63] # 获取港币牌价
# print(dollarData)

keys2 = ['外币', '汇买价', '钞买价', '汇卖价', '钞卖价', '中间价', '发布日期', '发布时间']
dictDollar = dict(zip(keys2, dollarData))
# print(dictDollar)

for k, v in dictDollar.items():
    print((k+':').ljust(6), str(v))