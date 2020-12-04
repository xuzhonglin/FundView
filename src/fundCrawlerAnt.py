import json
import re
import time

import requests
from fundConfig import FundConfig


class FundCrawlerAnt:

    def __init__(self, fundCode: str):
        self.fundCode = fundCode
        self.csrf = ''
        self.productId = ''
        self.fundInfo = {}
        self.netWorth = ''
        self.netGrowth = ''
        self.netWorthDate = ''
        self.curYear = time.localtime(time.time()).tm_year
        self.cookies = ''
        self._init_fund(fundCode)

    def _init_fund(self, fundCode):
        url = 'http://www.fund123.cn/matiaria?fundCode={}'.format(fundCode)
        html = requests.get(url)
        cookies = html.headers['set-cookie']
        for i in cookies.split(','):
            sub = i.split(';')
            self.cookies = self.cookies + sub[0] + ';'
        # 查找结果
        result = re.findall(r'window.context = (.*);', html.text)
        result = result[0]
        print(result)
        ret_json = json.loads(result)
        self.fundInfo = ret_json['materialInfo']
        self.csrf = ret_json['csrf']
        self.productId = ret_json['materialInfo']['productId']
        self.netWorth = ret_json['materialInfo']['titleInfo']['netValue']
        self.netWorthDate = str(self.curYear) + '-' + ret_json['materialInfo']['titleInfo']['netValueDate']
        self.netGrowth = ret_json['materialInfo']['titleInfo']['dayOfGrowth']

    def get_fund_expectWorth(self):
        url = FundConfig.ANT_URL + '/queryFundEstimateIntraday?_csrf={}'.format(self.csrf)
        headers = {
            'Cookie': self.cookies,
            "Origin": "http://www.fund123.cn",
            "Referer": "http://www.fund123.cn/matiaria?fundCode={}".format(self.fundCode),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }
        data = {
            "startTime": "2020-12-03",
            "endTime": "2020-12-04",
            "limit": 20,
            "productId": self.productId,
            "format": True,
            "source": "WEALTHBFFWEB"
        }
        resp = requests.post(url, data=data, headers=headers)
        print(resp.text)


fund = FundCrawlerAnt('110011')

fund.get_fund_expectWorth()
