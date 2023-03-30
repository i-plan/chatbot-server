"""
openai api: https://platform.openai.com/docs/api-reference/chat/create?lang=python
"""
from flask_restful import Resource, abort
from flask import request
import os
import openai

from app.util import l

openai.api_key = os.getenv("OPENAI_API_KEY")
#https://github.com/justjavac/openai-proxy
# openai.api_base = "https://closeai.deno.dev/v1"

class ChatAPI(Resource):
    actions = ['txt']

    def post(self, action = None):
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
        txt = request.args.get('content')
        l.i(f"content:{txt}")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": txt}])
        l.i(f"content:{completion.choices[0].message}")
        return completion.choices[0].message
