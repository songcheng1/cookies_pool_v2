# -*- coding: UTF-8 -*-
# @author: ylw
# @file: exception
# @time: 2025/1/9
# @desc:
# import sys
# import os

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class SlideBlockError(Exception):
    def __init__(self, message=''):
        self.message = f"{message} 滑块滑动失败"

    def __str__(self):
        return self.message


if __name__ == '__main__':
    pass
