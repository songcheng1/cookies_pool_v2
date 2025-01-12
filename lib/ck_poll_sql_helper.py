# -*- coding: UTF-8 -*-
# @author: ylw
# @file: ck_poll_sql_helper
# @time: 2025/1/10
# @desc:
# import sys
# import os
from typing import Optional, List

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from db_engine.engine import Engine
from utils.wrapper import Wrapper

from settings import TableConfig

from logger import logger


class CookiePollSQLHelper:
    """数据库交互类, 需要自己根据业务自己设计"""

    task_table = TableConfig.tasks.value  # cookie任务表(队列)
    cookie_table = TableConfig.cookies.value  # cookie表

    PLAT_RENAME_MAP = {}

    def __init__(self, engine: Engine):
        self.engine = engine

    def fetch_task(self, platform):
        """获取task任务"""
        print(self.cookie_table)
        return []

    def send_task(self, platform: str, store_code):
        """下发task任务"""
        print(self.task_table)

    def get_task_queue(self, platform: str) -> List[dict]:
        """从队列中获取task"""
        print(self.task_table)
        logger.info("获取到了任务...")
        return []

    def save_cookie(self, platform: str, *args, **kwargs):
        """储存cookie"""
        logger.info("储存cookie成功")
        print(self.cookie_table)

    @Wrapper.retry_until_done(10, 6, desc="获取验证码失败")
    def sms_verify_code(self, phone: int, platform: str, send_time: Optional[str] = None) -> Optional[str]:
        """获取短信验证码"""
        return "123456"


if __name__ == '__main__':
    pass
