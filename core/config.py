#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 20:55
@Author   : colinxu
@File     : config.py
@Desc     : 
"""


class FundConfig:
    ANT_URL = 'http://www.fund123.cn/api/fund'

    # 代理地址
    PROXY_POOL = 'http://proxy-pool.colinxu.cn'

    # 是否开启代理
    ENABLE_PROXY = False

    # 线程数
    THREAD_WORKERS = 10
