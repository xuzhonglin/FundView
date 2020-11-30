import json
import os, requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QMenu

from addFundDialog import Ui_AddFundDialog
from ui.fundViewForm import Ui_MainWindow
from src.fundCrawler import FundCrawler
# import jpype
import traceback

RED_STR = '<span style=" color:#ff0000;">{}</span>'
GREEN_STR = '<span style=" color:#00aa00;">{}</span>'
RED = QBrush(QColor('#ff0000'))
GREEN = QBrush(QColor('#00aa00'))
STYLE_RED = 'color: rgb(255, 0, 0);'
STYLE_GREEN = 'color: rgb(0, 170, 0);'


class FundViewMain(QMainWindow, Ui_MainWindow):

    # fundSaveSignal=pySignal

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_slot()
        self.fundCrawler = FundCrawler()
        self.positionModel = QStandardItemModel(0, 11)
        self.fundConfigOrigin = {}
        self.positionFund = {}
        self.start_init()

    def start_init(self):
        self.read_local_config()
        self.parse_fund_config()
        self.refresh_board_data()
        self.init_position_table()
        self.refresh_position_data()

        # print(self.fundConfigOrigin)
        print(self.positionFund)

    def init_slot(self):
        self.positionRefreshBtn.clicked.connect(self.refresh_btn_clicked)
        self.addFundBtn.clicked.connect(lambda: self.fund_add_edit_clicked(True))
        self.editFundBtn.clicked.connect(lambda: self.fund_add_edit_clicked(False))

    def refresh_btn_clicked(self):
        print('refresh_btn_click')
        self.refresh_board_data()
        self.refresh_position_data()

    def init_position_table(self):
        self.positionTable.clearContents()
        # 设置一共10列
        self.positionTable.setColumnCount(11)
        #  设置水平方向两个头标签文本内容
        self.positionTable.setHorizontalHeaderLabels(
            ['基金名称', '基金编码', '持仓成本', '持有份额', '持有金额', '持有收益', '持有收益率', '单位净值', '估算净值', '估值浮动', '预计收益'])
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.positionTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.positionTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # self.positionTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:#f5f5f5;}")
        # 设置整行选中
        self.positionTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.positionTable.verticalHeader().hide()
        # 设置选中行是表头不加粗
        # self.positionTable.horizontalHeader().setHighlightSections(False)

        # 设置行高
        self.positionTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # self.positionTable.setColumnWidth(1, 40)

        # 调整第 1-3列的宽度 为适应内容
        self.positionTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.positionTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.positionTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 允许弹出菜单
        self.positionTable.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        self.positionTable.customContextMenuRequested.connect(self.position_table_menu)

    def position_table_menu(self, pos):
        print(pos)
        contextMenu = QMenu(self.positionTable)
        menu1 = contextMenu.addAction('历史净值')
        menu2 = contextMenu.addAction('基金持仓')
        menu3 = contextMenu.addAction('净值图')
        menu4 = contextMenu.addAction('估值图')
        action = contextMenu.exec_(self.positionTable.mapToGlobal(pos))

        # 得到索引
        # for i in self.tableWidget.selectionModel().selection().indexes():
        #     rowNum = i.row()

        # 如果选择的行索引小于1，弹出上下文菜单
        # if rowNum < 3:
        #     menu = QMenu()
        #     item1 = menu.addAction("菜单1")
        #     item2 = menu.addAction("菜单2")
        #     item3 = menu.addAction("菜单3")
        #     # 使菜单在正常位置显示
        #     screenPos = self.tableWidget.mapToGlobal(pos)
        #
        #     # 单击一个菜单项就返回，使之被阻塞
        #     action = menu.exec(screenPos)
        #     if action == item1:
        #         print('选择菜单1', self.tableWidget.item(rowNum, 0).text())
        #     if action == item2:
        #         print('选择菜单2', self.tableWidget.item(rowNum, 0).text())
        #     if action == item3:
        #         print('选择菜单3', self.tableWidget.item(rowNum, 0).text())
        #     else:
        #         return

    def refresh_board_data(self):
        ret = self.fundCrawler.get_board_info()
        for board_item in ret:
            # fund_name = board_item["name"]
            fund_code = board_item["code"]
            priceChange = board_item["priceChange"]
            # 上涨还是下跌
            isRaiseFall = float(priceChange) > 0
            price = board_item["price"]
            priceChange = "+" + priceChange if isRaiseFall else "" + priceChange
            changePercent = board_item["changePercent"]
            changePercent = "+" + changePercent if isRaiseFall > 0 else "" + changePercent
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
        ret = self.fundCrawler.get_position_data(self.positionFund.keys())
        self.positionTable.clearContents()
        self.positionTable.setRowCount(len(ret))
        todayExpectIncome = 0
        totalIncome = 0
        holdAmount = 0
        worthDate = ''
        for index, item in enumerate(ret):
            print(index, item)
            fundCode = item['code']
            worthDate = item['expectWorthDate']

            fundHold = self.positionFund[fundCode]

            # 1.基金名称
            fundNameItem = QTableWidgetItem(item['name'])
            self.positionTable.setItem(index, 0, fundNameItem)

            # 2.基金代码
            fundCodeItem = QTableWidgetItem(item['code'])
            self.positionTable.setItem(index, 1, fundCodeItem)

            # 3.持仓成本
            fundHoldCost = fundHold['fundCost']
            fundHoldCostItem = QTableWidgetItem("{}".format(format(fundHoldCost, '.4f')))
            self.positionTable.setItem(index, 2, fundHoldCostItem)

            # 4.持有份额
            fundHoldUnits = fundHold['fundUnits']
            fundHoldUnitsItem = QTableWidgetItem("{}".format(round(fundHoldUnits, 2)))
            self.positionTable.setItem(index, 3, fundHoldUnitsItem)

            # 5.持有金额
            fundHoldAmount = float(item['netWorth']) * fundHold['fundUnits']
            fundHoldAmountItem = QTableWidgetItem("{}".format(format(fundHoldAmount, '.2f')))
            self.positionTable.setItem(index, 4, fundHoldAmountItem)

            # 6.持有收益
            fundHoldIncome = (float(item['netWorth']) - fundHold['fundCost']) * fundHold['fundUnits']
            fundHoldIncomeItem = QTableWidgetItem("{}".format(round(fundHoldIncome, 2)))
            self.positionTable.setItem(index, 5, fundHoldIncomeItem)

            # 7.持有收益率
            fundHoldIncomeRate = (float(item['netWorth']) - fundHold['fundCost']) / fundHold['fundCost']
            fundHoldIncomeRate = 0 if fundHold['fundUnits'] <= float(0) else fundHoldIncomeRate
            fundHoldIncomeRateItem = QTableWidgetItem("{}%".format(round(fundHoldIncomeRate * 100, 2)))
            self.positionTable.setItem(index, 6, fundHoldIncomeRateItem)
            expectGrowthColor = RED if fundHoldIncomeRate >= 0 else GREEN
            self.positionTable.item(index, 6).setForeground(expectGrowthColor)

            # 8.基金净值
            netWorth = format(item['netWorth'], '.4f')
            # 净值变化率
            dayGrowth = format(float(item['dayGrowth']), '.2f')
            isDayGrowthUpDown = float(dayGrowth) > 0
            prefix = "+" if isDayGrowthUpDown else ""
            dayGrowth = prefix + dayGrowth + "%"
            dayGrowthItem = QTableWidgetItem("{} ({})".format(netWorth, dayGrowth))
            self.positionTable.setItem(index, 7, dayGrowthItem)
            dayGrowthColor = RED if isDayGrowthUpDown > 0 else GREEN
            self.positionTable.item(index, 7).setForeground(dayGrowthColor)

            # 9.估算净值
            expectWorth = float(item['expectWorth'])
            isExpectGrowthUpDown = float(item['expectGrowth']) > 0
            expectWorthColor = RED if isExpectGrowthUpDown > 0 else GREEN
            expectWorthItem = QTableWidgetItem("{}".format(format(expectWorth, '.4f')))
            self.positionTable.setItem(index, 8, expectWorthItem)
            self.positionTable.item(index, 8).setForeground(expectWorthColor)

            # 10.估值变化率
            expectGrowth = format(float(item['expectGrowth']), '.2f')
            isExpectGrowthUpDown = float(expectGrowth) > 0
            prefix = "+" if isExpectGrowthUpDown else ""
            expectGrowth = prefix + expectGrowth + "%"
            expectGrowthItem = QTableWidgetItem(expectGrowth)
            self.positionTable.setItem(index, 9, expectGrowthItem)
            expectGrowthColor = RED if isExpectGrowthUpDown > 0 else GREEN
            self.positionTable.item(index, 9).setForeground(expectGrowthColor)

            # 11.预估收益
            netWorthFloat = float(netWorth)
            expectWorthFloat = float(item['expectWorth'])
            expectIncome = (expectWorthFloat - netWorthFloat) * fundHoldUnits
            todayExpectIncome = todayExpectIncome + expectIncome
            prefix = '+' if expectIncome > 0 else ''
            expectIncomeItem = QTableWidgetItem('{}{}'.format(prefix, round(expectIncome, 2)))
            self.positionTable.setItem(index, 10, expectIncomeItem)
            expectIncomeColor = RED if expectIncome > 0 else GREEN
            self.positionTable.item(index, 10).setForeground(expectIncomeColor)

            totalIncome = totalIncome + (netWorthFloat - fundHold['fundCost']) * fundHold['fundUnits']
            holdAmount = holdAmount + fundHold['fundCost'] * fundHold['fundUnits']

        self.worthDateTxt.setText(worthDate)

        # 计算今日收益
        incomeTxt = '预估收益：{}'.format(round(todayExpectIncome, 2))
        incomeTxtColor = STYLE_RED if todayExpectIncome > 0 else STYLE_GREEN
        self.incomeTxt.setText(incomeTxt)
        self.incomeTxt.setStyleSheet(self.incomeTxt.styleSheet() + incomeTxtColor)

        # 计算总收益
        totalIncomeTxt = '持有收益：{}'.format(round(totalIncome, 2))
        totalIncomeTxtColor = STYLE_RED if totalIncome > 0 else STYLE_GREEN
        self.holdIncomeTxt.setText(totalIncomeTxt)
        self.holdIncomeTxt.setStyleSheet(self.holdIncomeTxt.styleSheet() + totalIncomeTxtColor)

        # 计算总金额
        holdAmountTxt = '持有金额：{}'.format(round(holdAmount + totalIncome, 2))
        # totalIncomeTxtColor = STYLE_RED if totalIncome > 0 else STYLE_GREEN
        self.holdAmount.setText(holdAmountTxt)
        # self.holdIncomeTxt.setStyleSheet(self.holdIncomeTxt.styleSheet() + totalIncomeTxtColor)

    def fund_add_edit_clicked(self, isAddFlag):
        title = '新增基金' if isAddFlag else "编辑基金"
        dialog = QDialog(self.centralwidget)
        ui = Ui_AddFundDialog()
        ui.setupUi(dialog)
        if not isAddFlag:
            selectedItem = self.positionTable.selectedItems()
            if len(selectedItem) == 0: return
            ui.fundCode.setText(selectedItem[1].text())
            ui.fundCost.setText(selectedItem[2].text())
            ui.fundUnits.setText(selectedItem[3].text())
            ui.fundCode.setEnabled(False)
            title = title + '：' + selectedItem[0].text()

        dialog.accepted.connect(
            lambda: self.edit_fund_data(ui.fundCode.text(), ui.fundCost.text(), ui.fundUnits.text()))

        dialog.setWindowTitle(title)
        dialog.exec_()

    def edit_fund_data(self, fundCode, fundCost, fundUnits):
        print(fundCode, fundCost, fundUnits)
        self.positionFund[fundCode] = {
            "fundCode": fundCode,
            "fundCost": float(fundCost),
            "fundUnits": float(fundUnits)
        }
        # self.fundConfigOrigin[]
        self.refresh_position_data()

    def read_local_config(self):
        with open('fund.json', 'r', encoding='utf-8') as f:
            # temp = f.read()
            self.fundConfigOrigin = json.load(f)

    def parse_fund_config(self):
        positions = self.fundConfigOrigin['positions']
        totalPositionAmount = 0
        for item in positions:
            self.positionFund[item['fundCode']] = item
            totalPositionAmount = totalPositionAmount + item['fundCost'] * item['fundUnits']
        print(totalPositionAmount)
