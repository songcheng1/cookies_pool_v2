# -*- coding: UTF-8 -*-
# @author: ylw
# @file: feishu_api
# @time: 2025/1/9
# @desc:
# import sys
# import os
import json
import base64
import hashlib
import hmac
import time
import requests
from typing import Type, Optional

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from utils.wrapper import Wrapper

from settings import FeishuKey
from logger import logger


class FeishuApi:
    _feishu_key: Type[FeishuKey] = None

    def __init__(self):
        self._headers = {'Content-Type': 'application/json', 'Authorization': ''}

    @staticmethod
    def api_sign(timestamp, key):
        string_to_sign = '{}\n{}'.format(timestamp, key)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(hmac_code).decode('utf-8')

    def api_app_access_token(self) -> str:
        """
        自建应用获取 tenant_access_token
        tenant_access_token 的最大有效期是 2 小时。如果在有效期小于 30 分钟的情况下，调用本接口，会返回一个新的 tenant_access_token
        这会同时存在两个有效的 tenant_access_token。
        """
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        params = json.dumps({'app_id': self._feishu_key.app_id.value, 'app_secret': self._feishu_key.secret_key.value})
        response = requests.post(url, data=params, headers={'Content-Type': "application/json; charset=utf-8"}).json()

        tenant_access_token = response['tenant_access_token']
        logger.info(f'当前-tenant_access_token:{tenant_access_token}-有效时间为:{response["expire"] / 60}分钟')
        return tenant_access_token

    @Wrapper.retry(retries=3, delay=5)
    def _requests(self, method, url, **kwargs) -> requests.Response:
        headers = kwargs.pop('headers') if kwargs.get('headers') else self._headers

        response: requests.Response = requests.request(method, url, headers=headers, timeout=5, **kwargs)
        response_text = response.text
        if 'Missing access token' in response_text or 'Invalid access token' in response_text or 'access token' in response_text:
            tenant_access_token = self.api_app_access_token()
            headers['Authorization'] = f'Bearer {tenant_access_token}'
            response: requests.Response = requests.request(method, url, headers=headers, timeout=5, **kwargs)

        return response

    @Wrapper.cache_with_expiration(60 * 1)
    def api_user_id(self, mobiles: str) -> Optional[str]:
        if not isinstance(mobiles, str):
            return None

        url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id'
        payload = json.dumps({"mobiles": [mobiles]})
        response = self._requests("POST", url, headers=self._headers, data=payload).json()
        user_list = response['data']['user_list']
        if not user_list:
            return None
        return user_list[0]['user_id']

    @Wrapper.cache_with_expiration(60 * 1)
    def api_user_info(self, mobiles: str) -> dict:
        user_id = self.api_user_id(mobiles)
        print(mobiles)

        url = "https://open.feishu.cn/open-apis/contact/v3/users/batch?department_id_type=open_department_id&user_id_type=open_id&"
        url += f'user_ids={user_id}'
        respons = self._requests("GET", url, headers=self._headers).json()
        user_list = respons['data']['items']
        if not user_list:
            return {}

        item = user_list[0]
        return {
            'mobiles': mobiles,
            'name': item['name'],
            'job_title': item['job_title'],
            'user_id': item['open_id'],
        }

    def api_send_message(self, url, key, content_text):
        timestamp = int(time.time())
        data = {
            "timestamp": timestamp,
            "sign": self.api_sign(timestamp, key),
            "msg_type": "text",
            "content": json.dumps({"text": content_text})
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers={
            "Content-Type": "application/json"
        }, data=data)
        print(response.text)


if __name__ == '__main__':
    pass
