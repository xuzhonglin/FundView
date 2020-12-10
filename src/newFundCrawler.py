import json
import random
import re

import requests
from bs4 import BeautifulSoup


def get_fake_ua():
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


def get_fund_data(fundCode: str):
    url = 'http://fund.eastmoney.com/{}.html'.format(fundCode)
    fundData = {}
    headers = {
        'User-Agent': get_fake_ua(),
        'Host': 'fund.eastmoney.com',
        'Referer': url
    }
    html = requests.get(url, headers=headers)
    html = html.content.decode('utf-8')
    soup = BeautifulSoup(html, "lxml")

    title = soup.select('.fundDetail-tit > div')[0]
    fundCode = title.text.split('(')[0]
    fundName = title.text.split('(')[1]
    fundData['code'] = fundCode
    fundData['name'] = fundName

    # 获取净值
    netWorthHtml = soup.select('div.dataOfFund > dl.dataItem02 > dd.dataNums > span')
    fundData['netWorth'] = netWorthHtml[0].get_text()
    fundData['dayGrowth'] = netWorthHtml[1].get_text().replace('%', '')
    netWorthDate = soup.select('div.dataOfFund > dl.dataItem02 > dt > p')[0].text[-11:-1]
    fundData['netWorthDate'] = netWorthDate

    buyRate = soup.select('span.nowPrice')[0].text
    fundData['buyRate'] = buyRate.replace('%', '')

    # 持仓股票
    expectWorthHtml = soup.select('#position_shares > div.poptableWrap > table')
    for i in expectWorthHtml[0].findAll('tr')[1:]:
        temp = i.findAll('td')
        a = temp[0].find('a').get_text()
        b = temp[1].get_text().replace('%', '')
        c = temp[2].find('span').get_text().replace('%', '')
        print(a, b, c)

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

    print(fundData)


def get_fund_growth(fundCode):
    url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jdzf&code={}&rt={}'.format(fundCode,
                                                                                               random.random())
    headers = {
        'User-Agent': get_fake_ua(),
        'Host': 'fundf10.eastmoney.com',
        'Referer': 'http://fundf10.eastmoney.com/jdzf_{}.html'.format(fundCode)
    }
    html = requests.get(url, headers=headers)
    html = html.content.decode('utf-8')
    html = re.findall(r'content:"(.*)"};', html)[0]
    soup = BeautifulSoup(html, "lxml")
    growth = []
    for i in soup.select('ul li:nth-child(2)'):
        growth.append(i.text.replace('%', ''))
    ret = {
        "lastWeekGrowth": growth[1],
        "lastMonthGrowth": growth[2],
        "lastThreeMonthsGrowth": growth[3],
        "lastSixMonthsGrowth": growth[4],
        "lastYearGrowth": growth[5]
    }
    print(ret)
    return ret


def get_fund_positions(fundCode):
    url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=&month=&rt={}'.format(
        fundCode,
        random.random())
    headers = {
        'User-Agent': get_fake_ua(),
        'Host': 'fundf10.eastmoney.com',
        'Referer': 'http://fundf10.eastmoney.com/ccmx_{}.html'.format(fundCode)
    }
    html = requests.get(url, headers=headers)
    html = html.content.decode('utf-8')
    print(html)
    html = re.findall(r'content:"(.*)",', html)[0]
    print(html)
    soup = BeautifulSoup(html, "lxml")
    growth = []
    for i in soup.select('ul li:nth-child(2)'):
        growth.append(i.text.replace('%', ''))
    ret = {
        "lastWeekGrowth": growth[1],
        "lastMonthGrowth": growth[2],
        "lastThreeMonthsGrowth": growth[3],
        "lastSixMonthsGrowth": growth[4],
        "lastYearGrowth": growth[5]
    }
    print(ret)
    return ret


get_fund_data('110011')
