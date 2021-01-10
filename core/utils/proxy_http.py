#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 17:45
@Author   : colinxu
@File     : proxy_http.py
@Desc     :
"""
import requests

from config import FundConfig


class ProxyHttp:

    @classmethod
    def get(cls, url: str, headers: dict = None, params: dict = None, enable_proxy: bool = False):
        """
        使用代理调用get
        :param enable_proxy: 是否启用代理
        :param url: 地址
        :param params: 参数
        :param headers: 请求头
        :return:
        """
        session = requests.Session()
        session.trust_env = False
        if enable_proxy:
            retry_count = 5
            proxy = cls._get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    return session.get(url, timeout=5, headers=headers, params=params,
                                       proxies={"http": "http://{}".format(proxy)})
                except Exception as e:
                    print(e)
                    retry_count -= 1
            # 删除代理池中代理
            cls._delete_proxy(proxy)
            return None
        else:
            return session.get(url, timeout=5, headers=headers, params=params)

    @classmethod
    def post(cls, url: str, data: dict = None, headers: dict = None, enable_proxy: bool = False):
        """
        使用代理调用get
        :param enable_proxy: 是否启用代理
        :param url: 地址
        :param data: 数据
        :param headers: 请求头
        :return:
        """
        session = requests.Session()
        session.trust_env = False
        if enable_proxy:
            retry_count = 5
            proxy = cls._get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    resp = session.post(url, data, headers=headers, timeout=5,
                                        proxies={"http": "http://{}".format(proxy)})
                    return resp
                except Exception as e:
                    print(e)
                    retry_count -= 1
            # 删除代理池中代理
            cls._delete_proxy(proxy)
            return None
        else:
            return session.post(url, data, headers=headers, timeout=5)

    @classmethod
    def _get_proxy(cls):
        """
        获取代理地址
        :return:
        """
        return requests.get(FundConfig.PROXY_POOL + "/get/").json()

    @classmethod
    def _delete_proxy(cls, proxy):
        """
        删除代理
        :param proxy: 代理地址
        :return:
        """
        requests.get(FundConfig.PROXY_POOL + "/delete/?proxy={}".format(proxy))
