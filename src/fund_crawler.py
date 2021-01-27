import json
import os
import random
import re
import time
import uuid
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from chinese_calendar import is_workday

from src.fund_enum import DBSource
from src.fund_config import FundConfig
from src.fund_crawler_ant import FundAnt


class FundCrawler:

    def __init__(self):
        pass

    def get_board_info_ydi(self):
        """
        获取大盘信息
        :return:
        """
        try:
            url = FundConfig.YDI_URL + '/stock/board'
            resp = self.http_get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                temp = []
                for item in resp_json['data']:
                    print(item)
                    temp.append({
                        "priceChange": item['f4'],
                        "date": '',
                        "code": item['f12'],
                        "type": "ZS",
                        "volume": '',
                        "high": '',
                        "low": '',
                        "price": item['f2'],
                        "name": item['f14'],
                        "changePercent": item['f3'],
                        "close": '',
                        "turnover": '',
                        "open": ''
                    })
                return temp
        except Exception as e:
            print(e)
        return []

    def get_board_info_oth(self):
        """
        获取大盘信息
        :return:
        """
        try:
            url = FundConfig.OTHER_URL + '/stock?code=sh000001,sz399001,sz399006,sh000300,sh000016'
            resp = self.http_get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                temp = []
                for item in resp_json['data']:
                    print(item)
                    item['code'] = item['code'][2:]
                    temp.append(item)
                return temp
        except Exception as e:
            print(e)
        return []

    def get_board_info_ttt(self):
        try:
            url = 'http://push2.eastmoney.com/api/qt/clist/get'
            # 参数化访问链接，以dict方式存储
            params = {
                'cb': 'jQuery{}_{}'.format(self.random_str(20), self.get_now_timestamp()),
                'pn': 1,
                'pz': 10,  # 页码
                'fltt': 2,
                'fs': 'i:1.000001,i:0.399001,i:0.399006,i:1.000300,i:1.000016',
                'fields': 'f2,f3,f4,f5,f6,f12,f14,f15,f16,f17,f18',
                '_': self.get_now_timestamp()
            }
            # 装饰头文件
            headers = {
                'Host': '16.push2.eastmoney.com',
                'User-Agent': self.get_fake_ua(),
                'Referer': 'http://quote.eastmoney.com/',
            }
            r = self.http_get(url=url, headers=headers, params=params)  # 发送请求
            result = json.loads(r.text[len(params['cb']) + 1:-2])
            temp = []
            for item in result['data']['diff'].values():
                temp.append({
                    "priceChange": item['f4'],
                    "date": '',
                    "code": item['f12'],
                    "type": "ZS",
                    "volume": item['f5'],
                    "high": item['f15'],
                    "low": item['f16'],
                    "price": item['f2'],
                    "name": item['f14'],
                    "changePercent": item['f3'],
                    "close": item['f18'],
                    "turnover": item['f6'],
                    "open": item['f17']
                })
            return temp

        except Exception as e:
            print(e)
        return []

    def get_board_info(self):
        """
        获取基金的历史净值
        :param fundCode:
        :param startDate:
        :param endDate:
        :return:
        """
        if FundConfig.DB_SWITCH == DBSource.YDI:
            return self.get_board_info_ydi()
        elif FundConfig.DB_SWITCH == DBSource.OTH:
            return self.get_board_info_oth()
        else:
            return self.get_board_info_ttt()

    def get_funds_data_ydi(self, fundCode: [], isOptional: bool = False):
        """
        获取持仓基金信息
        :param isOptional: 是否自选
        :param fundCode: 基金代码列表
        :return:
        """
        try:
            fundCodeArray = self.split_array(fundCode, 20)
            ret = []
            for subArray in fundCodeArray:
                fundCodes = ','.join(subArray)
                url = FundConfig.YDI_URL + '/fund?code=' + fundCodes
                resp = self.http_get(url)
                if resp.status_code == 200:
                    resp_json = resp.json()
                    data = resp_json['data']
                    for item in data:
                        item.update(self.query_update_worth(item))
                        # 是自选基金 这查询近期涨幅
                        if isOptional:
                            item.update(self.get_fund_growth(item['code']))
                    ret.extend(data)
            return ret
        except Exception as e:
            print(e)
        return []

    def get_funds_data_oth(self, fundCode: []):
        """
        获取持仓基金信息
        :param fundCode: 基金代码列表
        :return:
        """
        try:
            fundCodeArray = self.split_array(fundCode, 20)
            ret = []
            for subArray in fundCodeArray:
                fundCodes = ','.join(subArray)
                url = FundConfig.OTHER_URL + '/fund?code=' + fundCodes
                resp = self.http_get(url)
                if resp.status_code == 200:
                    resp_json = resp.json()
                    data = resp_json['data']
                    for item in data:
                        # 查询是否需要更新净值
                        item.update(self.query_update_worth(item))
                    ret.extend(data)
            return ret
        except Exception as e:
            print(e)
        return []

    # def get_funds_data_ttt(self, fundCodes: [], isOptional: bool = False):
    #     data = []
    #     try:
    #         for fundCode in fundCodes:
    #             url = "http://fundgz.1234567.com.cn/js/%s.js" % fundCode
    #             # 浏览器头
    #             headers = {
    #                 'content-type': 'application/json',
    #                 'User-Agent': self.get_fake_ua()
    #             }
    #             r = self.http_get(url, headers=headers)
    #             # 返回信息
    #             content = r.text
    #             # 正则表达式
    #             pattern = r'^jsonpgz\((.*)\)'
    #             # 查找结果
    #             result = re.findall(pattern, content)[0]
    #             result = json.loads(result)
    #             # 遍历结果
    #             temp = {
    #                 "code": result['fundcode'],
    #                 "name": result['name'],
    #                 "netWorth": result['dwjz'],
    #                 "netWorthDate": result['jzrq'],
    #                 "dayGrowth": "0.72",
    #                 "expectWorth": result['gsz'],
    #                 "expectWorthDate": result['gztime'],
    #                 "expectGrowth": result['gszzl']
    #             }
    #
    #             temp.update(self.get_fund_data_ttt_bak(fundCode, isOptional))
    #
    #             # temp.update(self.query_update_worth(temp))
    #
    #             # if isOptional:
    #             #     temp.update(self.get_fund_growth(fundCode))
    #             # temp.
    #             data.append(temp)
    #         return data
    #     except Exception as e:
    #         print(e)
    #         return data

    def get_funds_data_ttt(self, fundCodes: list, isOptional: bool = False):
        """
        获取基金的基础信息[天天基金]
        :param fundCodes: 基金编码
        :param isOptional: 是否自选
        :return: []
        """
        data = []
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': self.get_fake_ua()
            }
            params = {
                'pageIndex': 1,
                'pageSize': len(fundCodes),
                'plat': 'Android',
                'appType': 'ttjj',
                'product': 'EFund',
                'Version': '1',
                'deviceid': str(uuid.uuid4()),
                'Fcodes': ','.join(fundCodes)
            }
            resp = self.http_get(url, headers=headers, params=params)
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
            if isOptional:
                # TODO 移植
                growth = self.get_funds_growth(fundCodes)
                for index, item in enumerate(data):
                    item.update(growth[index])
            print(data)
        except Exception as ex:
            print(ex)
            pass
        return data

    def _get_fund_data_ttt_bak(self, fundCode: str, isOptional: bool = False):
        """
        废弃-获取基金的基础信息[天天基金]
        :param fundCodes: 基金编码
        :param isOptional: 是否自选
        :return: []
        """
        fundData = {}
        try:
            url = 'http://fund.eastmoney.com/{}.html'.format(fundCode)
            headers = {
                'User-Agent': self.get_fake_ua(),
                'Host': 'fund.eastmoney.com',
                'Referer': url
            }
            html = self.http_get(url, headers=headers)
            html = html.content.decode('utf-8')
            soup = BeautifulSoup(html, "lxml")

            # 获取净值
            netWorthHtml = soup.select('div.dataOfFund > dl.dataItem02 > dd.dataNums > span')
            fundData['netWorth'] = netWorthHtml[0].get_text()
            fundData['dayGrowth'] = netWorthHtml[1].get_text().replace('%', '')
            netWorthDate = soup.select('div.dataOfFund > dl.dataItem02 > dt > p')[0].text[-11:-1]
            fundData['netWorthDate'] = netWorthDate

            buyRate = soup.select('span.nowPrice')[0].text
            fundData['buyRate'] = buyRate.replace('%', '')

            # 持仓股票
            # expectWorthHtml = soup.select('#position_shares > div.poptableWrap > table')
            # for i in expectWorthHtml[0].findAll('tr')[1:]:
            #     temp = i.findAll('td')
            #     a = temp[0].find('a').get_text()
            #     b = temp[1].get_text().replace('%', '')
            #     c = temp[2].find('span').get_text().replace('%', '')
            #     print(a, b, c)

            if isOptional:
                # 阶段涨幅
                growthHtml = soup.select('#increaseAmount_stage > table  ')
                growth = growthHtml[0].findAll('tr')[1:2][0].select('.Rdata')
                a = {
                    "lastWeekGrowth": growth[0].text.replace('%', ''),
                    "lastMonthGrowth": growth[1].text.replace('%', ''),
                    "lastThreeMonthsGrowth": growth[2].text.replace('%', ''),
                    "lastSixMonthsGrowth": growth[3].text.replace('%', ''),
                    "lastYearGrowth": growth[5].text.replace('%', '')
                }
                fundData.update(a)
        except Exception as e:
            print(e)
        return fundData

    def get_funds_growth(self, fundCodes: list):
        """
        查询基金的阶段涨幅[天天基金]
        :param fundCodes: 基金编码
        :return:
        """
        from concurrent.futures import ThreadPoolExecutor
        startTime = time.time()
        threadPool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="thread")
        results = []
        for result in threadPool.map(self.get_fund_growth, fundCodes):
            results.append(result)
        endTime = time.time()
        print('执行耗时：{}'.format(endTime - startTime))
        return results

    def get_fund_growth(self, fundCode: str):
        """
        查询单个基金的阶段涨幅[天天基金]
        :param fundCode: 基金代码
        :return:
        """
        growth = {}
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNPeriodIncrease'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': self.get_fake_ua()
            }
            params = {
                'deviceid': str(uuid.uuid4()),
                'version': '6.3.5',
                'appVersion': '6.0.0',
                'product': 'EFund',
                'plat': 'Iphone',
                'FCODE': fundCode,
            }
            resp = requests.get(url, headers=headers, params=params)
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
            growth = {
                "lastWeekGrowth": "--",
                "lastMonthGrowth": "--",
                "lastThreeMonthsGrowth": "--",
                "lastSixMonthsGrowth": "--",
                "lastYearGrowth": "--"
            }
        return growth

    def get_funds_data_ant(self, fundCodes: [], isOptional: bool = False):
        """
        获取基金的基础信息[蚂蚁财富]
        :param fundCodes: 基金编码
        :param isOptional: 是否自选
        :return:
        """
        from concurrent.futures import ThreadPoolExecutor
        startTime = time.time()
        threadPool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="thread")
        results = []
        fundAnt = FundAnt()
        for result in threadPool.map(lambda fundCode: fundAnt.get_fund_data(fundCode, isOptional), fundCodes):
            results.append(result)
            print(result)
        endTime = time.time()
        print('执行耗时：{}'.format(endTime - startTime))
        print(results)
        return results

    def get_funds_data(self, fundCodes: [], isOptional: bool = False):
        """
        获取持仓基金信息
        :param isOptional: 是否是自选基金
        :param fundCodes: 基金代码列表
        :return:
        """
        print('当前数据源：[{}]'.format(FundConfig.DB_SWITCH))
        if FundConfig.DB_SWITCH == DBSource.YDI:
            return self.get_funds_data_ydi(fundCodes, isOptional)
        elif FundConfig.DB_SWITCH == DBSource.OTH:
            return self.get_funds_data_oth(fundCodes)
        elif FundConfig.DB_SWITCH == DBSource.ANT:
            return self.get_funds_data_ant(fundCodes, isOptional)
        else:
            return self.get_funds_data_ttt(fundCodes, isOptional)

    def get_fund_performance_ydi(self, fundCode: str, startDate: str = ''):
        try:
            url = FundConfig.OTHER_URL + '/fund/detail?code={}&startDate={}'.format(fundCode, startDate)
            resp = self.http_get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                data = resp_json['data']
                return data
        except Exception as e:
            print(e)
        return {}

    def get_fund_performance_ttt(self, fundCode: str, type: str = 'threemonth'):
        if type == 'ONE_MONTH':
            type = 'month'
        elif type == 'THREE_MONTH':
            type = 'threemonth'
        elif type == 'SIX_MONTH':
            type = 'sixmonth'
        elif type == 'ONE_YEAR':
            type = 'year'
        elif type == 'THREE_YEAR':
            type = 'threeyear'

        try:
            url = 'http://fund.eastmoney.com/data/FundPicData.aspx?bzdm={}&n=0&dt={}&vname=ljsylSVG_PicData&r={}'.format(
                fundCode, type, random.random())
            resp = self.http_get(url)
            if resp.status_code == 200:
                result = re.findall('PicData="(.*)";', resp.text)
                result = result[0].split('|')
                data = []
                for i in result:
                    temp = i.split('_')
                    dateTime = temp[0].replace('/', '-')
                    curFund = float(temp[1]) if temp[1] != '' else 0.0
                    hz300 = float(temp[2]) if temp[2] != '' else 0.0
                    if len(temp) == 4:
                        szzs = float(temp[3]) if temp[3] != '' else 0.0
                        data.append([dateTime, curFund, hz300, szzs])
                    else:
                        data.append([dateTime, curFund, hz300])
                return data
        except Exception as e:
            print(e)
        return []

    def get_day_worth(self, fundCode: str, worthDate: str = ''):
        """
        获取具体某天的净值
        :param fundCode: 基金代码
        :param worthDate: 净值日期 为空时默认为上个交易日
        :return:
        """
        ret = self.get_history_worth(fundCode, worthDate, worthDate)
        if worthDate == '' and len(ret) > 1:
            return ret[1]
        else:
            for item in ret:
                if item['netWorthDate'] == worthDate:
                    return item
        return None

    def get_history_worth(self, fundCode: str, startDate: str = '', endDate: str = '', pageSize: int = 10,
                          pageNum: int = 1):
        """
        获取基金的历史净值
        :param pageNum:
        :param pageSize:
        :param fundCode:
        :param startDate:
        :param endDate:
        :return:
        """
        try:
            url = 'http://api.fund.eastmoney.com/f10/lsjz'
            # 参数化访问链接，以dict方式存储
            params = {
                'callback': 'jQuery{}_{}'.format(self.random_str(20), self.get_now_timestamp()),
                'fundCode': fundCode,
                'pageIndex': pageNum,
                'pageSize': pageSize,
                'startDate': startDate,
                'endDate': endDate,
                '_': self.get_now_timestamp()
            }
            # 存储cookie内容
            cookie = 'qgqp_b_id=8eb47817bcd0492676a2cf45e1d7a9d6; _qddaz=QD.pptv1v.pzr5nq.khfqpywc; pgv_pvi=1289374720; em_hq_fls=js; EMFUND1=null; EMFUND2=null; EMFUND3=null; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; em-quote-version=topspeed; HAList=f-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sh-603056-%u5FB7%u90A6%u80A1%u4EFD; st_si=11021199998785; st_asi=delete; EMFUND0=null; EMFUND4=11-25%2017%3A11%3A53@%23%24%u666F%u987A%u957F%u57CE%u65B0%u5174%u6210%u957F%u6DF7%u5408@%23%24260108; EMFUND5=11-27%2019%3A03%3A15@%23%24%u62DB%u5546%u4E2D%u8BC1%u767D%u9152%u6307%u6570%u5206%u7EA7@%23%24161725; EMFUND6=11-27%2019%3A03%3A18@%23%24%u5BCC%u56FD%u4E2D%u8BC1%u94F6%u884C%u6307%u6570@%23%24161029; EMFUND7=11-30%2012%3A25%3A35@%23%24%u4E2D%u6B27%u963F%u5C14%u6CD5%u6DF7%u5408C@%23%24009777; EMFUND8=12-01%2008%3A24%3A12@%23%24%u534E%u590F%u6210%u957F%u6DF7%u5408@%23%24000001; EMFUND9=12-01 08:28:40@#$%u6613%u65B9%u8FBE%u4E2D%u5C0F%u76D8%u6DF7%u5408@%23%24110011; st_pvi=34514567509675; st_sp=2020-10-26%2019%3A56%3A41; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=6; st_psi=20201201083501251-0-0251503392'
            # 装饰头文件
            headers = {
                'Cookie': cookie,
                'Host': 'api.fund.eastmoney.com',
                'User-Agent': self.get_fake_ua(),
                'Referer': 'http://fundf10.eastmoney.com/jjjz_%s.html' % fundCode,
            }
            r = self.http_get(url=url, headers=headers, params=params)  # 发送请求
            result = json.loads(r.text[len(params['callback']) + 1:-1])
            temp = []
            for item in result['Data']['LSJZList']:
                temp.append({
                    'netWorth': item['DWJZ'],
                    'netWorthDate': item['FSRQ'],
                    'netGrowth': item['JZZZL']
                })
            return temp
        except Exception as e:
            print(e)
            return []

    # def get_fund_growth(self, fundCode):
    #     """
    #     获取基金近期涨幅
    #     :param fundCode: 基金代码
    #     :return:
    #     """
    #     try:
    #         url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdzf&code={}&rt={}'.format(fundCode,
    #                                                                                                    random.random())
    #         headers = {
    #             'User-Agent': self.get_fake_ua(),
    #             'Host': 'fundf10.eastmoney.com',
    #             'Referer': 'http://fundf10.eastmoney.com/jdzf_{}.html'.format(fundCode)
    #         }
    #         html = self.http_get(url, headers=headers)
    #         html = html.content.decode('utf-8')
    #         html = re.findall(r'content:"(.*)"};', html)[0]
    #         soup = BeautifulSoup(html, "lxml")
    #         growth = []
    #         for i in soup.select('ul li:nth-child(2)'):
    #             growth.append(i.text.replace('%', ''))
    #         ret = {
    #             "lastWeekGrowth": growth[2],
    #             "lastMonthGrowth": growth[3],
    #             "lastThreeMonthsGrowth": growth[4],
    #             "lastSixMonthsGrowth": growth[5],
    #             "lastYearGrowth": growth[6]
    #         }
    #         return ret
    #     except:
    #         ret = {
    #             "lastWeekGrowth": '0',
    #             "lastMonthGrowth": '0',
    #             "lastThreeMonthsGrowth": '0',
    #             "lastSixMonthsGrowth": '0',
    #             "lastYearGrowth": '0'
    #         }
    #         return ret

    def query_update_worth(self, fundData: dict):
        """
        查询是否需要更新净值
        :param fundData: 基金信息
        :return:
        """
        try:
            if fundData['netWorthDate'] != fundData['expectWorthDate'][0:10] and self.is_query_worth():
                todayDate = datetime.now().strftime('%Y-%m-%d')
                todayWorth = self.get_day_worth(fundData['code'], todayDate)
                if todayWorth is not None:
                    fundData.update(todayWorth)
        except Exception as e:
            print('出现异常：' + str(e))
        return fundData

    def get_all_fund(self):
        url = 'http://fund.eastmoney.com/js/fundcode_search.js'
        resp = self.http_get(url)
        resp = re.findall(r'var r = (.*);', resp.text)[0]
        resp_json = json.loads(resp)
        data = []
        for item in resp_json:
            data.append('{}-{}'.format(item[0], item[2]))
        return data

    # def get_fund_positions(self, fundCode: str):
    #     """
    #     获取基金的持仓
    #     :param fundCode: 基金代码
    #     :return: []
    #     """
    #
    #     try:
    #         url = FundConfig.YDI_URL + '/fund/position?code=' + fundCode
    #         resp = self.http_get(url)
    #         if resp.status_code == 200:
    #             resp_json = resp.json()
    #             data = resp_json['data']
    #             ret = []
    #             stock_codes = []
    #             for item in data['stockList']:
    #                 stock_codes.append(item[0])
    #                 ret.append({
    #                     'code': item[0],
    #                     'name': item[1],
    #                     'proportion': item[2],
    #                     'holdUnits': item[3],
    #                     'holdAmount': item[4]
    #                 })
    #             stock_codes = ','.join(stock_codes)
    #             url = FundConfig.YDI_URL + '/stock?code=' + stock_codes
    #             resp = self.http_get(url)
    #             resp_json = resp.json()
    #             data = resp_json['data']
    #             for index, item in enumerate(ret):
    #                 item['changePercent'] = data[index]['changePercent']
    #             # print(ret)
    #             return ret
    #     except Exception as e:
    #         print(e)
    #     return []

    def get_fund_positions(self, fundCode: str):
        """
        获取基金的持仓
        :param fundCode: 基金代码
        :return: []
        """
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': self.get_fake_ua()
            }
            params = {
                'plat': 'Android',
                'appType': 'ttjj',
                'product': 'EFund',
                'Version': '2.0.0',
                'deviceid': 'Wap',
                'FCODE': fundCode,
                '_': self.get_now_timestamp()
            }
            resp = self.http_get(url, params=params, headers=headers)
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
                stock_info = self.get_stocks_info(stock_codes)
                for index, item in enumerate(ret):
                    item['changePercent'] = stock_info[index]['f3']
                return ret
        except Exception as e:
            print(e)
        return []

    def get_stocks_info(self, stock_codes: str):
        try:
            url = 'https://push2.eastmoney.com/api/qt/ulist.np/get'
            headers = {
                'Host': 'push2.eastmoney.com',
                'User-Agent': self.get_fake_ua()
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
            resp = self.http_get(url, headers=headers, params=params)
            resp_json = resp.json()
            return resp_json['data']['diff']
        except:
            pass
            return []

    def get_fund_info(self, fundCode: str):
        """
        获取基金的基础信息
        :param fundCode:
        :return:
        """
        data = {}
        try:
            url = 'https://fundmobapi.eastmoney.com/FundMApi/FundBaseTypeInformation.ashx'
            headers = {
                'Host': 'fundmobapi.eastmoney.com',
                'User-Agent': self.get_fake_ua()
            }
            params = {
                'plat': 'Android',
                'appType': 'ttjj',
                'product': 'EFund',
                'Version': '1',
                'deviceid': 'Wap',
                'FCODE': fundCode,
                '_': self.get_now_timestamp()
            }
            resp = requests.get(url, headers=headers, params=params)
            resp_json = resp.json()
            return resp_json['Datas']
        except:
            pass
        return data

    def http_get(self, url: str, headers: dict = None, params: dict = None):
        """
        使用代理调用get
        :param url: 地址
        :param params: 参数
        :param headers: 请求头
        :return:
        """
        session = requests.Session()
        session.trust_env = False
        if FundConfig.ENABLE_PROXY:
            retry_count = 5
            proxy = self.get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    return session.get(url, timeout=5, headers=headers, params=params,
                                       proxies={"http": "http://{}".format(proxy)})
                except Exception as e:
                    print(e)
                    retry_count -= 1
            # 删除代理池中代理
            self.delete_proxy(proxy)
            return None
        else:
            os.environ['no_proxy'] = '*'
            return session.get(url, timeout=5, headers=headers, params=params)

    def http_post(self, url: str, data: dict = None, headers: dict = None):
        """
        使用代理调用get
        :param url: 地址
        :param data: 数据
        :param headers: 请求头
        :return:
        """
        session = requests.Session()
        session.trust_env = False

        if FundConfig.ENABLE_PROXY:
            retry_count = 5
            proxy = self.get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    resp = session.post(url, data, headers=headers, timeout=5,
                                        proxies={"http": "http://{}".format(proxy)})
                    return resp
                except Exception as e:
                    print(e)
                    retry_count -= 1
            # 删除代理池中代理
            self.delete_proxy(proxy)
            return None
        else:
            os.environ['no_proxy'] = '*'
            return session.post(url, data, headers=headers, timeout=5)

    def get_proxy(self):
        """
        获取代理地址
        :return:
        """
        return requests.get(FundConfig.PROXY_POOL + "/get/").json()

    def delete_proxy(self, proxy):
        """
        删除代理
        :param proxy: 代理地址
        :return:
        """
        requests.get(FundConfig.PROXY_POOL + "/delete/?proxy={}".format(proxy))

    def random_str(self, length=10):
        """
        生产随机字符串
        :param length: 长度
        :return: 字符串
        """
        return ''.join(str(random.choice(range(10))) for _ in range(length))

    def get_now_timestamp(self):
        """
        获取当前的时间戳 13位
        :return: int 时间戳
        """
        return int(round(time.time() * 1000))

    def split_array(self, array, size):
        """
        拆分数组
        :param array:  数组
        :param size: 每组的大小
        :return:
        """
        return [array[i:i + size] for i in range(0, len(array), size)]

    def get_fake_ua(self):
        ua = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
            'Opera/8.0 (Windows NT 5.1; U; en)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
        ]
        return random.choice(ua)

    def is_query_worth(self):
        """
        判断是否需要查询净值
        交易日 19.30之后
        :return:
        """
        nowTime = datetime.now()
        return is_workday(nowTime) and nowTime.hour >= 19 and nowTime.minute >= 0

    def get_last_work_day(self, curDate: str):
        curDatetime = datetime.strptime(curDate, '%Y-%m-%d')
        i = -1
        yesterday = curDatetime + timedelta(days=i)  # 昨天日期
        while not is_workday(yesterday):
            i = i - 1
            yesterday = curDatetime + timedelta(days=i)  # 昨天日期
        return yesterday.strftime('%Y-%m-%d')


if __name__ == '__main__':
    # pass
    fund = FundCrawler()
    # ret = fund.get_day_worth('009777', '2020-12-23')
    # ret = fund.get_funds_data(['110011'])
    # ret = fund.get_board_data_bak()
    # ret = fund.get_fund_performance_ydi('110011')
    # ret = fund.get_history_worth('110011', '2020-09-04', '2020-12-04', 93, 1)
    # ret = fund.get_fund_performance_ttt('110011', 'THREE_MONTH')
    # ret = fund.get_funds_data_ttt(['110011'])
    # ret = fund.get_all_fund()
    # ret = fund.get_fund_positions('110011')
    ret = fund.get_last_work_day('2020-12-20')
    print(ret)
