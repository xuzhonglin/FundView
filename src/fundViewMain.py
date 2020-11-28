import os, requests

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from ui.fundViewForm import Ui_MainWindow
from fundCrawler import FundCrawler
# import jpype
import traceback

RED_STR = '<span style=" color:#ff0000;">{}</span>'
GREEN_STR = '<span style=" color:#00aa00;">{}</span>'


class FundViewMain(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fundCrawler = FundCrawler()
        self.start_init()

    def start_init(self):
        ret = self.fundCrawler.get_board_info()
        for board_item in ret:
            # fund_name = board_item["name"]
            fund_code = board_item["code"]
            priceChange = board_item["priceChange"]
            # 上涨还是下跌
            isRaiseFall = float(priceChange) > 0
            price = board_item["price"]
            priceChange = "+" + priceChange if isRaiseFall else "-" + priceChange
            changePercent = board_item["changePercent"]
            changePercent = "+" + changePercent if isRaiseFall > 0 else "-" + changePercent
            changePercent = changePercent + " %"
            colorString = RED_STR if isRaiseFall else GREEN_STR
            # 变色
            price = colorString.format(price)
            priceChange = colorString.format(priceChange)
            changePercent = colorString.format(changePercent)
            if fund_code == "sh000001":
                self.SHZ_Price.setText(price)
                self.SHZ_PriceChange.setText(priceChange)
                self.SHZ_ChangePercent.setText(changePercent)
            elif fund_code == "sz399001":
                self.SZZ_Price.setText(price)
                self.SZZ_PriceChange.setText(priceChange)
                self.SZZ_ChangePercent.setText(changePercent)
            elif fund_code == "sz399300":
                self.HS_Price.setText(price)
                self.HS_PriceChange.setText(priceChange)
                self.HS_ChangePercent.setText(changePercent)
            elif fund_code == "sh000905":
                self.ZZ_Price.setText(price)
                self.ZZ_PriceChange.setText(priceChange)
                self.ZZ_ChangePercent.setText(changePercent)
            elif fund_code == "sz399006":
                self.CY_Price.setText(price)
                self.CY_PriceChange.setText(priceChange)
                self.CY_ChangePercent.setText(changePercent)
