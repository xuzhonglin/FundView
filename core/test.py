#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 21:04
@Author   : colinxu
@File     : test.py
@Desc     : 
"""

from core.crawler.fund_ant_fortune import FundAntFortune
from core.crawler.fund_east_money import FundEastMoney

fund_code = '110011'
fund_codes = ["002190",
              "007824",
              "001510",
              "003096",
              "007020",
              "161029",
              "001702",
              "003984",
              "161028",
              "008888",
              "320007",
              "000961",
              "001593",
              "161726",
              "519674",
              "009777",
              "160630",
              "260108",
              "001508",
              "161725",
              "001595",
              "005693",
              "470006",
              "001606",
              "003494"]
# fund = FundAntFortune()
fund = FundEastMoney()
# result = fund.get_networth('110011')
# result = fund.get_networth_batch(fund_codes)
# result = fund.get_growth(fund_code)
# result = fund.get_growth_batch(fund_codes)
result = fund.get_positions(fund_code)
print(result)
