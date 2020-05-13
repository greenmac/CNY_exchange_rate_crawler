import requests
import json

stock_code = 'sz000001'
url = f'http://hq.sinajs.cn/list={stock_code}'
res = requests.get(url)
res_text = res.text
res_json = json.dumps(res_text)

print(res_text[4])
print('type:', type(res_text))

# print(res_json)
# print('type:', type(res_json))