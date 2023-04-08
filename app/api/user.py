import json

import requests
from flask import jsonify, request, current_app
from flask_restful import Resource

from app.api.wx_auth import get_openid
from app.storage import get_mongo
from app.form.user import RegistrationForm
from app.storage import user as user_dao

from sqlalchemy.ext.declarative import DeclarativeMeta

from app.storage.user import get_chat_users
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
    # @auth
    def get(self, *args, **kw):
        # print(json.dumps(User.query.all(),cls= AlchemyEncoder))
        # return jsonify({
        #     'code': 1,
        #     'data': user_dao.get(id=user_id) if user_id else user_dao.get()
        # })
        with current_app.app_context():
            c = get_chat_users()
            openid = request.headers.get('X-WX-OPENID')
            # openid = kw.get('openid')
            u = c.find_one({'openid': openid}, {'_id': False})
            if not u:
                l.i("用户不存在")
                return jsonify({
                    'result': {
                        'code': 401,
                        'msg': "用户不存在"
                    }})
            l.i("200 获取成功")
            return jsonify({
                'result': {
                    'code': 200,
                    'msg': "获取成功",
                    'data': json.dumps(u)
                }})

    # @auth
    def post(self, user_id=None, action=None,*args, **kw):
        # form = RegistrationForm(request.form, csrf=False)
        # # 校验
        # if form.validate_on_submit():
        #     user_info = form.form2dict()
        #     u = user_dao.add(**user_info)
        #     return jsonify(u)
        # return jsonify(form.errors)
        with current_app.app_context():
            # openid = kw.get('openid')
            openid = request.headers.get('X-WX-OPENID')
            c = get_chat_users()
            u = c.find_one({'openid': openid})
            if u:
                l.i("200 u已存在")
                return jsonify({
                    'result': {
                        'code': 200,
                        'msg': "已存在",
                        'inserted_id': str(u['_id'])
                    }})
            ret = c.insert_one({'openid': openid, 'usage': 1, 'userInfo': request.get_json()})
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
