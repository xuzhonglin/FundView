import json
import random
import time

import requests


class FundCrawler:
    URL = 'https://api.yiduu.com/v1'

    def __init__(self):
        pass

    def get_board_info(self):
        """
        获取大盘信息
        :return:
        """
        try:
            url = self.URL + '/stock/board'
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                return resp_json['data']
        except Exception as e:
            pass
        return []

    def get_funds_data(self, fundCode: []):
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
                resp = requests.get(url)
                if resp.status_code == 200:
                    resp_json = resp.json()
                    data.extend(resp_json['data'])
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
        r = requests.get(url=url, headers=headers, params=params)  # 发送请求
        result = json.loads(r.text[len(params['callback']) + 1:-1])
        temp = []
        for item in result['Data']['LSJZList']:
            temp.append({
                'netWorth': item['DWJZ'],
                'netWorthDate': item['FSRQ'],
                'netGrowth': item['JZZZL']
            })
        return temp

    def get_fund_positions(self, fundCode: str):
        """
        获取基金的持仓
        :param fundCode: 基金代码
        :return: []
        """
        try:
            url = self.URL + '/fund/position?code=' + fundCode
            resp = requests.get(url)
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


if __name__ == '__main__':
    fund = FundCrawler()
    # ret = fund.get_history_worth('110011', '', '')
    ret = fund.get_fund_positions('110011')
    print(ret)
