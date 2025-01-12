# -*- coding: UTF-8 -*-
# @author: ylw
# @file: g_tools
# @time: 2025/1/8
# @desc:
# import sys
import os


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from logins.config import LOGIN_ARCHIVE_PATH


def path_parent_name(file_name: str) -> str:
    """父路径文件名"""
    return os.path.dirname(file_name).replace('\\', '/').rsplit('/', 1)[-1]


def archive_data_path(file_name: str):
    parent_name = path_parent_name(file_name)
    return os.path.join(LOGIN_ARCHIVE_PATH, parent_name).replace('\\', '/')


if __name__ == '__main__':
    print(archive_data_path(r'D:\cookies_pool_v2\logins\tb\almm\login_tb_base.py'))
