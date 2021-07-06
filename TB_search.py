'''
https://suggest.taobao.com/sug?code=utf-8&q=%E7%9F%AD%E8%A2%96&_ksTS=1625559056875_511&callback=jsonp512&k=1&area=c2c&bucketid=6
'''

import re
import requests
import json
from urllib import parse
from flask import Flask, jsonify, request


@app.route('/get_tb_word', methods=['post'])
def get_tb_word(keyword):
    keyword = parse.quote(keyword)
    url = 'https://suggest.taobao.com/sug?code=utf-8&q=' + keyword + '&_ksTS=1625559056875_511&callback=jsonp512'

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"
    }

    rule = re.compile(r'json.*?\((.*?)\)', re.S)
    resp = requests.get(url=url, headers=headers)
    text = resp.text
    text = rule.findall(text)[0]

    json_page = json.loads(text)     # json格式
    source_result_list = json_page['result']

    result_list = []                # 字符串列表
    for data in source_result_list:
        result_list.append(data[0])

    result_dict = {}                # 字典格式
    length = len(result_list)
    result_dict['length'] = length
    result_dict['data'] = result_list
    print(result_dict)

    return jsonify(result_dict)


if __name__ == '__main__':
    app = Flask(__name__)
    app.run(host='127.0.0.1', port=5000, debug=True)

# get_tb_word("短袖")