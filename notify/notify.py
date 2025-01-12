# -*- coding: UTF-8 -*-
# @author: ylw
# @file: notify_base
# @time: 2025/1/9
# @desc:
# import sys
# import os
from abc import ABC, abstractmethod
from typing import Union


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class NotifyBase(ABC):
    def __init__(self, *args, **kwargs):
        ...

    @abstractmethod
    def send_message(self, group_name: str, maintainer: Union[str, list], content: str):
        ...


if __name__ == '__main__':
    pass
