import _thread
import json
import os, requests
import sys
import time

from PyQt5.QtCore import Qt, pyqtSignal, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QMenu

from src.fundConfig import FundConfig
from src.fundEnum import DBSource
from ui.fundChartMain import FundChartMain
from ui.fundSettingDialog import Ui_FundSettingDialog
from src.myThread import MyThread
from ui.addFundDialog import Ui_AddFundDialog
from ui.fundViewForm import Ui_MainWindow
from ui.fundImageDialog import Ui_FundImageDialog
from ui.fundTableMain import FundTableMain
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

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_slot()
        self.fundCrawler = FundCrawler()
        self.positionModel = QStandardItemModel(0, 11)
        self.fundConfigOrigin = {}
        self.positionFund = {}
        self.optionalFund = []
        self.spaceKeyTimes = 0
        self.start_init()

        self.tabWidget.setCurrentIndex(0)

    def start_init(self):
        self.read_local_config()
        self.parse_fund_config()
        self.init_position_table()
        self.init_optional_table()

        print("界面初始化完成")
        self.thread = MyThread(self.positionFund, self.optionalFund)
        self.thread.start()
        self.thread.BDone.connect(self.refresh_board_data)
        self.thread.PDone.connect(self.refresh_position_data)
        self.thread.ODone.connect(self.refresh_optional_data)

    def init_slot(self):
        self.positionRefreshBtn.clicked.connect(lambda: self.refresh_btn_clicked(False))
        self.addFundBtn.clicked.connect(lambda: self.fund_add_edit_clicked(True))
        self.editFundBtn.clicked.connect(lambda: self.fund_add_edit_clicked(False))
        self.optionalRefreshBtn.clicked.connect(lambda: self.refresh_btn_clicked(True))
        self.addOptionalFundBtn.clicked.connect(self.optional_add_fund_clicked)
        self.positionTable.doubleClicked.connect(self.fund_double_clicked)
        self.settingBtn.clicked.connect(self.setting_btn_clicked)
        self.dbSourceCob.currentIndexChanged.connect(self.dbSource_changed)

    def dbSource_changed(self, index):
        if index == 0:
            FundConfig.DB_SWITCH = DBSource.YDI
        elif index == 1:
            FundConfig.DB_SWITCH = DBSource.TTT
        elif index == 2:
            FundConfig.DB_SWITCH = DBSource.OTH
        print('当前数据源：{}'.format(FundConfig.DB_SWITCH))

    def refresh_btn_clicked(self, isOptional: bool = False):
        print('refresh_btn_click')
        if not isOptional:
            self.positionRefreshBtn.setDisabled(True)
            self.addFundBtn.setDisabled(True)
            self.editFundBtn.setDisabled(True)
            _thread.start_new_thread(lambda: self.refresh_data(False), ())
        else:
            self.optionalRefreshBtn.setDisabled(True)
            self.optionalFundCodeTxt.setDisabled(True)
            self.addOptionalFundBtn.setDisabled(True)
            _thread.start_new_thread(lambda: self.refresh_data(True), ())

    def refresh_data(self, isOptional: bool = False):
        if not isOptional:
            self.refresh_board_data()
            self.refresh_position_data()
            self.positionRefreshBtn.setEnabled(True)
            self.addFundBtn.setEnabled(True)
            self.editFundBtn.setEnabled(True)
        else:
            self.refresh_board_data()
            self.refresh_optional_data()
            self.optionalRefreshBtn.setEnabled(True)
            self.optionalFundCodeTxt.setEnabled(True)
            self.addOptionalFundBtn.setEnabled(True)

    def init_position_table(self):
        """
        初始化持仓表头
        :return:
        """
        self.positionTable.clearContents()
        # 设置一共10列
        self.positionTable.setColumnCount(11)
        #  设置水平方向两个头标签文本内容
        self.positionTable.setHorizontalHeaderLabels(
            ['基金名称', '基金编码', '持仓成本', '持有份额', '持有金额', '持有收益', '持有收益率', '单位净值', '估算净值', '估值浮动', '预估收益'])
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.positionTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.positionTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # self.positionTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:#f5f5f5;}")
        # 设置整行选中
        self.positionTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.positionTable.verticalHeader().hide()

        # 设置行高
        self.positionTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 调整第 1-3列的宽度 为适应内容
        self.positionTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 允许弹出菜单
        self.positionTable.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        self.positionTable.customContextMenuRequested.connect(self.fund_table_menu)

    def init_optional_table(self):
        self.optionalTable.clearContents()
        # 设置一共10列
        self.optionalTable.setColumnCount(10)
        #  设置水平方向两个头标签文本内容
        self.optionalTable.setHorizontalHeaderLabels(
            ['基金名称', '基金编码', '估值', '净值', '近1周', '近1月', '近3月', '近6月', '近1年', '更新时间'])
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.optionalTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.optionalTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 设置整行选中
        self.optionalTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.optionalTable.verticalHeader().hide()

        # 设置行高
        self.optionalTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 调整第 1-3列的宽度 为适应内容
        self.optionalTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.optionalTable.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 允许弹出菜单
        self.optionalTable.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        self.optionalTable.customContextMenuRequested.connect(self.fund_table_menu)

    def fund_table_menu(self, pos):
        curTabIndex = self.tabWidget.currentIndex()

        contextMenu = QMenu(self.positionTable)
        menu1 = contextMenu.addAction('历史净值')
        menu2 = contextMenu.addAction('基金持仓')
        menu3 = contextMenu.addAction('净值图')
        menu4 = contextMenu.addAction('估值图')
        menu5 = contextMenu.addAction('删除')

        if curTabIndex == 0:
            screenPos = self.positionTable.mapToGlobal(pos)
        else:
            screenPos = self.optionalTable.mapToGlobal(pos)

        action = contextMenu.exec_(screenPos)

        if curTabIndex == 0:
            selectedItem = self.positionTable.selectedItems()
        else:
            selectedItem = self.optionalTable.selectedItems()

        if len(selectedItem) == 0: return
        fundCode = selectedItem[1].text()
        if action == menu1:
            title = '历史净值：' + selectedItem[0].text()
            dialog = QDialog(self.centralwidget)
            FundTableMain(dialog, fundCode, 1)
            dialog.setWindowTitle(title)
            dialog.exec_()
        elif action == menu2:
            title = '基金持仓：' + selectedItem[0].text()
            dialog = QDialog(self.centralwidget)
            FundTableMain(dialog, fundCode, 2)
            dialog.setWindowTitle(title)
            dialog.exec_()
        elif action == menu3:
            url = "http://j3.dfcfw.com/images/JJJZ1/{}.png".format(fundCode)
            title = '净值图：' + selectedItem[0].text()
            self.show_net_image(title, url)
        elif action == menu4:
            url = "http://j4.dfcfw.com/charts/pic6/{}.png".format(fundCode)
            title = '估值图：' + selectedItem[0].text()
            self.show_net_image(title, url)
        elif action == menu5:
            if curTabIndex == 0:
                selectedIndex = self.positionTable.selectedIndexes()[0].row()
                self.positionTable.removeRow(selectedIndex)
                self.positionFund.pop(fundCode)
                self.write_local_config(fundCode, isDelete=True)

            else:
                selectedIndex = self.optionalTable.selectedIndexes()[0].row()
                self.optionalTable.removeRow(selectedIndex)
                self.optionalFund.remove(fundCode)
                self.write_local_config(fundCode, isDelete=True, isOptional=True)

    def show_net_image(self, title, url):
        res = requests.get(url)
        img = QImage.fromData(res.content)
        dialog = QDialog(self.centralwidget)
        ui = Ui_FundImageDialog()
        ui.setupUi(dialog)
        ui.imageLabel.setPixmap(QPixmap.fromImage(img))
        dialog.setWindowTitle(title)
        dialog.exec_()

    def refresh_board_data(self, ret: list = None):
        print(ret)
        if ret is None:
            ret = self.fundCrawler.get_board_info()
        for board_item in ret:
            # fund_name = board_item["name"]
            fund_code = board_item["code"]
            priceChange = board_item["priceChange"]
            # 上涨还是下跌
            isRaiseFall = float(priceChange) > 0
            price = board_item["price"]
            priceChange = "+{}".format(priceChange) if isRaiseFall else "{}".format(priceChange)
            changePercent = board_item["changePercent"]
            changePercent = "+{}".format(changePercent) if isRaiseFall > 0 else "{}".format(changePercent)
            changePercent = changePercent + " %"
            colorString = RED_STR if isRaiseFall else GREEN_STR
            # 变色
            price = colorString.format(price)
            priceChange = colorString.format(priceChange)
            changePercent = colorString.format(changePercent)
            # 上证指数
            if fund_code == "000001":
                self.SHZ_Price.setText(price)
                self.SHZ_PriceChange.setText(priceChange)
                self.SHZ_ChangePercent.setText(changePercent)
            # 深证成指
            elif fund_code == "399001":
                self.SZZ_Price.setText(price)
                self.SZZ_PriceChange.setText(priceChange)
                self.SZZ_ChangePercent.setText(changePercent)
            # 创业板指
            elif fund_code == "399006":
                self.CY_Price.setText(price)
                self.CY_PriceChange.setText(priceChange)
                self.CY_ChangePercent.setText(changePercent)
            # 沪深300
            elif fund_code == "399300" or fund_code == '000300':
                self.HS_Price.setText(price)
                self.HS_PriceChange.setText(priceChange)
                self.HS_ChangePercent.setText(changePercent)
            # 上证50
            elif fund_code == "000016":
                self.SZ_Price.setText(price)
                self.SZ_PriceChange.setText(priceChange)
                self.SZ_ChangePercent.setText(changePercent)

    def refresh_position_data(self, ret: list = None):
        """
        刷新持仓基金数据
        :param ret: 手动出入的数据
        :return:
        """
        if ret is None:
            keys = []
            for key in self.positionFund:
                keys.append(key)
            ret = self.fundCrawler.get_funds_data(keys)
        # self.positionTable.clearContents()
        self.positionTable.setRowCount(len(ret))
        todayExpectIncome = 0
        totalIncome = 0
        holdAmount = 0
        worthDate = ''
        expectWorthDate = ''
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
            if fundHold['fundCost'] != float(0):
                fundHoldIncomeRate = (float(item['netWorth']) - fundHold['fundCost']) / fundHold['fundCost']
                fundHoldIncomeRate = 0 if fundHold['fundUnits'] <= float(0) else fundHoldIncomeRate
            else:
                fundHoldIncomeRate = 0
            fundHoldIncomeRateItem = QTableWidgetItem("{}%".format(round(fundHoldIncomeRate * 100, 2)))
            self.positionTable.setItem(index, 6, fundHoldIncomeRateItem)
            expectGrowthColor = RED if fundHoldIncomeRate >= 0 else GREEN
            self.positionTable.item(index, 6).setForeground(expectGrowthColor)

            # 8.基金净值
            netWorth = format(float(item['netWorth']), '.4f')
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
            checkTip = ''
            netWorthFloat = float(netWorth)
            # 当日净值已更新
            if item['netWorthDate'] == item['expectWorthDate'][0:10]:
                lastDayNetWorth = self.fundCrawler.get_day_worth(fundCode)['netWorth']
                lastDayNetWorthFloat = float(lastDayNetWorth)
                expectIncome = (netWorthFloat - lastDayNetWorthFloat) * fundHoldUnits
                checkTip = '√'  # 已结算标记
            else:
                expectWorthFloat = float(item['expectWorth'])
                expectIncome = (expectWorthFloat - netWorthFloat) * fundHoldUnits

            todayExpectIncome = todayExpectIncome + expectIncome
            prefix = '+' if expectIncome > 0 else ''
            expectIncomeItem = QTableWidgetItem('{} {}{}'.format(checkTip, prefix, round(expectIncome, 2)))
            self.positionTable.setItem(index, 10, expectIncomeItem)
            expectIncomeColor = RED if expectIncome > 0 else GREEN
            self.positionTable.item(index, 10).setForeground(expectIncomeColor)

            totalIncome = totalIncome + (netWorthFloat - fundHold['fundCost']) * fundHold['fundUnits']
            holdAmount = holdAmount + fundHold['fundCost'] * fundHold['fundUnits']

        self.positionTable.update()

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

    def refresh_optional_data(self, ret: list = None):
        """
        刷新自选基金数据
        :param ret: 手动传入数据
        :return:
        """
        if ret is None:
            ret = self.fundCrawler.get_funds_data(self.optionalFund, isOptional=True)
        self.optionalTable.clearContents()
        self.optionalTable.setRowCount(len(ret))

        for index, item in enumerate(ret):
            print(index, item)
            fundCode = item['code']

            # 1.基金名称
            fundNameItem = QTableWidgetItem(item['name'])
            self.optionalTable.setItem(index, 0, fundNameItem)

            # 2.基金代码
            fundCodeItem = QTableWidgetItem(item['code'])
            self.optionalTable.setItem(index, 1, fundCodeItem)

            # 3.基金估值
            fundExpectWorth = float(item['expectWorth'])
            fundExpectGrowth = float(item['expectGrowth'])
            fundExpectWorthColor = RED if fundExpectGrowth >= 0 else GREEN
            fundExpectWorthItem = QTableWidgetItem(
                "{} ({}%)".format(format(fundExpectWorth, '.4f'), format(fundExpectGrowth, '.2f')))
            self.optionalTable.setItem(index, 2, fundExpectWorthItem)
            self.optionalTable.item(index, 2).setForeground(fundExpectWorthColor)

            # 4.基金净值
            fundNetWorth = float(item['netWorth'])
            fundDayGrowth = float(item['dayGrowth'])
            fundNetWorthColor = RED if fundDayGrowth >= 0 else GREEN
            fundNetWorthItem = QTableWidgetItem(
                "{} ({}%)".format(format(fundNetWorth, '.4f'), format(fundDayGrowth, '.2f')))
            self.optionalTable.setItem(index, 3, fundNetWorthItem)
            self.optionalTable.item(index, 3).setForeground(fundNetWorthColor)

            # 5.近1周
            if 'lastWeekGrowth' in item and item['lastWeekGrowth'] != '---':
                lastWeekGrowth = float(item['lastWeekGrowth'])
                lastWeekGrowthColor = RED if lastWeekGrowth >= 0 else GREEN
                lastWeekGrowthItem = QTableWidgetItem("{}%".format(format(lastWeekGrowth, '.2f')))
                self.optionalTable.setItem(index, 4, lastWeekGrowthItem)
                self.optionalTable.item(index, 4).setForeground(lastWeekGrowthColor)
            else:
                self.optionalTable.setItem(index, 4, QTableWidgetItem("-"))

            #  6.近1月

            if 'lastMonthGrowth' in item and item['lastMonthGrowth'] != '---':
                lastMonthGrowth = float(item['lastMonthGrowth'])
                lastMonthGrowthColor = RED if lastMonthGrowth >= 0 else GREEN
                lastMonthGrowthItem = QTableWidgetItem("{}%".format(format(lastMonthGrowth, '.2f')))
                self.optionalTable.setItem(index, 5, lastMonthGrowthItem)
                self.optionalTable.item(index, 5).setForeground(lastMonthGrowthColor)
            else:
                self.optionalTable.setItem(index, 5, QTableWidgetItem("-"))

            #  7.近3月
            if 'lastThreeMonthsGrowth' in item and item['lastThreeMonthsGrowth'] != '---':
                lastThreeMonthsGrowth = float(item['lastThreeMonthsGrowth'])
                lastThreeMonthsGrowthColor = RED if lastThreeMonthsGrowth >= 0 else GREEN
                lastThreeMonthsGrowthItem = QTableWidgetItem("{}%".format(format(lastThreeMonthsGrowth, '.2f')))
                self.optionalTable.setItem(index, 6, lastThreeMonthsGrowthItem)
                self.optionalTable.item(index, 6).setForeground(lastThreeMonthsGrowthColor)
            else:
                self.optionalTable.setItem(index, 6, QTableWidgetItem("-"))

            #  8.近6月
            if 'lastSixMonthsGrowth' in item and item['lastSixMonthsGrowth'] != '---':
                lastSixMonthsGrowth = float(item['lastSixMonthsGrowth'])
                lastSixMonthsGrowthColor = RED if lastSixMonthsGrowth >= 0 else GREEN
                lastSixMonthsGrowthItem = QTableWidgetItem("{}%".format(format(lastSixMonthsGrowth, '.2f')))
                self.optionalTable.setItem(index, 7, lastSixMonthsGrowthItem)
                self.optionalTable.item(index, 7).setForeground(lastSixMonthsGrowthColor)
            else:
                self.optionalTable.setItem(index, 7, QTableWidgetItem("-"))

            #  9.近1年
            if 'lastYearGrowth' in item and item['lastYearGrowth'] != '---':
                lastYearGrowth = float(item['lastYearGrowth'])
                lastYearGrowthColor = RED if lastYearGrowth >= 0 else GREEN
                lastYearGrowthItem = QTableWidgetItem("{}%".format(format(lastYearGrowth, '.2f')))
                self.optionalTable.setItem(index, 8, lastYearGrowthItem)
                self.optionalTable.item(index, 8).setForeground(lastYearGrowthColor)
            else:
                self.optionalTable.setItem(index, 8, QTableWidgetItem("-"))

            #  10.更新时间
            if 'expectWorthDate' in item:
                expectWorthDateItem = QTableWidgetItem("{}".format(item['expectWorthDate']))
                self.optionalTable.setItem(index, 9, expectWorthDateItem)
            else:
                self.optionalTable.setItem(index, 9, QTableWidgetItem("-"))

        self.optionalTable.update()

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

    def optional_add_fund_clicked(self):
        fundCode = self.optionalFundCodeTxt.text()
        if fundCode == '' or len(fundCode) != 6 or fundCode is None: return
        self.optionalFundCodeTxt.setText("")

        if fundCode in self.optionalFund:
            index = self.optionalFund.index(fundCode)
            # self.optionalTable.row(index).
            # self.optionalTable.scrollTo()
            # self.optionalTable.findItems(fundCode)
            return

        self.optionalFund.append(fundCode)
        self.refresh_optional_data()
        self.optionalTable.scrollToBottom()

    def edit_fund_data(self, fundCode, fundCost, fundUnits):
        """
        修改持仓基金
        :param fundCode: 基金代码
        :param fundCost: 基金成本
        :param fundUnits: 持有份额
        :return:
        """
        print(fundCode, fundCost, fundUnits)
        print(fundCode, type(fundCost), type(fundUnits))

        if fundCost is None or fundCost == '':
            fundCost = 0
        if fundUnits is None or fundUnits == '':
            fundUnits = 0

        self.positionFund[fundCode] = {
            "fundCode": fundCode,
            "fundCost": float(fundCost),
            "fundUnits": float(fundUnits)
        }
        # self.fundConfigOrigin[]
        self.refresh_position_data()
        self.write_local_config(fundCode, float(fundCost), float(fundUnits))

    def fund_double_clicked(self, index: QModelIndex):
        rowIndex = index.row()
        fundCode = self.positionTable.item(rowIndex, 1).text()
        fundName = self.positionTable.item(rowIndex, 0).text()
        title = "业绩走势：{}".format(fundName)
        dialog = QDialog(self.centralwidget)
        windowsFlags = dialog.windowFlags()
        windowsFlags |= Qt.WindowMaximizeButtonHint
        dialog.setWindowFlags(windowsFlags)
        FundChartMain(dialog, fundCode, 1)
        dialog.setWindowTitle(title)
        dialog.exec_()

    def setting_btn_clicked(self):
        dialog = QDialog(self.centralwidget)
        ui = Ui_FundSettingDialog()
        ui.setupUi(dialog)
        dialog.setWindowTitle("程序设置")
        dialog.exec_()

    def read_local_config(self):
        """
        读取本地配置文件
        :return: void
        """
        try:
            with open('fund.json', 'r', encoding='utf-8') as f:
                self.fundConfigOrigin = json.load(f)
        except:
            with open('fund.json', 'w', encoding='utf-8') as f:
                config = {
                    'positions': [
                        {
                            'fundCode': '260108',
                            'fundCost': 1.000,
                            'fundUnits': 500.00
                        }
                    ],
                    'optional': ['260108']
                }
                self.fundConfigOrigin = config
                json.dump(config, f, indent=4, ensure_ascii=False)

    def write_local_config(self, fundCode: str, fundCost: float = 0, fundUnits: float = 0, isDelete: bool = False,
                           isOptional: bool = False):
        """
        写入本地配置文件
        :param fundCode: 基金代码
        :param fundCost: 持有成本
        :param fundUnits: 持有份额
        :param isDelete: 是否删除
        :param isOptional: 是否自选
        :return:
        """
        try:
            # 删除持仓
            if isDelete and not isOptional:
                for index, item in enumerate(self.fundConfigOrigin['positions']):
                    if item['fundCode'] == fundCode:
                        self.fundConfigOrigin['positions'].remove(item)
                        break
            # 删除自选
            elif isDelete and isOptional:
                if fundCode in self.fundConfigOrigin['optional']:
                    self.fundConfigOrigin['optional'].remove(fundCode)
            # 修改持仓
            elif not isDelete and not isOptional:
                modifyIndex = -1
                fund = {
                    'fundCode': fundCode,
                    'fundCost': fundCost,
                    'fundUnits': fundUnits
                }
                for index, item in enumerate(self.fundConfigOrigin['positions']):
                    if item['fundCode'] == fundCode:
                        modifyIndex = index
                        self.fundConfigOrigin['positions'].remove(item)
                        break
                if modifyIndex >= 0:
                    self.fundConfigOrigin['positions'].insert(modifyIndex, fund)
                else:
                    self.fundConfigOrigin['positions'].append(fund)
            # 修改自选
            elif not isDelete and isOptional:
                if fundCode not in self.fundConfigOrigin['optional']:
                    self.fundConfigOrigin['optional'].append(fundCode)
                else:
                    pass
            with open('fund.json', 'w', encoding='utf-8') as f:
                json.dump(self.fundConfigOrigin, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

    def parse_fund_config(self):
        """
        解析配置文件
        :return:
        """
        # 持仓基金
        if "positions" in self.fundConfigOrigin:
            positions = self.fundConfigOrigin['positions']
            for item in positions:
                self.positionFund[item['fundCode']] = item
        else:
            self.positionFund = {}
        # 自选基金
        if "optional" in self.fundConfigOrigin:
            self.optionalFund = self.fundConfigOrigin['optional']
        else:
            self.optionalFund = []

        # 检测键盘回车按键

    def keyPressEvent(self, event):
        print("按下：" + str(event.key()))
        curTabIndex = self.tabWidget.currentIndex()
        # 刷新按钮按下
        if event.key() == Qt.Key_F5:
            if curTabIndex == 0:
                self.refresh_btn_clicked(False)
            elif curTabIndex == 1:
                self.refresh_btn_clicked(True)

        # 回车按钮
        if event.key() == Qt.Key_Enter:
            if curTabIndex == 0:
                pass
            elif curTabIndex == 1:
                self.optional_add_fund_clicked()
