'''
http://mobile.pinduoduo.com/proxy/api/search_suggest?pdduid=0&query=%E7%9F%AD%E8%A2%96&plat=H5&source=index&is_change=1&goods_id_list=&sug_srch_type=0

'''

import re
import requests
import json
from urllib import parse

keyword = "裙子"
keyword = parse.quote(keyword)
url = 'http://mobile.pinduoduo.com/proxy/api/search_suggest?pdduid=0&query='+keyword+'&plat=H5&source=index&is_change=1&goods_id_list=&sug_srch_type=0'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"
}

resp = requests.get(url=url, headers=headers)
text = resp.text
json_page = json.loads(text)     # json格式
result_list = json_page['suggest']
print(result_list)
