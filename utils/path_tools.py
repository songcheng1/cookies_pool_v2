# -*- coding: UTF-8 -*-
# @author: ylw
# @file: path
# @time: 2023/11/30
# @desc:

import os


def get_file_name(file):
    """
    获得文件名
    :param file: __file__
    :return:
    """
    return os.path.dirname(file).replace('\\', '/').rsplit('/', 1)[-1]


def path_join(l, r, create_path=False):
    """
    路径合并
    :param l:
    :param r:
    :param create_path: 是否创建新的路径
    :return:
    """
    p = os.path.join(l, r).replace('\\', '/')
    if create_path:
        if not os.path.isdir(p):
            os.makedirs(p)

    return p


if __name__ == '__main__':
    pass
