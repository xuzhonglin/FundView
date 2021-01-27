from PyQt5.QtCore import QThread, pyqtSignal

from src.fund_crawler import FundCrawler


class MyThread(QThread):
    BDone = pyqtSignal(list)
    PDone = pyqtSignal(list)
    ODone = pyqtSignal(list)

    StartDone = pyqtSignal()

    def __init__(self, positionFund: dict, optionalFund: list):
        super(MyThread, self).__init__()
        self.positionFund = positionFund
        self.optionalFund = optionalFund
        self.fundCrawler = FundCrawler()

    def __del__(self):
        self.wait()

    def run(self):
        # 刷新大盘数据
        board_ret = self.fundCrawler.get_board_info()
        self.BDone.emit(board_ret)

        # 刷新持仓数据
        keys = []
        for key in self.positionFund:
            keys.append(key)
        position_ret = self.fundCrawler.get_funds_data(keys)
        self.PDone.emit(position_ret)

        # 刷新自选数据
        optional_ret = self.fundCrawler.get_funds_data(self.optionalFund, isOptional=True)
        self.ODone.emit(optional_ret)

        print("数据加载完成")
        self.StartDone.emit()
