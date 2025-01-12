# -*- coding: UTF-8 -*-
# @author: ylw
# @file: logger_func
# @time: 2024/1/15
# @desc:
import os
import sys
from loguru import logger as __logger

__all__ = [
    'logger'
]

logger = __logger
__LOG_DIR_NAME = '_logs'  # 日志输出目录


def __init_logger():
    # 设置保存路径为项目路径下的 _logs 目录
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), __LOG_DIR_NAME)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    program = os.path.basename(sys.argv[0]).split(".")[0]
    log_file = os.path.join(logs_dir, f"{program}.log")

    # 移除默认格式
    logger.remove()

    # 添加输出到文件的处理器，保留最近的 1 个日志文件，每个文件最大 10MB
    logger.add(
        log_file, rotation="10 MB", retention="1 week", level="DEBUG", encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} : {function} : {line} - {message}",
    )

    # 添加输出到控制台的处理器，输出级别设置为 INFO
    logger.level("INFO", color="<red>")
    logger.add(
        sys.stdout, level="INFO",
        format="<level>{level}</level> : <level>{file}</level> : <green>{function}</green> : <blue>{line}</blue> - <level>{message}</level>"
    )


__init_logger()

if __name__ == '__main__':
    logger.info("测试一下")
