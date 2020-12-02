import json
import random
import re
import time

import requests
from bs4 import BeautifulSoup


class FundCrawler:
    URL = 'https://api.yiduu.com/v1'
    PROXY_POOL = 'http://proxy-pool.colinxu.cn'
    ENABLE_PROXY = False

    def __init__(self):
        pass

    def get_proxy(self):
        """
        获取代理地址
        :return:
        """
        return requests.get(self.PROXY_POOL + "/get/").json()

    def delete_proxy(self, proxy):
        """
        删除代理
        :param proxy: 代理地址
        :return:
        """
        requests.get(self.PROXY_POOL + "/delete/?proxy={}".format(proxy))

    def get_board_info(self):
        """
        获取大盘信息
        :return:
        """
        try:
            url = self.URL + '/stock/board'
            resp = self.http_get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                return resp_json['data']
        except Exception as e:
            print(e)
        return []

    def get_funds_data_bak(self, fundCode: []):
        """
        获取持仓基金信息
        :param fundCode: 基金代码列表
        :return:
        """
        try:
            fundCodeArray = self.split_array(fundCode, 12)
            data = []
            for subArray in fundCodeArray:
                fundCodes = ','.join(subArray)
                url = self.URL + '/fund?code=' + fundCodes
                resp = self.http_get(url)
                if resp.status_code == 200:
                    resp_json = resp.json()
                    data.extend(resp_json['data'])
            return data
        except Exception as e:
            print(e)
        return []

    def get_funds_data(self, fundCodes: [], isOptional: bool = False):
        """
        获取持仓基金信息
        :param isOptional: 是否是自选基金
        :param fundCodes: 基金代码列表
        :return:
        """
        data = []
        try:
            for fundCode in fundCodes:
                url = "http://fundgz.1234567.com.cn/js/%s.js" % fundCode
                # 浏览器头
                headers = {'content-type': 'application/json',
                           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
                r = requests.get(url, headers=headers)
                # 返回信息
                content = r.text
                # 正则表达式
                pattern = r'^jsonpgz\((.*)\)'
                # 查找结果
                result = re.findall(pattern, content)[0]
                result = json.loads(result)
                # 遍历结果
                temp = {
                    "code": result['fundcode'],
                    "name": result['name'],
                    "netWorth": result['dwjz'],
                    "netWorthDate": result['jzrq'],
                    "dayGrowth": "0.72",
                    "expectWorth": result['gsz'],
                    "expectWorthDate": result['gztime'],
                    "expectGrowth": result['gszzl']
                }
                if isOptional:
                    temp.update(self.get_fund_growth(fundCode))
                # temp.
                data.append(temp)
            return data
        except Exception as e:
            print(e)
            return data

    def get_day_worth(self, fundCode: str, worthDate: str = ''):
        """
        获取具体某天的净值
        :param fundCode: 基金代码
        :param worthDate: 净值日期 为空时默认为上个交易日
        :return:
        """
        ret = self.get_history_worth(fundCode, worthDate, worthDate)
        if worthDate == '':
            return ret[1]
        else:
            for item in ret:
                if item['netWorthDate'] == worthDate:
                    return item

    def get_history_worth(self, fundCode: str, startDate: str = '', endDate: str = '', pageSize: int = 10,
                          pageNum: int = 1):
        """
        获取基金的历史净值
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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
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

    def get_fund_growth(self, fundCode):
        try:
            url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdzf&code={}&rt={}'.format(fundCode,
                                                                                                       random.random())
            headers = {
                'User-Agent': self.get_fake_ua(),
                'Host': 'fundf10.eastmoney.com',
                'Referer': 'http://fundf10.eastmoney.com/jdzf_{}.html'.format(fundCode)
            }
            html = self.http_get(url, headers=headers)
            html = html.content.decode('utf-8')
            html = re.findall(r'content:"(.*)"};', html)[0]
            soup = BeautifulSoup(html, "lxml")
            growth = []
            for i in soup.select('ul li:nth-child(2)'):
                growth.append(i.text.replace('%', ''))
            ret = {
                "lastWeekGrowth": growth[2],
                "lastMonthGrowth": growth[3],
                "lastThreeMonthsGrowth": growth[4],
                "lastSixMonthsGrowth": growth[5],
                "lastYearGrowth": growth[6]
            }
            return ret
        except:
            ret = {
                "lastWeekGrowth": '0',
                "lastMonthGrowth": '0',
                "lastThreeMonthsGrowth": '0',
                "lastSixMonthsGrowth": '0',
                "lastYearGrowth": '0'
            }
            return ret

    def get_fund_positions(self, fundCode: str):
        """
        获取基金的持仓
        :param fundCode: 基金代码
        :return: []
        """
        try:
            url = self.URL + '/fund/position?code=' + fundCode
            resp = self.http_get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                data = resp_json['data']
                ret = []
                for item in data['stockList']:
                    ret.append({
                        'code': item[0],
                        'name': item[1],
                        'proportion': item[2],
                        'holdUnits': item[3],
                        'holdAmount': item[4]
                    })
                return ret
        except Exception as e:
            print(e)
        return []

    def http_get(self, url: str, headers: dict = None, params: dict = None):
        """
        使用代理调用get
        :param url: 地址
        :param params: 参数
        :param headers: 请求头
        :return:
        """
        if self.ENABLE_PROXY:
            retry_count = 5
            proxy = self.get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    return requests.get(url, timeout=5, headers=headers, params=params,
                                        proxies={"http": "http://{}".format(proxy)})
                except Exception as e:
                    print(e)
                    retry_count -= 1
            # 删除代理池中代理
            self.delete_proxy(proxy)
            return None
        else:
            return requests.get(url, timeout=5, headers=headers, params=params)

    def http_post(self, url: str, data: dict = None, headers: dict = None):
        """
        使用代理调用get
        :param url: 地址
        :param data: 数据
        :param headers: 请求头
        :return:
        """
        if self.ENABLE_PROXY:
            retry_count = 5
            proxy = self.get_proxy().get("proxy")
            while retry_count > 0:
                try:
                    resp = requests.post(url, data, headers=headers, timeout=5,
                                         proxies={"http": "http://{}".format(proxy)})
                    return resp
                except Exception as e:
                    print(e)
                    retry_count -= 1
            # 删除代理池中代理
            self.delete_proxy(proxy)
            return None
        else:
            return requests.post(url, data, headers=headers, timeout=5)

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


if __name__ == '__main__':
    fund = FundCrawler()
    # ret = fund.get_history_worth('110011')
    # ret = fund.get_funds_data(['110011'])
    ret = fund.get_fund_growth('009777')
    print(ret)
