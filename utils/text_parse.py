# -*- coding: UTF-8 -*-
# @author: ylw
# @file: text_parse
# @time: 2023/11/14
# @desc:
# import sys
# import os
import hashlib
from pypinyin import pinyin, Style


def chinese_to_pinyin(chinese: str, join=False):
    result = pinyin(chinese, style=Style.NORMAL)
    if join:
        return ''.join([i[0] for i in result])
    return result


def calculate_number(text):
    """
    根据文本计算出在 9600, 19800 之间的数字
    :param text:
    :return:
    """
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    decimal_hash = int(sha256_hash, 16)  # 将16进制的hash转换为10进制
    number = 9600 + (decimal_hash % 10201)
    return number


if __name__ == '__main__':
    print(calculate_number(
        'isg=BImJ6d'))
