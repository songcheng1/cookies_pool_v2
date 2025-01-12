# -*- coding: UTF-8 -*-
# @author: ylw
# @file: handling_tools
# @time: 2023/11/21
# @desc:
import traceback

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from notify.notify import NotifyBase

from logger import logger

__all__ = [
    'NotifyTools',
]

# 失败或者提示等信息字符串模板
ERROR_NOTIFY_STR_MAP = {
    "登录": "登录失败，检查具体原因并修复\n平台：{platform}\n账号：{account}",  # 登陆失败邮件通知模板
    "检查cookie": "检测是否登录失败，检查具体原因并修复\n平台：{platform}\n账号：{account}",  # 检查cookie是否过期模块报错 通知模板
    "密码错误": "登录失败\n平台：{platform}\n账号：{account}\n提示：{help}",  # 密码错误别的导致的登录失败的字符(有提示)
    "店铺未找到": "店铺未找到\n平台：{platform}\n账号：{account}\n店铺：{shop}\n提示：请检测该店铺是否下架或者更改名称",  # 针对抖店这种子店铺未找到的情况
}





class NotifyTools:
    def __init__(self, config: NotifyToolsInitConfig, debugger: bool = False):
        self.platform = config.platform
        self.group_name = config.group_name
        self.maintainer = config.maintainer
        self.debugger = debugger
        self.feishu_notify = FeishuNotify(config.feishu_key, config.feishu_group_info)

    def _send_message(self, notify_str):
        if self.debugger is False:
            self.feishu_notify.send_message(self.group_name, self.maintainer, notify_str)

    def error_notify(self, error_type: str, account: str):
        """捕获错误， 并作相应的处理"""
        if error_type == '登录':
            notify_str = ERROR_NOTIFY_STR_MAP['登录'].format(platform=self.platform, account=account)
        elif error_type == '登录':
            notify_str = ERROR_NOTIFY_STR_MAP['检查cookie'].format(platform=self.platform, account=account)
        else:
            notify_str = ''

        logger.info(f'\n{notify_str}\n{traceback.format_exc()}')
        self._send_message(notify_str)

    def help_notify(self, engin, table, account, sub_shop, help_text: str):
        """
        根据运行提示，做出相应的动作
        :return:
        """
        if '密码错误' in help_text or '密码不正确' in help_text:
            notify_str = ERROR_NOTIFY_STR_MAP['密码错误'].format(platform=self.platform, account=account, help=help_text)
            if self.debugger is False:
                sql = f'update {table} set account_status="0" where account="{account}"'
                engin.commit_task_sql(sql)
        elif "店铺未找到" in help_text:
            notify_str = ERROR_NOTIFY_STR_MAP['店铺未找到'].format(platform=self.platform, account=account, shop=sub_shop)
        else:
            notify_str = ''

        logger.info(notify_str)
        self._send_message(notify_str)


if __name__ == '__main__':
    pass
