#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 17:59
@Author   : colinxu
@File     : fund_abstract.py
@Desc     : 基金抽象类
"""
import abc


class Fund(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_info(self, fund_code: str):
        """
        获取基金基础信息：经理，公司等
        :param fund_code: 基金代码
        :return:
        """

    @abc.abstractmethod
    def get_networth(self, fund_code: str):
        """
        获取基金最新净值、估值
        :param fund_code: 基金代码
        :return:
        """

    @abc.abstractmethod
    def get_growth(self, fund_code: str):
        """
        获取基金阶段涨幅：近1月，近3月，近6月，近1年
        :param fund_code: 基金代码
        :return:
        """

    @abc.abstractmethod
    def get_networth_batch(self, fund_codes: list):
        """
        批量获取基金最新净值、估值
        :param fund_codes: 基金代码
        :return:
        """

    @abc.abstractmethod
    def get_growth_batch(self, fund_codes: list):
        """
        批量获取基金阶段涨幅：近1月，近3月，近6月，近1年
        :param fund_codes: 基金代码
        :return:
        """

    @abc.abstractmethod
    def get_history_networth(self, fund_code: str, start_date: str, end_date: str):
        """
        获取基金的历史净值
        :param fund_code: 基金代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return:
        """

    @abc.abstractmethod
    def get_positions(self, fund_code: str):
        """
        获取基金持仓：重仓股票
        :param fund_code: 基金代码
        :return:
        """
