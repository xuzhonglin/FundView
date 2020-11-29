import os, requests

from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtGui import QResizeEvent, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QHeaderView
from ui.fundViewForm import Ui_MainWindow
from src.fundCrawler import FundCrawler
# import jpype
import traceback

RED_STR = '<span style=" color:#ff0000;">{}</span>'
GREEN_STR = '<span style=" color:#00aa00;">{}</span>'


class FundViewMain(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fundCrawler = FundCrawler()
        self.positionModel = QStandardItemModel(0, 10)
        self.start_init()

    def start_init(self):
        self.refresh_board_data()
        self.init_position_table()
        self.refresh_position_data()

    def init_slot(self):
        self.positionRefreshBtn.click.connect(self.refresh_position_data)

    def init_position_table(self):
        #  设置水平方向两个头标签文本内容
        self.positionModel.setHorizontalHeaderLabels(
            ['基金名称', '基金编码', '成本金额', '持仓成本', '持仓份额', '持有收益', '持有收益率', '净值', '估值', '预计收益'])
        self.tableView.setModel(self.positionModel)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def refresh_board_data(self):
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

    def refresh_position_data(self):
        ret = self.fundCrawler.get_position_data()
        for index, item in enumerate(ret):
            fundName = QStandardItem(item['name'])
            fundCode = QStandardItem(item['code'])
            dayGrowth = QStandardItem(item['dayGrowth'])
            expectGrowth = QStandardItem(item['expectGrowth'])

            self.positionModel.setItem(index, 0, fundName)
            self.positionModel.setItem(index, 1, fundCode)
            self.positionModel.setItem(index, 7, dayGrowth)

            self.positionModel.setItem(index, 8, expectGrowth)
        self.tableView.setModel(self.positionModel)
