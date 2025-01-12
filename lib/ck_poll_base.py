# -*- coding: UTF-8 -*-
# @author: ylw
# @file: cookie_poll_base
# @time: 2025/1/8
# @desc:
import sys
import os
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from accounts.account_base_class import AccountBaseClass
from db_engine.engine import Engine
from logins.login_base import LoginBase
from notify.notify import NotifyBase


# from account_config import AccountConfigTemp


class CookiePollBase(ABC):
    engine: Engine
    account_config: AccountBaseClass
    platform: str  # 平台
    maintainer: list  # 通知负责人
    timer: tuple  # 定时运行时间 tuple：[每天的开始时间(h), 结束时间(h), 检测间隔(单位分钟)]
    open_init_task: bool  # 主动下发任务
    open_check: bool  # 主动检测
    debugger: bool  # debugger模式

    login_instance: Optional[LoginBase] = None
    notify_tools: Optional[NotifyBase] = None

    # def __init__(self, config: CookiePollInitConfig, debugger: bool = False):
    #     if not isinstance(config, CookiePollInitConfig):
    #         return
    #
    #     self.account_config: Dict[str, Dict[str, AccountConfigTemp]] = config.account_config
    #     self.platform: str = config.platform  # 平台
    #     self.maintainer: list = config.maintainer  # 通知负责人
    #     self.timer: tuple = config.timer  # 定时运行时间 tuple：[每天的开始时间(h), 结束时间(h), 检测间隔(单位分钟)]
    #     self.open_init_task = config.open_init_task  # 主动下发任务
    #     self.open_check = config.open_check  # 主动检测
    #     self.debugger = debugger  # debugger模式
    #
    #     self.login_instance: Optional[LoginBase] = None
    #     self.notify_tools: Optional[NotifyBase] = None

    @abstractmethod
    def initiative_push_task(self):
        """主动推送任务"""

    @abstractmethod
    def logout_push_task(self):
        """登录失效,推送任务"""

    @abstractmethod
    def gen_cookie(self):
        """根据任务队列生成cookie"""

    def register_login_instance(self, login_class: Type[LoginBase], *args, **kwargs):
        """注册登录类实例"""
        if not issubclass(login_class, LoginBase):
            raise TypeError('注册类型错误, 必须是 `LoginBase` 类的继承')

        self.login_instance = login_class(*args, **kwargs)
        self.login_instance.set_engine(self.engine)
        return self

    def register_notify_tools(self, notify_class: Type[NotifyBase], *args, **kwargs):
        """注册消息通知工具"""
        if not issubclass(notify_class, NotifyBase):
            raise TypeError('注册类型错误, 必须是 `NotifyBase` 类的继承')

        self.notify_tools = notify_class(*args, **kwargs)
        return self

    def start(self):
        scheduler = BlockingScheduler(timezone='Asia/Shanghai')

        # 每天定时下发任务
        trigger = CronTrigger.from_crontab(f'0 {self.timer[0]} * * *')
        scheduler.add_job(self.initiative_push_task, trigger)

        if self.open_check:  # 主动检测cookie是否过期， 并下发到任务队列
            trigger = CronTrigger(hour=f'{self.timer[0]}-{self.timer[1]}', minute=f'*/{self.timer[2]}')
            scheduler.add_job(self.logout_push_task, trigger=trigger, max_instances=1)

        # 主动检测cookie任务队列， 并生成cookie
        trigger = CronTrigger(hour=f'{self.timer[0]}-{self.timer[1]}', minute='*', second='*/5')  # 5秒钟运行一次
        scheduler.add_job(self.gen_cookie, trigger=trigger, max_instances=2)

        scheduler.start()


if __name__ == '__main__':
    def demo():
        ...


    demo()
