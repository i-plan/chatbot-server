import flask
from flask import request, current_app, jsonify
from flask_login import logout_user, login_user, current_user
from flask_restful import Resource, abort
from werkzeug.security import check_password_hash

from app.form.user import LoginForm, MiniProgramLoginForm
from app.storage import user as user_dao
from app.util import l


class PassportAPI(Resource):
    actions = ['login', 'logout']

    def post(self, action):
        """
        /passport/login
        or
        /passport/logout
        :param action:
        :return:
        """
        if action in self.actions:
            self_action = getattr(self, action.lower())
            return self_action()
        else:
            abort(404)

    def login(self):
        login_type = int(request.form.get('type', -1))
        l.i("login_type: %s", login_type)
        if login_type == 0:  # 账号登录
            return self.email_login(request.form)
        elif login_type == 1:  # 手机号验证码登录
            return self.mobile_login(request.form)
        elif login_type == 2:  # 小程序授权登录
            return self.miniprogram_login(request.form)
        elif login_type == 3:  # sdk授权登录
            return self.sdk_login(request.form)
        else:
            return flask.make_response("不存在该登录方式")

    def sdk_login(self, f):
        # u = user_dao.query(email=email).first()
        return ""

    def miniprogram_login(self, f):
        form = MiniProgramLoginForm(f, csrf=False)
        if not form.validate_on_submit(): return jsonify(form.errors)
        code = form.code.data
        # d = get_session(code)
        d={"openid":"oh1Hz5DfxK54QoSEoPmaCrtA8Ch4"}
        try:
            u = user_dao.query(openid=d['openid']).first()
            if not u: return jsonify({'message': f"登录失败,账号不存在{code}"})
            # if not u:
            #     user_info = form.form2dict()
            #     user_info['openid'] = d['openid']
            #     l.i(f'插入一条:{user_info}')
            #     user_info['password'] = "asdfasdf"
            #     u = user_dao.add(**user_info)
            remember = False
            if current_app.config.get("COOKIE_ENABLE"): remember = True
            login_user(u, remember=remember)
            l.i(f'remember me(记住我)功能是否开启,{remember}')
            return jsonify(current_user.to_json())
        except Exception as e:
            print(e)
            l.e(f'auth_code:{code} {d}')
            return jsonify({"l": "failure"})

    def mobile_login(self, f):
        return ""

    def email_login(self, f):
        form = LoginForm(f, csrf=False)
        if not form.validate_on_submit():  return jsonify(form.errors)
        email = form.email.data
        pwd = form.password.data
        l.i("%s,%s", email, pwd, exc_info=1)
        u = user_dao.query(email=email).first()
        if not u: return jsonify({'message': f"登录失败,账号不存在{email} {pwd}"})
        if not check_password_hash(u.password, pwd): return jsonify({'message': f"登录失败,密码不匹配{email} {pwd}"})
        try:
            remember = False
            if current_app.config.get("COOKIE_ENABLE"): remember = True
            login_user(u, remember=remember)
            l.i(f'remember me(记住我)功能是否开启,{remember}')
            current_app.logger.info(f'remember me(记住我)功能是否开启,{remember}')
            flask.flash('Logged in successfully.')
            return jsonify(current_user.to_json())
            # return flask.redirect(flask.url_for('index'))
        except BaseException as e:
            return jsonify({'message': "登录异常"})

    def logout(self):
        logout_user()
        return "退出成功"
