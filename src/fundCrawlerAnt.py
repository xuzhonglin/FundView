import json
import queue
import re
import threading
import time
from datetime import datetime

import requests
from fundConfig import FundConfig


class FundCrawlerAnt:

    def __init__(self, fundCode: str):
        self.fundCode = fundCode
        self.csrf = ''
        self.productId = ''
        self.fundInfo = {}
        self.fundName = ''
        self.netWorth = ''
        self.netGrowth = ''
        self.netWorthDate = ''
        self.curYear = time.localtime(time.time()).tm_year
        self.cookies = ''
        # self._init_fund(fundCode)

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
        ret_json = json.loads(result)
        self.fundInfo = ret_json['materialInfo']
        self.csrf = ret_json['csrf']
        self.fundName = ret_json['materialInfo']['fundBrief']['fundNameAbbr']
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
        return resp.json()

    def get_fund_data(self):
        self._init_fund(self.fundCode)
        ret = self.get_fund_expectWorth()['list'][-1]
        timeStamp = int(ret['time'] / 1000)
        dateArray = datetime.fromtimestamp(timeStamp)
        expectWorthDate = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "code": self.fundCode,
            "name": self.fundName,
            "netWorth": self.netWorth,
            "netWorthDate": self.netWorthDate,
            "dayGrowth": self.netGrowth,
            "expectWorth": ret['forecastNetValue'],
            "expectWorthDate": expectWorthDate,
            "expectGrowth": ret['forecastGrowth']
        }
        print("%s %s" % (threading.current_thread().name, data))
        # print(time.time(), data)
        return data


def get_fund_data_ant(fundCodes: [], isOptional: bool = False):
    from concurrent.futures import ThreadPoolExecutor
    startTime = time.time()
    threadPool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="thread")

    for fundCode in fundCodes:
        antCrawler = FundCrawlerAnt(fundCode)
        threadPool.submit(antCrawler.get_fund_data)
    threadPool.shutdown(wait=True)
    # fund_code_queue = queue.Queue(len(fundCodes))
    # for fundCode in fundCodes:
    #     fund_code_queue.put(fundCode)
    #     # 创建一个线程锁，防止多线程写入文件时发生错乱
    # mutex_lock = threading.Lock()
    # 线程数为50，在一定范围内，线程数越多，速度越快
    # for index, fundCode in enumerate(fundCodes):
    #     antCrawler = FundCrawlerAnt(fundCode)
    #     t = threading.Thread(target=antCrawler.get_fund_data, name='LoopThread' + str(index))
    #     t.start()

    # for fundCode in fundCodes:
    #     antCrawler = FundCrawlerAnt(fundCode)
    #     antCrawler.get_fund_data()
    endTime = time.time()
    print('执行耗时：{}'.format(endTime - startTime))


fundCodes = [
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
    "005693"
]
get_fund_data_ant(fundCodes)
#
# fund = FundCrawlerAnt('110011')
#
# fund.get_fund_data()
