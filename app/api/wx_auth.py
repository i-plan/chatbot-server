import requests

from app.util import l


def get_openid(auth_code):
    url = "https://api.weixin.qq.com/sns/jscode2session"
    url += "?appid=wxf12c64ae66740127"
    url += "&secret=299b42c42daebe0ac0c779e43c74946a"
    url += f"&js_code={auth_code}"
    url += "&grant_type=authorization_code"
    url += "&connect_redirect=1"
    response = requests.get(url,verify=False)
    d: dict = response.json()
    try:
        return d['openid']
    except Exception as e:
        l.e(f'auth_code:{auth_code} {d}')
        return None

def get_session(auth_code):
    url = "https://api.weixin.qq.com/sns/jscode2session"
    url += "?appid=wxf12c64ae66740127"
    url += "&secret=299b42c42daebe0ac0c779e43c74946a"
    url += f"&js_code={auth_code}"
    url += "&grant_type=authorization_code"
    url += "&connect_redirect=1"
    response = requests.get(url,verify=False)
    d: dict = response.json()
    return d