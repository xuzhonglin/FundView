#!/usr/bin/env python
# _*_coding:utf-8_*_
from .client import Client
from .consts import *

"""
@Time     : 2021/5/22 18:08
@Author   : colinxu
@File     : common_api.py
@Desc     : okex v5 公共api
"""


class CommonApi(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, flag='1'):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, flag)

    # 获取搜索的币
    def get_all_coin(self):
        return self._request_without_params(GET, ALL_COIN)

    # 获取汇率
    def get_rate(self, currency: str):
        params = {}
        if currency:
            params['rateName'] = 'usd_' + currency
        return self._request_with_params(GET, CURRENCY_RATE, params)
