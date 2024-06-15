# import functools
#
# from flask import request, jsonify, session
#
# from app.api.wx_auth import get_openid
# from app.lrucache import LRUCache
# from app.util import l
#
#
# class UserId:
#     wx_auth_code: str
#     openid: str
#
#
# lrucache = LRUCache(4000)
#
#
# def auth(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kw):
#         wx_auth_code = request.headers.get('wx-auth-code').strip()
#         openid = lrucache.get(wx_auth_code)
#         print('1', wx_auth_code, openid)
#         if not openid:
#             openid = get_openid(wx_auth_code)
#             lrucache.put(wx_auth_code, openid)
#             print('2', wx_auth_code, openid)
#
#         kw.setdefault('openid', openid)
#         if not openid:
#             l.i("not openid,400 openid 为空，需要重新授权登录")
#             return jsonify({
#                 'result': {
#                     'code': 402,
#                     'msg': "openid 为空，需要重新授权登录"
#                 }})
#         else:
#             return func(*args, **kw)
#
#     return wrapper
