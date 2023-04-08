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

from app.api.wx_auth import get_openid
from app.storage.user import get_chat_users
from app.util import l

openai.api_key = os.getenv("OPENAI_API_KEY")
# https://github.com/justjavac/openai-proxy
openai.api_base = "https://closeai.deno.dev/v1"

use_limit = 5


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
            return self_action(request.headers.get('X-WX-OPENID'))
        else:
            abort(404)

    def txt(self, openid):
        with current_app.app_context():
            u = get_chat_users().find_one({'openid': openid}, {'_id': False})
            if not u:
                l.i("用户不存在")
                return jsonify({
                    'result': {
                        'code': 401,
                        'msg': "用户不存在"
                    }})

            usage = u.get('usage', 1)
            print(usage, usage % use_limit, usage // use_limit)
            if not usage % use_limit:
                latest_usage_time = time.mktime(time.strptime(u['latest_usage_time'], "%Y-%m-%d %H:%M:%S"))
                if datetime.datetime.now() - datetime.datetime.fromtimestamp(latest_usage_time)  < datetime.timedelta(days = 1) :
                    # 限制访问
                    return jsonify({
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
            d = request.get_json()
            l.i(f"txt question:{d['content']}")
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": d['content']}])
            l.i(f"txt answer:{completion.choices[0].message['content']}")
            return jsonify({
                'result': {
                    'code': 200,
                    'msg': completion.choices[0].message['content']
                }
            })

            # return jsonify({
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
    @staticmethod
    async def onMessage(websocket):
        async for message in websocket:
            await websocket.send(message)
