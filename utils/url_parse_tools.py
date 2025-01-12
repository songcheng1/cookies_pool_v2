# -*- coding: UTF-8 -*-
# @author: ylw
# @file: url_parse
# @time: 2023/11/3
# @desc:
# import sys
# import os
from urllib.parse import urlparse


def extract_http_host(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    host = parsed_url.netloc
    return f"{scheme}://{host}/"


if __name__ == '__main__':
    print(extract_http_host(
        'http'
    ))
