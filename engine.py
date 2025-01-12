# -*- coding: UTF-8 -*-
# @author: ylw
# @file: engine
# @time: 2025/1/8
# @desc:
# import sys
# import os

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from db_engine.engine import Engine
from settings import MysqlConfig

__all__ = [
    'engine'
]

engine = Engine(MysqlConfig)

if __name__ == '__main__':
    pass
