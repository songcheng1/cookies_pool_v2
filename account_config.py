# -*- coding: UTF-8 -*-
# @author: ylw
# @file: account_config
# @time: 2025/1/9
# @desc:
# import sys
# import os
from typing import Dict

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


ALL_ACCOUNT_INFO: Dict[str, Dict[str, dict]] = {
    '平台': {
        '账号唯一编码': {'account': '账号', 'password': '密码', 'phone': '手机号[int类型]'},
    },
}

if __name__ == '__main__':
    print(ALL_ACCOUNT_INFO)
