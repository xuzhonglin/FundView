import requests


class FundCrawler:
    URL = 'https://api.yiduu.com/v1'

    def __init__(self):
        pass

    def get_board_info(self):
        try:
            url = self.URL + '/stock/board'
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                return resp_json['data']
        except Exception as e:
            pass
        return []

    def get_position_data(self, fundCode: []):
        try:
            fundCodes = ','.join(fundCode)
            url = self.URL + '/fund?code=' + fundCodes
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                return resp_json['data']
        except Exception as e:
            pass
        return []


if __name__ == '__main__':
    fund = FundCrawler()
    ret = fund.get_position_data()
    print(ret)
