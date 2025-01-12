# -*- coding: UTF-8 -*-
# @author: ylw
# @file: demo
# @time: 2025-01-12
# @desc:
# import sys
# import os

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from engine import engine
from lib.ck_poll import CookiePoll
from lib.ck_poll_init_config import CookiePollInitConfig

from accounts.account_base_class import AccountBaseClass
from account_config import ALL_ACCOUNT_INFO

from logins.login.demo import DemoLogin
from notify.notify_feishu import NotifyFeishu, FeishuKey
from settings import FETSHU_GROUP_CONFIG


def demo():
    cp = CookiePoll(engine, CookiePollInitConfig(
        account_config=AccountBaseClass('平台', ALL_ACCOUNT_INFO['平台']),
        platform='平台-平台',
        maintainer=[12345678901],  # 消息通知人手机号
        timer=(5, 23, 10),  # 每天 5点 到 23点, 每十分钟主动检测一次cookie任务是否过期
        open_init_task=False,  # 初始化下发任务
        open_check=False  # 主动检测cookie是否过期
    ))
    cp.register_login_instance(DemoLogin)  # 注册登录类
    cp.register_notify_tools(NotifyFeishu, FeishuKey, FETSHU_GROUP_CONFIG)  # 注册通知类

    cp.start()


demo()

if __name__ == '__main__':
    pass
