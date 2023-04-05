"""
openai api: https://platform.openai.com/docs/api-reference/chat/create?lang=python
"""
import json

from flask_restful import Resource, abort
from flask import request, make_response, jsonify
import os
import openai

from app.util import l

openai.api_key = os.getenv("OPENAI_API_KEY")
# https://github.com/justjavac/openai-proxy
# openai.api_base = "https://closeai.deno.dev/v1"


class ChatAPI(Resource):
    actions = ['txt']

    def post(self, action):
        """
        /chat/txt
        :return:
        """
        if action in self.actions:
            self_action = getattr(self, action.lower())
            return self_action()
        else:
            abort(404)

    def txt(self):
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
