import json
import re
import time
from datetime import datetime

import requests
from src.fund_config import FundConfig


class FundAnt:
    def get_fund_data(self, fundCode: str, isOptional: bool = False):
        try:
            url = 'http://www.fund123.cn/matiaria?fundCode={}'.format(fundCode)
            html = requests.get(url)
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
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
            }
            data = {
                "startTime": "2020-12-03",
                "endTime": "2020-12-04",
                "limit": 20,
                "productId": productId,
                "format": True,
                "source": "WEALTHBFFWEB"
            }
            resp = requests.post(url, data=data, headers=headers).json()
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
