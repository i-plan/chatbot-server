from flask import Flask, render_template, jsonify, make_response,current_app
from flask_restful import Api, Resource

from app.api import user,passport,chat
from app.storage import  get_mongo
import asyncio
from websockets.server import serve

class Ping(Resource):
    def get(self):
        return make_response("ping成功")

def init(csrf_protect,app: Flask):
    api = Api(app, decorators=[csrf_protect.exempt])
    # api = Api(app)
    api.add_resource(Ping,"/ping" ,endpoint='ping')
    api.add_resource(user.UserApi, "/api/user", "/api/user/<int:user_id>/<string:action>", "/api/user/<string:action>",
                     "/api/user/<int:user_id>", endpoint='user')
    api.add_resource(passport.PassportAPI, '/api/passport', '/api/passport/','/api/passport/<string:action>', endpoint='passport')
    api.add_resource(chat.ChatAPI,'/api/chat/<string:action>', endpoint='chat')

    async def main():
        async with serve(chat.ChatAPI.onMessage, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    asyncio.run(main())
