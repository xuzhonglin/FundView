#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 17:39
@Author   : colinxu
@File     : fund_ant_fortune.py
@Desc     : 蚂蚁财富基金
"""

import json
import re
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from config import FundConfig
from utils.proxy_http import ProxyHttp
from utils.other import *
from crawler.fund_abstract import Fund


class FundAntFortune(Fund):
    def __init__(self):
        super().__init__()

    def get_info(self, fund_code: str):
        super().get_info(fund_code)

    def get_networth(self, fund_code: str):
        ant = AntCrawler()
        return ant.get_fund_data(fund_code)

    def get_growth(self, fund_code: str):
        super().get_growth(fund_code)

    def get_networth_batch(self, fund_codes: list):
        startTime = time.time()
        threadPool = ThreadPoolExecutor(max_workers=FundConfig.THREAD_WORKERS)
        results = []
        for result in threadPool.map(lambda fund_code: self.get_networth(fund_code), fund_codes):
            results.append(result)
        endTime = time.time()
        print('执行耗时：{}'.format(endTime - startTime))
        return results

    def get_growth_batch(self, fund_codes: list):
        super().get_growth_batch(fund_codes)

    def get_history_networth(self, fund_code: str, start_date: str, end_date: str):
        super().get_history_networth(fund_code, start_date, end_date)

    def get_positions(self, fund_code: str):
        super().get_positions(fund_code)


class AntCrawler:

    def get_fund_data(self, fundCode: str, isOptional: bool = False):
        try:
            url = 'http://www.fund123.cn/matiaria?fundCode={}'.format(fundCode)
            html = ProxyHttp.get(url)
            cookies = html.headers['set-cookie']
            for i in cookies.split(','):
                sub = i.split(';')
                cookies = cookies + sub[0] + ';'
            # 查找结果
            result = re.findall(r'window.context = (.*);', html.text)
            result = result[0]
            ret_json = json.loads(result)
            csrf = ret_json['csrf']
            fundName = ret_json['materialInfo']['fundBrief']['fundNameAbbr']
            productId = ret_json['materialInfo']['productId']
            netWorth = ret_json['materialInfo']['titleInfo']['netValue']
            netWorthDate = str(time.localtime(time.time()).tm_year) + '-' + ret_json['materialInfo']['titleInfo'][
                'netValueDate']
            netGrowth = ret_json['materialInfo']['titleInfo']['dayOfGrowth']

            url = FundConfig.ANT_URL + '/queryFundEstimateIntraday?_csrf={}'.format(csrf)
            headers = {
                'Cookie': cookies,
                "Origin": "http://www.fund123.cn",
                "Referer": "http://www.fund123.cn/matiaria?fundCode={}".format(fundCode),
                "User-Agent": get_fake_ua()
            }
            data = {
                "startTime": "2020-12-03",
                "endTime": "2020-12-04",
                "limit": 20,
                "productId": productId,
                "format": True,
                "source": "WEALTHBFFWEB"
            }
            resp = ProxyHttp.post(url, data=data, headers=headers).json()
            resp = resp['list'][-1]
            timeStamp = int(resp['time'] / 1000)
            dateArray = datetime.fromtimestamp(timeStamp)
            expectWorthDate = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "code": fundCode,
                "name": fundName,
                "netWorth": netWorth,
                "netWorthDate": netWorthDate,
                "dayGrowth": netGrowth,
                "expectWorth": resp['forecastNetValue'],
                "expectWorthDate": expectWorthDate,
                "expectGrowth": float(resp['forecastGrowth']) * 100
            }
        except:
            data = {
                "code": fundCode,
                "name": '',
                "netWorth": '',
                "netWorthDate": '',
                "dayGrowth": '',
                "expectWorth": '',
                "expectWorthDate": '',
                "expectGrowth": ''
            }
        if isOptional:
            data.update({
                "lastWeekGrowth": '--',
                "lastMonthGrowth": '--',
                "lastThreeMonthsGrowth": '--',
                "lastSixMonthsGrowth": '--',
                "lastYearGrowth": '--'
            })
        return data
