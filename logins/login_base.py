# -*- coding: UTF-8 -*-
# @author: ylw
# @file: login_base
# @time: 2025/1/8
# @desc:
# import sys
# import os
from typing import Any
from abc import ABC, abstractmethod
from db_engine.engine import Engine


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class LoginBase(ABC):
    engine: Engine = None

    def __init__(self, *args, **kwargs):
        ...

    def set_engine(self, engine: Engine):
        self.engine = engine

    @abstractmethod
    def login_status(self, platform, account, sub_shop, cookie: str, *args, **kwargs) -> (bool, Any):
        """
        登录未过期
        :return: 有效 True, 无效 False
        """

    @abstractmethod
    def login(self, platform, account, pwd, phone=None, store_code=None, *args, **kwargs) -> dict:
        """
        登录入口
        :return:
        """


if __name__ == '__main__':
    pass
