#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 17:40
@Author   : colinxu
@File     : fund_east_money.py
@Desc     : 天天基金网基金
"""

from .fund_abstract import Fund


class FundEastMoney(Fund):
    def __init__(self):
        super().__init__()

    def get_info(self, fund_code: str):
        super().get_info(fund_code)

    def get_networth(self, fund_code: str):
        super().get_networth(fund_code)

    def get_growth(self, fund_code: str):
        super().get_growth(fund_code)

    def get_networth_batch(self, fund_codes: list):
        super().get_networth_batch(fund_codes)

    def get_growth_batch(self, fund_codes: list):
        super().get_growth_batch(fund_codes)

    def get_history_networth(self, fund_code: str, start_date: str, end_date: str):
        super().get_history_networth(fund_code, start_date, end_date)

    def get_positions(self, fund_code: str):
        super().get_positions(fund_code)


