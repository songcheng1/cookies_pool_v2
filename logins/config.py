# -*- coding: UTF-8 -*-
# @author: ylw
# @file: config
# @time: 2025/1/10
# @desc:
# import sys
import os

F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


__all__ = [
    'LOGIN_ARCHIVE_PATH'
]

# 登录缓存文件路径
LOGIN_ARCHIVE_PATH = os.path.join(F_PATH, '.login_archive').replace('\\', '/')

if not os.path.isdir(LOGIN_ARCHIVE_PATH):
    os.makedirs(LOGIN_ARCHIVE_PATH)

if __name__ == '__main__':
    print(LOGIN_ARCHIVE_PATH)
