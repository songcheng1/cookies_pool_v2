# -*- coding: UTF-8 -*-
# @author: ylw
# @file: cookie_poll
# @time: 2025/1/8
# @desc:
# import sys
# import os
import traceback
from typing import cast, Dict, Optional
from functools import wraps

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from lib.ck_poll_base import CookiePollBase, LoginBase, NotifyBase, Engine
from lib.ck_poll_sql_helper import CookiePollSQLHelper
from lib.ck_poll_init_config import CookiePollInitConfig
from accounts.account_base_class import AccountBaseClass, AccountConfigTemp

from utils.wrapper import Wrapper

from logger import logger

FUNC_LOCK_MAP = {}


def synchronized_method(func):
    """
    装饰器：加锁限制同步运行
    :param func: 需要加锁的目标函数
    :return: 包装后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_id = id(func)
        if FUNC_LOCK_MAP.get(func_id, True) is False:
            return

        try:
            FUNC_LOCK_MAP[func_id] = False
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(traceback.format_exc())
            raise e
        finally:
            FUNC_LOCK_MAP[func_id] = True

    return cast(Wrapper.F, wrapper)


class CookiePoll(CookiePollBase):

    def __init__(self, engine: Engine, config: CookiePollInitConfig, debugger: bool = False):
        if not isinstance(config, CookiePollInitConfig):
            return
        # 工具
        self.engine: Engine = engine
        self.ck_poll_sql_helper = CookiePollSQLHelper(self.engine)

        # 任务配置相关
        self.account_config: AccountBaseClass = config.account_config
        self.platform: str = config.platform  # 平台
        self.maintainer: list = config.maintainer  # 通知负责人
        self.timer: tuple = config.timer  # 定时运行时间 tuple：[每天的开始时间(h), 结束时间(h), 检测间隔(单位分钟)]
        self.open_init_task = config.open_init_task  # 主动下发任务
        self.open_check = config.open_check  # 主动检测
        self.debugger = debugger  # debugger模式

        # 类
        self.login_instance: Optional[LoginBase] = None
        self.notify_tools: Optional[NotifyBase] = None

        if config.open_init_task:
            self.initiative_push_task()

    def initiative_push_task(self):
        """主动推送任务"""
        account_config: Dict[str, AccountConfigTemp] = self.account_config.account_config()
        for store_code in account_config.keys():
            self.ck_poll_sql_helper.send_task(self.platform, store_code)

    def logout_push_task(self):
        """登录失效,推送任务(需要进行检测)"""
        cookie_data_s = self.ck_poll_sql_helper.fetch_task(self.platform)
        if not cookie_data_s:
            logger.info("暂时无账号需要检测")
            return
        for cookie_data in cookie_data_s:
            account = cookie_data['account']
            store_code = cookie_data['store_code']
            sub_shop = cookie_data['sub_shop']
            cookie = cookie_data['cookie']
            notify_shop = sub_shop or account  # 根据不同的平台, 选择 店铺或者子店铺 进行通知

            status = self.login_instance.login_status(self.platform, account, sub_shop, cookie)
            if status is True:
                logger.info(f"{self.platform} {notify_shop} cookie未过期")
                continue

            logger.info(f"{self.platform} {notify_shop} cookie过期, 下发到任务数据库")
            self.ck_poll_sql_helper.send_task(self.platform, store_code)

    @synchronized_method
    def gen_cookie(self):
        """根据任务队列生成cookie"""

        # 注意, 抽象根据业务自己去实现
        tasks = self.ck_poll_sql_helper.get_task_queue(self.platform)
        for task in tasks:
            cookie = self.login_instance.login(**task)
            self.ck_poll_sql_helper.save_cookie(self.platform, cookie)


if __name__ == '__main__':
    def demo():
        from settings import MysqlConfig
        from accounts.account_base_class import AccountBaseClass
        from account_config import ALL_ACCOUNT_INFO

        from logins.login.demo import DemoLogin
        from notify.notify_feishu import NotifyFeishu, FeishuKey
        from settings import FETSHU_GROUP_CONFIG

        cp = CookiePoll(Engine(MysqlConfig), CookiePollInitConfig(
            account_config=AccountBaseClass('平台', ALL_ACCOUNT_INFO['平台']),
            platform='平台-平台',
            maintainer=[12345678901],  # 消息通知人手机号
            timer=(5, 23, 10),
            open_init_task=False,
            open_check=False
        ))
        cp.register_login_instance(DemoLogin)  # 注册登录类
        cp.register_notify_tools(NotifyFeishu, FeishuKey, FETSHU_GROUP_CONFIG)  # 注册通知类

        cp.start()


    demo()
