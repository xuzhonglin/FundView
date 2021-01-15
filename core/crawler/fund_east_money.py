#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/10 17:40
@Author   : colinxu
@File     : fund_east_money.py
@Desc     : 天天基金网基金
"""
import uuid
from concurrent.futures.thread import ThreadPoolExecutor

from config import FundConfig
from .fund_abstract import Fund

from utils.other import *
from utils.proxy_http import ProxyHttp


class FundEastMoney(Fund):
    def __init__(self):
        super().__init__()

    def get_info(self, fund_code: str):
        super().get_info(fund_code)

    def get_networth(self, fund_code: str):
        return self._get_networth([fund_code])[0]

    def _get_networth(self, fund_codes: list):
        data = []
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': get_fake_ua()
            }
            params = {
                'pageIndex': 1,
                'pageSize': len(fund_codes),
                'plat': 'Android',
                'appType': 'ttjj',
                'product': 'EFund',
                'Version': '1',
                'deviceid': str(uuid.uuid4()),
                'Fcodes': ','.join(fund_codes)
            }
            resp = ProxyHttp.get(url, headers=headers, params=params)
            resp_json = resp.json()
            for item in resp_json['Datas']:
                data.append({
                    "code": item['FCODE'],
                    "name": item['SHORTNAME'],
                    "netWorth": item['NAV'],
                    "netWorthDate": item['PDATE'],
                    "dayGrowth": item['NAVCHGRT'],
                    "expectWorth": item['GSZ'],
                    "expectWorthDate": item['GZTIME'],
                    "expectGrowth": item['GSZZL']
                })
        except Exception as ex:
            print(ex)
        return data

    def get_growth(self, fund_code: str):
        super().get_growth(fund_code)

    def get_networth_batch(self, fund_codes: list):
        # 先每20个分隔
        fund_codes_array = split_array(fund_codes, 20)
        if len(fund_codes_array) > 1:
            startTime = time.time()
            # 获取最小工作线程数
            worker = min(FundConfig.THREAD_WORKERS, len(fund_codes_array))
            threadPool = ThreadPoolExecutor(max_workers=worker)
            results = []
            for result in threadPool.map(lambda fund_codes_item: self._get_networth(fund_codes_item), fund_codes_array):
                results.extend(result)
            endTime = time.time()
            print('执行耗时：{}'.format(endTime - startTime))
            return results
        else:
            return self._get_networth(fund_codes)

    def get_growth_batch(self, fund_codes: list):
        super().get_growth_batch(fund_codes)

    def get_history_networth(self, fund_code: str, start_date: str, end_date: str):
        super().get_history_networth(fund_code, start_date, end_date)

    def get_positions(self, fund_code: str):
        super().get_positions(fund_code)
