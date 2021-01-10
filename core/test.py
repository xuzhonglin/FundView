#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 21:04
@Author   : colinxu
@File     : test.py
@Desc     : 
"""

from core.crawler.fund_ant_fortune import FundAntFortune

fund_ant = FundAntFortune()
# result = fund_ant.get_networth('110011')
result = fund_ant.get_networth_batch([
    "002190",
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
    "003494"
])
print(result)
