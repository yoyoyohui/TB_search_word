import sys
import json
import random
import requests
from urllib import parse
from sanic import Blueprint
from sanic import Sanic
from worker.request_body.common import global_catch_exception

pdd_search_word = Blueprint('pdd_search_word', url_prefix='/pddSearch')

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
]

# 拼多多搜索词联想接口
@pdd_search_word.route("/pddSearchWord", methods=["GET"])
@global_catch_exception
async def post_json(request):
    keyword = request.args.get('keyWord', '')
    item = {}
    if keyword:
        keyword = parse.quote(keyword)  # 编码
        url = 'http://mobile.pinduoduo.com/proxy/api/search_suggest?pdduid=0&query={}&plat=H5&source=index&is_change=1&goods_id_list=&sug_srch_type=0'
        headers = {'User-Agent': random.choice(user_agent_list)}
        response = requests.get(url=url.format(keyword), headers=headers).text
        try:
            json_data = json.loads(response)
            results = json_data['suggest']
            item['count'] = len(results)
            item['data'] = results
            return json.dumps(item)
        except Exception:
            pass
    else:
        return {'code': 401, 'msg': '请求参数错误'}



if __name__ == '__main__':
    app = Sanic(__name__)
    app.blueprint(pdd_search_word)
    debug = False if sys.platform == 'linux' else True
    app.run(host='0.0.0.0', port=8086, debug=debug)


