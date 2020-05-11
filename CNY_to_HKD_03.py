from pyquery import PyQuery as pq

url = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
doc = pq(url)
print(doc)

