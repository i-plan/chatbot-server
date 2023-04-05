import json

import requests
from flask import jsonify, request, current_app
from flask_restful import Resource
from app.storage import get_mongo
from app.form.user import RegistrationForm
from app.storage import user as user_dao

from sqlalchemy.ext.declarative import DeclarativeMeta

from app.util import l


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class UserApi(Resource):
    def get(self, user_id=None):
        # print(json.dumps(User.query.all(),cls= AlchemyEncoder))
        # return jsonify({
        #     'code': 1,
        #     'data': user_dao.get(id=user_id) if user_id else user_dao.get()
        # })
        auth_code = request.args['code']
        openid = self.get_openid(auth_code)
        if not openid:
            l.i("not openid,400 获取失败")
            return jsonify({
                'result': {
                    'code': 400,
                    'msg': "获取失败"
                }})

        with current_app.app_context():
            c = self.get_chat_users()
            u = c.find_one({'openid': openid}, {'_id': False})
            if not u:
                l.i("not u , 401 未注册")
                return jsonify({
                    'result': {
                        'code': 401,
                        'msg': "未注册"
                    }})
        l.i("200 获取成功")
        return jsonify({
            'result': {
                'code': 200,
                'msg': "获取成功",
                'data': json.dumps(u)
            }})

    def post(self, user_id=None, action=None):
        # form = RegistrationForm(request.form, csrf=False)
        # # 校验
        # if form.validate_on_submit():
        #     user_info = form.form2dict()
        #     u = user_dao.add(**user_info)
        #     return jsonify(u)
        # return jsonify(form.errors)
        with current_app.app_context():
            d = request.get_json()
            openid = self.get_openid(d['code'])
            c = self.get_chat_users()
            u = c.find_one({'openid': openid})
            if u:
                l.i("200 u已存在")
                return jsonify({
                    'result': {
                        'code': 200,
                        'msg': "已存在",
                        'inserted_id': str(u['_id'])
                    }})

            ret = c.insert_one({'openid': openid, 'userInfo': d['userInfo']})
            l.i("200 注册成功")
            return jsonify({
                'result': {
                    'code': 200,
                    'msg': "注册成功",
                    'inserted_id': str(ret.inserted_id)
                }})

    def put(self, user_id, action=None):
        return "post"

    def delete(self, user_id):
        ret = user_dao.remove(id=user_id)
        return "删除成功" if ret == 1 else "删除失败"

    def get_chat_users(self):
        mongodb = get_mongo().cx.chatai
        return mongodb['chat_users']

    def get_openid(self, auth_code):
        url = "https://api.weixin.qq.com/sns/jscode2session"
        url += "?appid=wxf12c64ae66740127"
        url += "&secret=299b42c42daebe0ac0c779e43c74946a"
        url += f"&js_code={auth_code}"
        url += "&grant_type=authorization_code"
        url += "&connect_redirect=1"
        response = requests.get(url)
        d: dict = response.json()
        try:
            return d.get('openid')
        except Exception as e:
            l.i(d, auth_code)
            return None
