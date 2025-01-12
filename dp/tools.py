# -*- coding: UTF-8 -*-
# @author: ylw
# @file: tools
# @time: 2025/1/10
# @desc:
# import sys
import os
import hashlib


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

def path_join(l, r, create_path=False) -> str:
    """路径合并"""
    p = os.path.join(l, r).replace('\\', '/')
    if create_path:
        if not os.path.isdir(p):
            os.makedirs(p)

    return p


def calculate_number(text) -> int:
    """根据文本计算出在 9600, 19800 之间的数字"""
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    decimal_hash = int(sha256_hash, 16)  # 将16进制的hash转换为10进制
    number = 9600 + (decimal_hash % 10201)
    return number


if __name__ == '__main__':
    pass
