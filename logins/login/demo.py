# -*- coding: UTF-8 -*-
# @author: ylw
# @file: demo
# @time: 2025-01-12
# @desc:
# import sys
# import os
from typing import Any

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

from logins.login_base import LoginBase


class DemoLogin(LoginBase):
    def login_status(self, platform, account, sub_shop, cookie: str, *args, **kwargs) -> (bool, Any):
        print('登录未失效')
        return True

    def login(self, platform, account, pwd, phone=None, store_code=None, *args, **kwargs) -> dict:
        print('登录成功')
        return {}


if __name__ == '__main__':
    pass
