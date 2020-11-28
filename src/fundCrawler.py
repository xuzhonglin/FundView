import requests


class FundCrawler:
    URL = 'https://fund.yiduu.com/'

    def __init__(self):
        pass

    def get_board_info(self):
        try:
            url = 'https://api.yiduu.com/v1/stock/board'
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                return resp_json['data']
        except Exception as e:
            pass
        return []


if __name__ == '__main__':
    fund = FundCrawler()
    ret = fund.get_board_info()
    print(ret)
