import hashlib
import json
import random
import string
import time

import requests

from config import APP_ID, APP_SECRET, BASE_URL


class SmsClient:
    """SMS V2 接口客户端，封装签名生成和请求发送"""

    def __init__(self, app_id=None, app_secret=None, base_url=None):
        self.app_id = app_id or APP_ID
        self.app_secret = app_secret or APP_SECRET
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    def generate_headers(self):
        """
        前置脚本逻辑：
        CheckSum = SHA1(AppSecret + Nonce + CurTime) 小写 hex
        """
        cur_time = str(int(time.time()))
        nonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        raw = self.app_secret + nonce + cur_time
        check_sum = hashlib.sha1(raw.encode('utf-8')).hexdigest()

        return {
            "appID": self.app_id,
            "nonce": nonce,
            "curTime": cur_time,
            "checkSum": check_sum,
            "Content-Type": "application/json"
        }

    def post(self, path, json_body):
        """发送 POST 请求，返回 (响应JSON, URL, 请求Headers, 请求Body)"""
        url = f"{self.base_url}{path}"
        headers = self.generate_headers()
        response = self.session.post(url, json=json_body, headers=headers, timeout=120)
        return response.json(), url, headers, json_body
