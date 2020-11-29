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

    def get_position_data(self):
        try:
            url = self.URL + '/fund?code=001510,161029,009777,260108,007020,161725'
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
