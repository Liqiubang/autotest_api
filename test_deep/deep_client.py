"""深度接口请求客户端 - 发送 x-www-form-urlencoded 格式请求"""

import hashlib
import random
import string
import time

import requests

from test_v2_new.config import APP_ID, APP_SECRET, BASE_URL


class DeepClient:
    """深度接口客户端，封装签名生成和 form-urlencoded 请求发送"""

    def __init__(self, app_id=None, app_secret=None, base_url=None):
        self.app_id = app_id or APP_ID
        self.app_secret = app_secret or APP_SECRET
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    def generate_headers(self):
        """生成认证 Headers（与 SmsClient 相同的前置脚本逻辑）"""
        cur_time = str(int(time.time()))
        nonce = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        raw = self.app_secret + nonce + cur_time
        check_sum = hashlib.sha1(raw.encode('utf-8')).hexdigest()

        return {
            "appID": self.app_id,
            "nonce": nonce,
            "curTime": cur_time,
            "checkSum": check_sum,
        }

    def post(self, url, form_data):
        """发送 POST 请求（form-urlencoded），返回 (响应JSON, URL, 请求Headers, 请求Body)"""
        headers = self.generate_headers()
        response = self.session.post(
            url, data=form_data, headers=headers, timeout=120,
        )
        return response.json(), url, headers, form_data
