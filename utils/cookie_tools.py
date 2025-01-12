# -*- coding: UTF-8 -*-
# @author: ylw
# @file: cookie_tools
# @time: 2025/1/9
# @desc:
# import sys
# import os
from http.cookiejar import Cookie


def cookie_dict2str(dict_cookie: dict) -> str:
    return ';'.join([f'{k}={v}' for k, v in dict_cookie.items()])


def cookie_str2dict(str_cookie: str) -> dict:
    ck_dict = {}
    str_cookie_split = []
    for i in str_cookie.split('; '):
        for j in i.split(', '):
            str_cookie_split.append(j)
    for ck in str_cookie_split:
        if 'Max-Age=' in ck or 'Path=/' in ck or 'HttpOnly' in ck:
            continue

        resulut = ck.split('=', 1)
        if len(resulut) != 2:
            continue
        key, value = resulut
        ck_dict[key] = value
    return ck_dict


def cookie_to_dict(cookie):
    """把Cookie对象转为dict格式
    :param cookie: Cookie对象、字符串或字典
    :return: cookie字典
    """
    if isinstance(cookie, Cookie):
        cookie_dict = cookie.__dict__.copy()
        cookie_dict.pop('rfc2109', None)
        cookie_dict.pop('_rest', None)
        return cookie_dict

    elif isinstance(cookie, dict):
        cookie_dict = cookie

    elif isinstance(cookie, str):
        cookie = cookie.rstrip(';,').split(',' if ',' in cookie else ';')
        cookie_dict = {}

        for key, attr in enumerate(cookie):
            attr_val = attr.lstrip().split('=', 1)

            if key == 0:
                cookie_dict['name'] = attr_val[0]
                cookie_dict['value'] = attr_val[1] if len(attr_val) == 2 else ''
            else:
                cookie_dict[attr_val[0]] = attr_val[1] if len(attr_val) == 2 else ''

        return cookie_dict

    else:
        raise TypeError('cookie参数必须为Cookie、str或dict类型。')

    return cookie_dict


if __name__ == '__main__':
    pass
