import requests
import json
import logging

url = "https://api.openai.com/v1/chat/completions"

payload = json.dumps({
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
})
headers = {
    'Accept': 'application/json',
    'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
}
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

logging.captureWarnings(True)
disable_warnings(InsecureRequestWarning)
import requests, warnings
from requests.packages import urllib3

# 关闭警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

proxies = {
    'http': 'http://127.0.0.1:8118', 'https': 'https://127.0.0.1:8118',
    'https_proxy': 'http://127.0.0.1:8118', 'http_proxy': 'http://127.0.0.1:8118'
}
response = requests.request("POST", url, proxies=proxies, verify=False, headers=headers, data=payload)
# response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
