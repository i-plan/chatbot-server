"""
openai api: https://platform.openai.com/docs/api-reference/chat/create?lang=python
"""
import datetime
import json
import time

from flask_restful import Resource, abort
from flask import request, make_response, jsonify, current_app, session
import os
import openai
from flask_sock import Sock

from app import LRUCache
from app.api.wx_auth import get_openid
from app.storage.user import get_chat_users
from app.util import l

openai.api_key = os.getenv("OPENAI_API_KEY")
# https://github.com/justjavac/openai-proxy
openai.api_base = "https://closeai.deno.dev/v1"
use_limit = 5

sock = Sock()

lrucache = LRUCache(4000)
@sock.route('/chat')
def chat(ws):
    while True:
        d = json.loads(ws.receive())
        openid = lrucache.get(d['wxAuthCode'])
        print('1', d['wxAuthCode'], openid)
        if not openid:
            openid = get_openid(d['wxAuthCode'])
            lrucache.put(d['wxAuthCode'], openid)
            print('2', d['wxAuthCode'], openid)
        if not openid:
            l.i("not openid,400 openid 为空，需要重新授权登录")
            ws.send(json.dumps({
                'result': {
                    'code': 402,
                    'msg': "openid 为空，需要重新授权登录"
                }}))
        else:
            ws.send(chatai(openid, d['content']))

def chatai(openid, content):
    with current_app.app_context():
        u = get_chat_users().find_one({'openid': openid}, {'_id': False})
        if not u:
            l.i("用户不存在")
            return json.dumps({
                'result': {
                    'code': 401,
                    'msg': "用户不存在"
                }})

        usage = u.get('usage', 1)
        print(usage, usage % use_limit, usage // use_limit)
        if not usage % use_limit:
            latest_usage_time = time.mktime(time.strptime(u['latest_usage_time'], "%Y-%m-%d %H:%M:%S"))
            if datetime.datetime.now() - datetime.datetime.fromtimestamp(latest_usage_time) < datetime.timedelta(
                    days=1):
                # 限制访问
                return json.dumps({
                    'result': {
                        'code': 403,
                        'msg': f'只能使用{use_limit}次，明天加重新赋予你{use_limit}次'
                    }
                })
            else:
                u['usage'] = 1
        u['usage'] += 1
        u['latest_usage_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        get_chat_users().update_one({'openid': openid}, {'$set': u})

        l.i(f"txt question:{content}")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}])
        l.i(f"txt answer:{completion.choices[0].message['content']}")
        return json.dump({
            'result': {
                'code': 200,
                'msg': completion.choices[0].message['content']
            }
        })

        # return json.dumps({
        #     'result': {
        #         'code': 200,
        #         'msg': """
        #         後視鏡裏的世界 越來越遠的道別
        #         你轉身向背 側臉還是很美
        #         我用眼光去追 竟聽見你的淚
        #         在車窗外面徘徊 是我錯失的機會
        #         你站的方位 跟我中間隔著淚
        #         街景一直在後退 你的崩潰在窗外零碎
        #         """
        #     }
        # })


class ChatAPI(Resource):
    actions = ['txt']

    # @auth
    def post(self, **kw):
        """
        /chat/txt
        :return:
        """
        if kw['action'] in self.actions:
            self_action = getattr(self, kw['action'].lower())
            # return self_action(kw.get('openid'))
            d = request.get_json()
            return self_action(request.headers.get('X-WX-OPENID'), d['content'])
        else:
            abort(404)

    def txt(self, openid, content):
        return chatai(openid, content)
