import json
import os, requests
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QMenu

from ui.fundTableDialog import Ui_FundTableDialog
from src.fundCrawler import FundCrawler
# import jpype
import traceback

RED_STR = '<span style=" color:#ff0000;">{}</span>'
GREEN_STR = '<span style=" color:#00aa00;">{}</span>'
RED = QBrush(QColor('#ff0000'))
GREEN = QBrush(QColor('#00aa00'))
STYLE_RED = 'color: rgb(255, 0, 0);'
STYLE_GREEN = 'color: rgb(0, 170, 0);'


class FundTableMain(QMainWindow, Ui_FundTableDialog):

    def __init__(self, parent, fundCode: str, tableType: int):
        """
        构造函数
        :param fundCode: 基金代码
        :param tableType: 表格类型 ：1 历史净值，2 持仓股票
        """
        super().__init__()
        self.setupUi(parent)
        self.tableType = tableType
        self.fundCode = fundCode
        self.fundCrawler = FundCrawler()
        self.pageNum = 1
        if tableType == 1:
            self.refreshBtn.hide()
        elif tableType == 2:
            self.refreshBtn.hide()
            self.moreBtn.hide()
        self.init_slot()
        self.init_table_header()
        self.init_table_data()

    def init_slot(self):
        self.moreBtn.clicked.connect(lambda: self.init_table_data(True))

    def init_table_header(self):
        """
        初始化表头
        :param tableType:表格类型
        :return:
        """
        self.fundTable.clear()
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.fundTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fundTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # self.positionTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:#f5f5f5;}")
        # 设置整行选中
        self.fundTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.fundTable.verticalHeader().hide()
        # 设置选中行是表头不加粗
        # self.positionTable.horizontalHeader().setHighlightSections(False)

        # 设置行高
        self.fundTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 调整第 1-3列的宽度 为适应内容
        # self.fundTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        if self.tableType == 1:
            # 设置一共10列
            self.fundTable.setColumnCount(3)
            #  设置水平方向两个头标签文本内容
            self.fundTable.setHorizontalHeaderLabels(['日期', '净值', '涨幅'])

        elif self.tableType == 2:
            # 设置一共10列
            self.fundTable.setColumnCount(3)
            #  设置水平方向两个头标签文本内容
            self.fundTable.setHorizontalHeaderLabels(['股票', '占比', '持股数'])

    def init_table_data(self, isMore: bool = False):
        if self.tableType == 1:
            base_row_cnt = 0
            if isMore:
                self.pageNum = self.pageNum + 1
                base_row_cnt = self.fundTable.rowCount()
            list = self.fundCrawler.get_history_worth(self.fundCode, pageSize=20, pageNum=self.pageNum)
            self.fundTable.setRowCount(base_row_cnt + len(list))
            for index, item in enumerate(list):
                row = index + base_row_cnt if isMore else index

                self.fundTable.setItem(row, 0, QTableWidgetItem(item['netWorthDate']))
                self.fundTable.setItem(row, 1, QTableWidgetItem(item['netWorth']))
                netGrowth = float(item['netGrowth'])
                netGrowthColor = RED if netGrowth >= 0 else GREEN
                self.fundTable.setItem(row, 2, QTableWidgetItem("{}%".format(netGrowth)))
                self.fundTable.item(row, 2).setForeground(netGrowthColor)

        elif self.tableType == 2:
            list = self.fundCrawler.get_fund_positions(self.fundCode)
            self.fundTable.setRowCount(len(list))
            for index, item in enumerate(list):
                self.fundTable.setItem(index, 0, QTableWidgetItem("{}({})".format(item['name'], item['code'])))
                self.fundTable.setItem(index, 1, QTableWidgetItem("{}".format(item['proportion'])))
                self.fundTable.setItem(index, 2, QTableWidgetItem("{}".format(item['holdUnits'])))
