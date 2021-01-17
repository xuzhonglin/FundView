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
        growth = {
            "lastWeekGrowth": "--",
            "lastMonthGrowth": "--",
            "lastThreeMonthsGrowth": "--",
            "lastSixMonthsGrowth": "--",
            "lastYearGrowth": "--"
        }
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNPeriodIncrease'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': get_fake_ua()
            }
            params = {
                'deviceid': str(uuid.uuid4()),
                'version': '6.3.5',
                'appVersion': '6.0.0',
                'product': 'EFund',
                'plat': 'Iphone',
                'FCODE': fund_code,
            }
            resp = ProxyHttp.get(url, headers=headers, params=params)
            resp_json = resp.json()
            for item in resp_json['Datas']:
                key_name = item['title']
                if key_name == 'Z':
                    growth['lastWeekGrowth'] = item['syl'] if item['syl'] != '' else '--'
                elif key_name == 'Y':
                    growth['lastMonthGrowth'] = item['syl'] if item['syl'] != '' else '--'
                elif key_name == '3Y':
                    growth['lastThreeMonthsGrowth'] = item['syl'] if item['syl'] != '' else '--'
                elif key_name == '6Y':
                    growth['lastSixMonthsGrowth'] = item['syl'] if item['syl'] != '' else '--'
                elif key_name == '1N':
                    growth['lastYearGrowth'] = item['syl'] if item['syl'] != '' else '--'
        except:
            pass
        return growth

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
        startTime = time.time()
        threadPool = ThreadPoolExecutor(max_workers=FundConfig.THREAD_WORKERS)
        results = []
        for result in threadPool.map(lambda fund_code: self.get_growth(fund_code), fund_codes):
            results.append(result)
        endTime = time.time()
        print('执行耗时：{}'.format(endTime - startTime))
        return results

    def get_history_networth(self, fund_code: str, start_date: str, end_date: str):
        super().get_history_networth(fund_code, start_date, end_date)

    def get_positions(self, fund_code: str):
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': get_fake_ua()
            }
            params = {
                'plat': 'Android',
                'appType': 'ttjj',
                'product': 'EFund',
                'Version': '2.0.0',
                'deviceid': 'Wap',
                'FCODE': fund_code,
                '_': get_now_timestamp()
            }
            resp = ProxyHttp.get(url, params=params, headers=headers)
            if resp.status_code == 200:
                resp_json = resp.json()
                data = resp_json['Datas']['fundStocks']
                ret = []
                stock_codes = []
                for item in data:
                    stock_codes.append(item['NEWTEXCH'] + '.' + item['GPDM'])
                    ret.append({
                        'code': item['GPDM'],
                        'name': item['GPJC'],
                        'proportion': item['JZBL'],
                        'holdUnits': 0,
                        'holdAmount': 0,
                        'changePercent': item['PCTNVCHG']
                    })
                stock_codes = ','.join(stock_codes)
                stock_info = self._get_stocks_info(stock_codes)
                for index, item in enumerate(ret):
                    item['changePercent'] = stock_info[index]['f3']
                return ret
        except Exception as e:
            print(e)
        return []

    def _get_stocks_info(self, stock_codes: str):
        try:
            url = 'https://push2.eastmoney.com/api/qt/ulist.np/get'
            headers = {
                'Host': 'push2.eastmoney.com',
                'User-Agent': get_fake_ua()
            }
            params = {
                'fields': 'f1,f2,f3,f4,f12,f13,f14,f292',
                'fltt': '2',
                'secids': stock_codes,
                'deviceid': 'Wap',
                'plat': 'Wap',
                'product': 'EFund',
                'version': '2.0.0',
                'Uid': ''
            }
            resp = ProxyHttp.get(url, headers=headers, params=params)
            resp_json = resp.json()
            return resp_json['data']['diff']
        except:
            pass
            return []
