import _thread
import json
import os, requests
import sys
import uuid
from datetime import datetime
import time

from PyQt5.QtCore import Qt, QModelIndex, QTimer, QCoreApplication, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QImage, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView, QTableWidgetItem, QDialog, QMenu, \
    QApplication, QMessageBox, QCompleter, QSystemTrayIcon, QAction
from chinese_calendar import is_workday
from apscheduler.schedulers.background import BackgroundScheduler

from src.fund_update import FundUpdate
from src.fund_cloud_sync import CloudSync
from src.fund_config import FundConfig
from src.fund_enum import DBSource, ColorSwitch
from form.fund_chart_main import FundChartMain
from form.fund_setting_dialog import Ui_FundSettingDialog
from src.my_thread import MyThread
from form.fund_add_dialog import Ui_AddFundDialog
from form.fund_main_form import Ui_MainWindow
from form.fund_image_dialog import Ui_FundImageDialog
from form.fund_deal_dialog import Ui_FundDealDialog
from form.fund_browser_dialog import Ui_FundBrowser
from form.fund_table_main import FundTableMain
from src.fund_crawler import FundCrawler
from src.fund_utils import get_or_default, get_color, judge_time
from okex.okex_websocket import *
import okex.Account_api as Account
import okex.common_api as Common
import traceback
import asyncio


class FundMain(QMainWindow, Ui_MainWindow):
    scheduler = BackgroundScheduler()
    BoardChange = pyqtSignal(int, list)
    TableChange = pyqtSignal(list)
    api_key = "42adc4f1-3a4c-4cb4-b4b5-156051a77cab"
    secret_key = "69866D7C605424264AEC79428ED73D22"
    passphrase = "NBhgfIy324op9cvL"
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    # flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    url = 'wss://real.coinall.ltd:8443/ws/v3'
    channels = ["index/ticker:BTC-USDT", "index/ticker:ETH-USDT", "index/ticker:ADA-USDT",
                "index/ticker:XRP-USDT", "index/ticker:DOT-USDT"]
    loop = asyncio.new_event_loop()

    # account api
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    commonAPI = Common.CommonApi(api_key, secret_key, passphrase, False, flag)

    def __init__(self, parent: QApplication):
        super().__init__()
        sys.excepthook = self.except_hook
        self.setupUi(self)
        self.parentWindow = parent
        self.init_slot()
        self.fundCrawler = FundCrawler()
        self.positionModel = QStandardItemModel(0, 11)
        self.runDir = os.getcwd()
        self.fundConfigOrigin = {}
        self.positionFund = {}
        self.optionalFund = []
        self.allFund = []
        self.spaceKeyTimes = 0
        self.is_start_done = False
        self.trayIcon = QSystemTrayIcon(self)
        self.icon = QIcon(":/icon/new/windows/leekbox-icon-256.ico")
        self.all_fund_settled_cnt = 0
        self.completer = QCompleter([])
        self.tip_cnt = 0
        self.op_coin = []
        self.config_path = ''
        self.socket_running = True

        self.timer = QTimer()  # 初始化定时器
        self.timer.timeout.connect(self.timer_refresh)

        self.dbSourceCob.setFont(QFont(FundConfig.FONT_NAME, FundConfig.FONT_SIZE - 1))

        self.start_init()
        self.sync = CloudSync(self.config_path, FundConfig.FUND_MID)

        self.tabWidget.setCurrentIndex(0)

    def start_init(self):
        """
        初始化函数
        :return:
        """
        self.read_local_config()
        self.parse_fund_config()
        self.init_position_table()
        self.init_optional_table()
        self.init_coin_table()

        print("界面初始化完成")
        self.thread = MyThread(self.positionFund, self.optionalFund)
        self.thread.start()
        self.thread.BDone.connect(self.refresh_board_data)
        self.thread.PDone.connect(self.refresh_position_data)
        self.thread.ODone.connect(self.refresh_optional_data)

        self.thread.StartDone.connect(self.start_done)

    def init_tray_icon(self):
        """
        初始化系统状态栏
        :return:
        """
        about_action = QAction("关于程序", self)
        update_action = QAction("检查更新", self)
        open_action = QAction("显示窗口", self)
        quit_action = QAction("退出程序", self)

        tray_icon_menu = QMenu(self)
        tray_icon_menu.addAction(about_action)
        tray_icon_menu.addAction(update_action)
        tray_icon_menu.addSeparator()
        tray_icon_menu.addAction(open_action)
        tray_icon_menu.addAction(quit_action)

        quit_action.triggered.connect(QCoreApplication.quit)
        open_action.triggered.connect(self.showNormal)
        about_action.triggered.connect(self.show_about)
        update_action.triggered.connect(self.check_update)

        if FundConfig.PLATFORM == 'darwin':
            self.icon = QIcon(QPixmap(":/icon/white-icon/leekbox-white.png").scaled(16, 16))
        self.trayIcon.setIcon(self.icon)

        self.trayIcon.setToolTip("韭菜盒子")
        self.trayIcon.setContextMenu(tray_icon_menu)
        self.trayIcon.activated.connect(lambda reason: self.tray_icon_activated(reason))
        self.trayIcon.show()

    def show_about(self):
        self.showNormal()
        msg = QMessageBox(self)
        msg.setWindowTitle("关于程序")
        msg.setText("有了韭菜盒子从此不在做韭菜\t\n当前版本：{} \nCopyright © 2020-2021 colinxu".format(
            FundConfig.VERSION))
        msg.setIconPixmap(QPixmap(":/icon/new/windows/leekbox-icon-256.ico"))
        msg.addButton("确定", QMessageBox.ActionRole)
        msg.exec()

    def check_update(self):
        self.showNormal()
        res = FundUpdate(self).update(sys.argv)
        if res is not None:
            QMessageBox.information(self, '提示', '暂无更新，已是最新版本！\t')

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def start_done(self):
        if not self.is_start_done:
            self.is_start_done = True
            self.scheduler.add_job(self.scheduler_job, 'cron', hour='14', minute='50')
            self.scheduler.start()
            if FundConfig.AUTO_REFRESH_ENABLE:
                print('启动定时任务')
                self.timer.start(FundConfig.AUTO_REFRESH_TIMEOUT)
                self.init_tray_icon()
            try:
                # 设置自选基金自动补全
                self.completer = QCompleter(self.fundCrawler.get_all_fund())
                # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
                self.completer.setFilterMode(Qt.MatchContains)
                # 设置补全模式  有三种： QCompleter.PopupCompletion（默认）  QCompleter.InlineCompletion
                # QCompleter.UnfilteredPopupCompletion
                self.completer.setCompletionMode(QCompleter.PopupCompletion)
                self.optionalFundCodeTxt.setCompleter(self.completer)

                all_coin = self.commonAPI.get_all_coin()
                completer_list = []
                for coin_pair in all_coin['data']['list']:
                    completer_list.append('{}-USDT {}'.format(coin_pair['project'], coin_pair['fullName']))

                # 设置币对自动完成
                self.coin_pair_completer = QCompleter(completer_list)
                self.coin_pair_completer.setFilterMode(Qt.MatchContains)
                self.coin_pair_completer.setCompletionMode(QCompleter.PopupCompletion)
                self.coin_pair_completer.setCaseSensitivity(Qt.CaseInsensitive)
                self.coinPairText.setCompleter(self.coin_pair_completer)

                # 检查更新
                if FundConfig.PLATFORM == 'win32':
                    FundUpdate(self).update(sys.argv)
                else:
                    pass

            except Exception as e:
                print("设置自动补全失败：" + str(e))
            _thread.start_new_thread(self.start_websocket, ())
            # self.start_websocket()
        else:
            print("系统已经初始化完成")

    def start_websocket(self, restart: bool = False):
        if restart:
            self.socket_running = False
            while self.loop.is_running():
                print('等待结束')
            print('loop 已结束')
            self.loop.close()
            self.loop = asyncio.new_event_loop()
            self.socket_running = True
            self.channels = []
        self.op_coin = []
        for item in self.fundConfigOrigin['crypto-coin']:
            self.op_coin.append("spot/ticker:" + item)
        self.channels.extend(self.op_coin)
        # loop = asyncio.new_event_loop()
        # 公共数据 不需要登录（行情，K线，交易数据，资金费率，限价范围，深度数据，标记价格等频道）
        self.loop.run_until_complete(self.subscribe_without_login(self.url, self.channels))

    def scheduler_job(self):
        """
        定时任务
        :return:
        """
        self.trayIcon.showMessage(FundConfig.APP_NAME, '已经 14:50 了，快去加仓吧！', self.icon)

    def init_slot(self):
        """
        初始化槽函数
        :return:
        """
        self.positionRefreshBtn.clicked.connect(lambda: self.refresh_btn_clicked(False))
        self.addFundBtn.clicked.connect(lambda: self.fund_add_edit_clicked(True))
        self.editFundBtn.clicked.connect(lambda: self.fund_add_edit_clicked(False))
        self.optionalRefreshBtn.clicked.connect(lambda: self.refresh_btn_clicked(True))
        self.addOptionalFundBtn.clicked.connect(self.optional_add_fund_clicked)
        self.positionTable.doubleClicked.connect(self.fund_double_clicked)
        self.optionalTable.doubleClicked.connect(self.fund_double_clicked)
        # self.settingBtn.clicked.connect(self.setting_btn_clicked)
        self.dbSourceCob.currentIndexChanged.connect(self.db_source_changed)
        self.settingLabel.clicked.connect(self.setting_btn_clicked)
        self.tabWidget.currentChanged.connect(self.tab_widget_changed)
        self.BoardChange.connect(self.change_board_text)
        self.TableChange.connect(self.change_table_coneten)
        self.total_assets_txt.clicked.connect(self.balance_click)
        self.coinMarketTable.doubleClicked.connect(self.coin_double_clicked)
        self.addCoinPairBtn.clicked.connect(self.add_coin_btn_clicked)

    def balance_click(self):
        res = self.accountAPI.get_account()
        balance = float(res['data'][0]['totalEq'])
        balance_str = '{} USD'.format(format(balance, '.2f'))
        self.total_assets_txt.setText(balance_str)

    def tab_widget_changed(self, index):
        if index == 2:
            self.headLabelOne.setText('BTC / USDT')
            self.headLabelTwo.setText('ETH / USDT')
            self.headLabelThree.setText('ADA / USDT')
            self.headLabelFour.setText('XRP / USDT')
            self.headLabelFive.setText('DOT / USDT')
            self.SHZ_Price.setText('-')
            self.SHZ_PriceChange.setText('-')
            self.SHZ_ChangePercent.setText('-')
            # 深证成指
            self.SZZ_Price.setText('-')
            self.SZZ_PriceChange.setText('-')
            self.SZZ_ChangePercent.setText('-')
            # 创业板指
            self.CY_Price.setText('-')
            self.CY_PriceChange.setText('-')
            self.CY_ChangePercent.setText('-')
            # 沪深300
            self.HS_Price.setText('-')
            self.HS_PriceChange.setText('-')
            self.HS_ChangePercent.setText('-')
            # 上证50
            self.SZ_Price.setText('-')
            self.SZ_PriceChange.setText('-')
            self.SZ_ChangePercent.setText('-')

            self.balance_click()

        else:
            self.headLabelOne.setText('上证指数（ 000001 ）')
            self.headLabelTwo.setText('深证成指（ 399001 ）')
            self.headLabelThree.setText('创业板指（ 399006 ）')
            self.headLabelFour.setText('沪深300（ 000300 ）')
            self.headLabelFive.setText('上证50（ 000016 ）')
            self.refresh_board_data()

    def db_source_changed(self, index):
        if not self.is_start_done: return
        FundConfig.DB_SWITCH = DBSource(index)
        self.fundConfigOrigin['source'] = index
        self.write_local_config()
        self.refresh_btn_clicked()

    def timer_refresh(self):
        if not FundConfig.AUTO_REFRESH_ENABLE: return
        # 交易日15:30后自动关闭定时刷新
        nowTime = datetime.now()
        print(nowTime)
        if is_workday(nowTime) and judge_time('09:20:00') and not judge_time('15:20:00'):
            print('timer_refresh')
            if self.tabWidget.currentIndex() == 0:
                self.positionRefreshBtn.setText('自动刷新...')
                self.refresh_btn_clicked()
            elif self.tabWidget.currentIndex() == 1:
                self.optionalRefreshBtn.setText('自动刷新...')
                self.refresh_btn_clicked(True)
        else:
            print('timer_refresh passed')

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
            self.positionRefreshBtn.setText('刷新')
        else:
            self.refresh_board_data()
            self.refresh_optional_data()
            self.optionalRefreshBtn.setEnabled(True)
            self.optionalFundCodeTxt.setEnabled(True)
            self.addOptionalFundBtn.setEnabled(True)
            self.optionalRefreshBtn.setText('刷新')

    def init_position_table(self):
        """
        初始化持仓表头
        :return:
        """
        self.positionTable.clearContents()
        # 设置一共10列
        self.positionTable.setColumnCount(12)
        #  设置水平方向两个头标签文本内容
        self.positionTable.setHorizontalHeaderLabels(
            ['基金名称', '基金编码', '持仓成本', '持有份额', '持有金额', '持有收益', '持有收益率', '单位净值', '净值估算', '估值涨幅', '估值时间', '预估收益'])
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
        self.positionTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.positionTable.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.positionTable.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents)

        # 允许弹出菜单
        self.positionTable.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        self.positionTable.customContextMenuRequested.connect(self.fund_table_menu)

        # 关闭排序功能
        self.positionTable.setSortingEnabled(False)

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
        self.optionalTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.optionalTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.optionalTable.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 允许弹出菜单
        self.optionalTable.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        self.optionalTable.customContextMenuRequested.connect(self.fund_table_menu)

    def init_coin_table(self):
        self.coinMarketTable.clearContents()
        # 设置一共10列
        self.coinMarketTable.setColumnCount(7)
        #  设置水平方向两个头标签文本内容
        self.coinMarketTable.setHorizontalHeaderLabels(
            ['名称', '最新价', '今日涨幅', '24H最低', '24H最高', '24H成交量', '24H成交额'])
        # 水平方向标签拓展剩下的窗口部分，填满表格
        # self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.coinMarketTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.coinMarketTable.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 设置整行选中
        self.coinMarketTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.coinMarketTable.verticalHeader().hide()

        # 设置行高
        self.coinMarketTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 设置颜色相间
        self.coinMarketTable.setAlternatingRowColors(True)
        self.coinMarketTable.horizontalHeader().setHighlightSections(False)

        # 调整第 1-3列的宽度 为适应内容
        # self.coinMarketTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.coinMarketTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # self.coinMarketTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        # self.coinMarketTable.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)
        # self.positionTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # 允许弹出菜单
        # self.coinMarketTable.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到槽（单击鼠标右键，就调用方法）
        # self.coinMarketTable.customContextMenuRequested.connect(self.fund_table_menu)

    def fund_table_menu(self, pos):
        curTabIndex = self.tabWidget.currentIndex()

        contextMenu = QMenu(self.positionTable)
        menu1 = contextMenu.addAction('历史净值')
        menu2 = contextMenu.addAction('基金持仓')
        menu3 = contextMenu.addAction('净值图')
        menu4 = contextMenu.addAction('估值图')

        contextMenu.addSeparator()

        if curTabIndex == 0:
            # menu6 = contextMenu.addAction('加仓')
            # menu7 = contextMenu.addAction('减仓')
            screenPos = self.positionTable.mapToGlobal(pos)
        else:
            screenPos = self.optionalTable.mapToGlobal(pos)

        menu5 = contextMenu.addAction('删除')

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
        # elif action == menu6:
        #     title = '加仓：' + selectedItem[0].text()
        #     dialog = QDialog(self.centralwidget)
        #     form = Ui_FundDealDialog()
        #     form.setupUi(dialog)
        #
        #     form.saleUnitsLabel.setParent(None)
        #     form.saleUnitsTxt.setParent(None)
        #     form.allUnitsLabel.setParent(None)
        #     form.allUnitsTxt.setParent(None)
        #     form.saleRateLayout.setParent(None)
        #
        #     for i in range(form.saleRateLayout.count()):
        #         form.saleRateLayout.itemAt(i).widget().hide()
        #
        #     form.fundCodeTxt.setText(fundCode)
        #     form.fundCodeTxt.setEnabled(False)
        #     netWorth = selectedItem[7].text().split('(')[0]
        #     form.netWorthTxt.setText(netWorth)
        #
        #     fundInfo = self.fundCrawler.get_fund_info(fundCode)
        #     form.netWorthTxt.setText(fundInfo['DWJZ'])
        #     form.buyRateTxt.setText(fundInfo['RATE'])
        #
        #     dialog.accepted.connect(
        #         lambda: self.buy_sale_fund(fundCode, True,
        #                                    netWorth=form.netWorthTxt.text(),
        #                                    buyAmount=form.buyAmountTxt.text(),
        #                                    buyRate=form.buyRateTxt.text(),
        #                                    selectedItem=selectedItem))
        #     dialog.setFixedHeight(dialog.height() - 30 * 3 + 10)
        #     dialog.setWindowTitle(title)
        #     dialog.exec_()
        # elif action == menu7:
        #     title = '减仓：' + selectedItem[0].text()
        #     dialog = QDialog(self.centralwidget)
        #     form = Ui_FundDealDialog()
        #     form.setupUi(dialog)
        #
        #     form.netWorthLabel.setParent(None)
        #     form.netWorthTxt.setParent(None)
        #     form.buyRateLabel.setParent(None)
        #     form.buyRateTxt.setParent(None)
        #     form.buyAmountLabel.setParent(None)
        #     form.buyAmountTxt.setParent(None)
        #
        #     allUnits = selectedItem[3].text()
        #     form.fundCodeTxt.setText(fundCode)
        #     form.fundCodeTxt.setEnabled(False)
        #     form.allUnitsTxt.setText(allUnits)
        #     form.allUnitsTxt.setEnabled(False)
        #
        #     allUnitsFloat = float(allUnits)
        #
        #     form.rate20Btn.clicked.connect(lambda: form.saleUnitsTxt.setText(format(allUnitsFloat * 0.2, '.2f')))
        #     form.rate30Btn.clicked.connect(lambda: form.saleUnitsTxt.setText(format(allUnitsFloat * 0.3, '.2f')))
        #     form.rate50Btn.clicked.connect(lambda: form.saleUnitsTxt.setText(format(allUnitsFloat * 0.5, '.2f')))
        #     form.rate100Btn.clicked.connect(lambda: form.saleUnitsTxt.setText(format(allUnitsFloat, '.2f')))
        #
        #     dialog.setFixedHeight(dialog.height() - 30 * 3 + 10)
        #     dialog.setWindowTitle(title)
        #     dialog.exec_()

    def buy_sale_fund(self, fundCode: str, buyOrSale: bool, netWorth: str = None, buyAmount: str = None,
                      buyRate: str = None, allUnits: str = None, saleUnits: str = None, selectedItem: list = None):
        print(fundCode, netWorth, buyAmount, buyRate, allUnits, saleUnits)
        if buyOrSale:
            buyRate = float(buyRate.replace('%', '')) / 100
            buyAmount = float(buyAmount)
            buyAmount = buyAmount - buyAmount * buyRate
            buyUnits = buyAmount / float(netWorth)
            positionAmount = float(selectedItem[2].text()) * float(selectedItem[3].text())

            finalPositionAmount = positionAmount + buyAmount
            finalPositionUnits = float(selectedItem[3].text()) + buyUnits
            finalPositionCost = finalPositionAmount / finalPositionUnits
            print(finalPositionCost, finalPositionUnits)

    def show_net_image(self, title, url):
        session = requests.Session()
        session.trust_env = False
        res = session.get(url)
        img = QImage.fromData(res.content)
        dialog = QDialog(self.centralwidget)
        ui = Ui_FundImageDialog()
        ui.setupUi(dialog)
        ui.imageLabel.setPixmap(QPixmap.fromImage(img))
        dialog.setWindowTitle(title)
        dialog.exec_()

    def refresh_board_data(self, ret: list = None):
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
            colorString = get_color(float(priceChange), 'str')
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
        self.all_fund_settled_cnt = 0
        for index, item in enumerate(ret):
            print(index, item)
            fundCode = item['code']
            worthDate = item['expectWorthDate']

            fundHold = self.positionFund[fundCode]
            # 1.基金名称
            fundName = get_or_default(item['name'], '[未获取到名称]')
            # if len(fundName) > 10:
            #     fundName = fundName[:10] + '...'
            fundNameItem = QTableWidgetItem(fundName)

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

            netWorthValue = float(get_or_default(item['netWorth'], 1))
            # 5.持有金额
            fundHoldAmount = netWorthValue * fundHold['fundUnits']
            fundHoldAmountItem = QTableWidgetItem("{}".format(format(fundHoldAmount, '.2f')))
            self.positionTable.setItem(index, 4, fundHoldAmountItem)

            # 6.持有收益
            costAmount = round(fundHold['fundCost'] * fundHold['fundUnits'], 0)
            if costAmount % 5 == 0:
                fundHoldIncome = netWorthValue * fundHold['fundUnits'] \
                                 - costAmount
            else:
                fundHoldIncome = netWorthValue * fundHold['fundUnits'] \
                                 - fundHold['fundCost'] * fundHold['fundUnits']
            fundHoldIncomeItem = QTableWidgetItem("{}".format(round(fundHoldIncome, 2)))
            self.positionTable.setItem(index, 5, fundHoldIncomeItem)

            # fundHoldIncome = (float(item['netWorth']) - fundHold['fundCost']) * fundHold['fundUnits']
            # fundHoldIncomeItem = QTableWidgetItem("{}".format(round(fundHoldIncome, 2)))
            # self.positionTable.setItem(index, 5, fundHoldIncomeItem)

            # 7.持有收益率
            if fundHold['fundCost'] != float(0):
                fundHoldIncomeRate = (netWorthValue - fundHold['fundCost']) / fundHold['fundCost']
                fundHoldIncomeRate = 0 if fundHold['fundUnits'] <= float(0) else fundHoldIncomeRate
            else:
                fundHoldIncomeRate = 0
            fundHoldIncomeRateItem = QTableWidgetItem("{}%".format(round(fundHoldIncomeRate * 100, 2)))
            self.positionTable.setItem(index, 6, fundHoldIncomeRateItem)
            expectGrowthColor = get_color(fundHoldIncomeRate, 'brush')
            self.positionTable.item(index, 6).setForeground(expectGrowthColor)

            # 8.基金净值
            netWorth = format(netWorthValue, '.4f')
            dayGrowthFloat = get_or_default(item['dayGrowth'])
            # 净值变化率
            dayGrowth = format(float(dayGrowthFloat), '.2f')
            isDayGrowthUpDown = float(dayGrowth) > 0
            prefix = "+" if isDayGrowthUpDown else ""
            dayGrowth = prefix + dayGrowth + "%"
            dayGrowthItem = QTableWidgetItem("{} ({})".format(netWorth, dayGrowth))
            self.positionTable.setItem(index, 7, dayGrowthItem)
            dayGrowthColor = get_color(dayGrowthFloat, 'brush')
            self.positionTable.item(index, 7).setForeground(dayGrowthColor)

            # 9.估算净值
            expectWorth = float(get_or_default(item['expectWorth']))
            expectWorthColor = get_color(float(get_or_default(item['expectGrowth'])), 'brush')
            expectWorthItem = QTableWidgetItem("{}".format(format(expectWorth, '.4f')))
            self.positionTable.setItem(index, 8, expectWorthItem)
            self.positionTable.item(index, 8).setForeground(expectWorthColor)

            # 10.估值变化率
            expectGrowth = format(float(get_or_default(item['expectGrowth'])), '.2f')
            isExpectGrowthUpDown = float(expectGrowth) > 0
            prefix = "+" if isExpectGrowthUpDown else ""
            expectGrowth = prefix + expectGrowth + "%"
            expectGrowthItem = QTableWidgetItem(expectGrowth)
            self.positionTable.setItem(index, 9, expectGrowthItem)
            expectGrowthColor = get_color(float(get_or_default(item['expectGrowth'])), 'brush')
            self.positionTable.item(index, 9).setForeground(expectGrowthColor)

            # 预估时间
            expectWorthDate = item['expectWorthDate'][5:16] if '--' not in item['expectWorthDate'] else '--'
            expectWorthItem = QTableWidgetItem(expectWorthDate)
            self.positionTable.setItem(index, 10, expectWorthItem)

            # 11.预估收益
            checkTip = ''
            netWorthFloat = float(netWorth)
            # 当日净值已更新
            if get_or_default(item['expectWorthDate']) != '0' and item['netWorthDate'] == item['expectWorthDate'][:10]:
                lastDayTime = self.fundCrawler.get_last_trade_day(item['netWorthDate'])
                lastDayNetWorth = self.fundCrawler.get_day_worth(fundCode, lastDayTime)
                lastDayNetWorth = lastDayNetWorth['netWorth'] if lastDayNetWorth != 0 else 1
                lastDayNetWorthFloat = float(lastDayNetWorth)
                expectIncome = (netWorthFloat - lastDayNetWorthFloat) * fundHoldUnits
                checkTip = '√'  # 已结算标记
                self.all_fund_settled_cnt = self.all_fund_settled_cnt + 1
            else:
                expectWorthFloat = float(get_or_default(item['expectWorth']))
                expectIncome = (expectWorthFloat - netWorthFloat) * fundHoldUnits

            if '--' in item['expectWorthDate']:
                expectIncome = 0

            if len(expectWorthDate) <= 0:
                expectIncome = 0

            todayExpectIncome = todayExpectIncome + expectIncome
            prefix = '+' if expectIncome > 0 else ''
            expectIncomeItem = QTableWidgetItem('{} {}{}'.format(checkTip, prefix, round(expectIncome, 2)))
            self.positionTable.setItem(index, 11, expectIncomeItem)
            expectIncomeColor = get_color(expectIncome, 'brush')
            self.positionTable.item(index, 11).setForeground(expectIncomeColor)

            if '[' not in fundName:
                totalIncome = totalIncome + (netWorthFloat - fundHold['fundCost']) * fundHold['fundUnits']
                holdAmount = holdAmount + fundHold['fundCost'] * fundHold['fundUnits']

        # 刷新时间
        refreshTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.position_refresh_time_txt.setText(refreshTime)

        # 计算今日收益
        today_income_flag = '√' if self.all_fund_settled_cnt == len(ret) else ''
        incomeTxt = '预估收益：{} {}'.format(today_income_flag, round(todayExpectIncome, 2))
        incomeTxtColor = get_color(todayExpectIncome, 'style')
        self.incomeTxt.setText(incomeTxt)
        self.incomeTxt.setStyleSheet("margin-right:5px;" + incomeTxtColor)

        # 计算总收益
        totalIncomeTxt = '持有收益：{}'.format(round(totalIncome, 2))
        totalIncomeTxtColor = get_color(totalIncome, 'style')
        self.holdIncomeTxt.setText(totalIncomeTxt)
        self.holdIncomeTxt.setStyleSheet("margin-right:5px;" + totalIncomeTxtColor)

        # 计算总金额
        holdAmountTxt = '持有金额：{}'.format(round(holdAmount + totalIncome, 2))
        # totalIncomeTxtColor = FundColor.STYLE_RED if totalIncome > 0 else FundColor.STYLE_GREEN
        self.holdAmount.setText(holdAmountTxt)
        # self.holdIncomeTxt.setStyleSheet(self.holdIncomeTxt.styleSheet() + totalIncomeTxtColor)

        self.positionTable.horizontalHeader().update()
        self.positionTable.viewport().update()

    def refresh_optional_data(self, ret: list = None):
        """
        刷新自选基金数据
        :param ret: 手动传入数据
        :return:
        """
        if ret is None:
            ret = self.fundCrawler.get_funds_data(self.optionalFund, isOptional=True)
        # self.optionalTable.clearContents()
        self.optionalTable.setRowCount(len(ret))

        for index, item in enumerate(ret):
            print(index, item)
            fundCode = item['code']

            # 1.基金名称
            fundName = get_or_default(item['name'], '暂无')
            fundNameItem = QTableWidgetItem(fundName)
            self.optionalTable.setItem(index, 0, fundNameItem)

            # 2.基金代码
            fundCodeItem = QTableWidgetItem(fundCode)
            self.optionalTable.setItem(index, 1, fundCodeItem)

            # 3.基金估值
            fundExpectWorth = float(get_or_default(item['expectWorth']))
            fundExpectGrowth = float(get_or_default(item['expectGrowth']))
            fundExpectWorthColor = get_color(fundExpectGrowth, 'brush')
            fundExpectWorthItem = QTableWidgetItem(
                "{}% ({})".format(format(fundExpectGrowth, '.2f'), format(fundExpectWorth, '.4f')))
            self.optionalTable.setItem(index, 2, fundExpectWorthItem)
            self.optionalTable.item(index, 2).setForeground(fundExpectWorthColor)

            # 4.基金净值
            fundNetWorth = float(get_or_default(item['netWorth']))
            fundDayGrowth = float(get_or_default(item['dayGrowth']))
            fundNetWorthColor = get_color(fundDayGrowth, 'brush')
            fundNetWorthItem = QTableWidgetItem(
                "{}% ({})".format(format(fundDayGrowth, '.2f'), format(fundNetWorth, '.4f')))
            self.optionalTable.setItem(index, 3, fundNetWorthItem)
            self.optionalTable.item(index, 3).setForeground(fundNetWorthColor)

            # 5.近1周
            if 'lastWeekGrowth' in item and get_or_default(item['lastWeekGrowth']) != '0':
                lastWeekGrowth = float(item['lastWeekGrowth'])
                lastWeekGrowthColor = get_color(lastWeekGrowth, 'brush')
                lastWeekGrowthItem = QTableWidgetItem("{}%".format(format(lastWeekGrowth, '.2f')))
                self.optionalTable.setItem(index, 4, lastWeekGrowthItem)
                self.optionalTable.item(index, 4).setForeground(lastWeekGrowthColor)
            else:
                self.optionalTable.setItem(index, 4, QTableWidgetItem("-"))

            #  6.近1月

            if 'lastMonthGrowth' in item and get_or_default(item['lastMonthGrowth']) != '0':
                lastMonthGrowth = float(item['lastMonthGrowth'])
                lastMonthGrowthColor = get_color(lastMonthGrowth, 'brush')
                lastMonthGrowthItem = QTableWidgetItem("{}%".format(format(lastMonthGrowth, '.2f')))
                self.optionalTable.setItem(index, 5, lastMonthGrowthItem)
                self.optionalTable.item(index, 5).setForeground(lastMonthGrowthColor)
            else:
                self.optionalTable.setItem(index, 5, QTableWidgetItem("-"))

            #  7.近3月
            if 'lastThreeMonthsGrowth' in item and get_or_default(item['lastThreeMonthsGrowth']) != '0':
                lastThreeMonthsGrowth = float(item['lastThreeMonthsGrowth'])
                lastThreeMonthsGrowthColor = get_color(lastThreeMonthsGrowth, 'brush')
                lastThreeMonthsGrowthItem = QTableWidgetItem("{}%".format(format(lastThreeMonthsGrowth, '.2f')))
                self.optionalTable.setItem(index, 6, lastThreeMonthsGrowthItem)
                self.optionalTable.item(index, 6).setForeground(lastThreeMonthsGrowthColor)
            else:
                self.optionalTable.setItem(index, 6, QTableWidgetItem("-"))

            #  8.近6月
            if 'lastSixMonthsGrowth' in item and get_or_default(item['lastSixMonthsGrowth']) != '0':
                lastSixMonthsGrowth = float(item['lastSixMonthsGrowth'])
                lastSixMonthsGrowthColor = get_color(lastSixMonthsGrowth, 'brush')
                lastSixMonthsGrowthItem = QTableWidgetItem("{}%".format(format(lastSixMonthsGrowth, '.2f')))
                self.optionalTable.setItem(index, 7, lastSixMonthsGrowthItem)
                self.optionalTable.item(index, 7).setForeground(lastSixMonthsGrowthColor)
            else:
                self.optionalTable.setItem(index, 7, QTableWidgetItem("-"))

            #  9.近1年
            if 'lastYearGrowth' in item and get_or_default(item['lastYearGrowth']) != '0':
                lastYearGrowth = float(item['lastYearGrowth'])
                lastYearGrowthColor = get_color(lastYearGrowth, 'brush')
                lastYearGrowthItem = QTableWidgetItem("{}%".format(format(lastYearGrowth, '.2f')))
                self.optionalTable.setItem(index, 8, lastYearGrowthItem)
                self.optionalTable.item(index, 8).setForeground(lastYearGrowthColor)
            else:
                self.optionalTable.setItem(index, 8, QTableWidgetItem("-"))

            #  10.更新时间
            if 'expectWorthDate' in item:
                expectWorthDate = get_or_default(item['expectWorthDate'][5:16], '-')
                expectWorthDateItem = QTableWidgetItem("{}".format(expectWorthDate))
                self.optionalTable.setItem(index, 9, expectWorthDateItem)
            else:
                self.optionalTable.setItem(index, 9, QTableWidgetItem("-"))

        # 刷新时间
        refreshTime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.optional_refresh_time_txt.setText(refreshTime)

        self.optionalTable.viewport().update()

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
            ui.fundCode.setClearButtonEnabled(False)
            title = title + '：' + selectedItem[0].text()
        else:
            # 设置自动补全
            ui.fundCode.setCompleter(self.completer)

        dialog.accepted.connect(
            lambda: self.edit_fund_data(ui.fundCode.text(), ui.fundCost.text(), ui.fundUnits.text()))

        dialog.setWindowTitle(title)
        dialog.exec_()

    def optional_add_fund_clicked(self):
        fundCode = self.optionalFundCodeTxt.text()

        if '-' in fundCode:
            fundCode = fundCode.split('-')[0]

        if fundCode == '' or len(fundCode) != 6 or fundCode is None:
            QMessageBox.warning(self, '提示', '请检查输入的基金代码是否正确！')
            self.optionalFundCodeTxt.setText("")
            return

        if FundConfig.PLATFORM == 'darwin':
            selection_style = 'selection-background-color:rgb(0,99,225);selection-color:rgb(255,255,255)'
        else:
            selection_style = 'selection-background-color:rgb(51,153,255);selection-color:rgb(255,255,255)'

        # 设置选中色
        if fundCode in self.optionalFund:
            find_items = self.optionalTable.findItems(fundCode, Qt.MatchContains)
            for item in find_items:
                self.optionalTable.scrollToItem(item)
                self.optionalTable.setStyleSheet(selection_style)
                index = self.optionalTable.indexFromItem(item)
                self.optionalTable.selectRow(index.row())
            return

        # 新增时校验基金代码
        ret = self.fundCrawler.get_fund_info(fundCode)
        if ret is None or ret['FTYPE'] == '货币型':
            QMessageBox.warning(self, '提醒', '请检查基金代码！货币型基金，海外基金暂不支持！\n')
            return

        self.optionalFund.append(fundCode)
        self.write_local_config(fundCode, isOptional=True)
        self.refresh_optional_data()
        self.optionalTable.scrollToBottom()
        self.optionalTable.setStyleSheet(selection_style)
        self.optionalTable.selectRow(len(self.optionalFund) - 1)

    def edit_fund_data(self, fundCode, fundCost, fundUnits):
        """
        修改持仓基金
        :param fundCode: 基金代码
        :param fundCost: 基金成本
        :param fundUnits: 持有份额
        :return:
        """
        print(fundCode, fundCost, fundUnits)

        if fundCode == '' or fundCode is None:
            QMessageBox.warning(self, '提示', '基金代码输入不正确！')
            return

        # 对于自动补全带出的做处理
        if '-' in fundCode:
            fundCode = fundCode.split('-')[0]

        # 新增时校验基金代码
        if fundCode not in self.positionFund.keys():
            ret = self.fundCrawler.get_fund_info(fundCode)
            if ret is None or ret['FTYPE'] == '货币型':
                QMessageBox.warning(self, '提醒', '请检查基金代码！货币型基金，海外基金暂不支持！\n')
                return

        if fundCost is None or fundCost == '':
            fundCost = 0
        if fundUnits is None or fundUnits == '':
            fundUnits = 0

        # 对于自动补全带出的做处理
        if '-' in fundCode:
            fundCode = fundCode.split('-')[0]

        self.positionFund[fundCode] = {
            "fundCode": fundCode,
            "fundCost": float(fundCost),
            "fundUnits": float(fundUnits)
        }
        # self.fundConfigOrigin[]
        self.refresh_position_data()
        self.write_local_config(fundCode, float(fundCost), float(fundUnits))

    def fund_double_clicked(self, index: QModelIndex):
        try:
            rowIndex = index.row()
            if self.tabWidget.currentIndex() == 0:
                fundCode = self.positionTable.item(rowIndex, 1).text()
                fundName = self.positionTable.item(rowIndex, 0).text()
            else:
                fundCode = self.optionalTable.item(rowIndex, 1).text()
                fundName = self.optionalTable.item(rowIndex, 0).text()
            title = "业绩走势：{}-{}".format(fundCode, fundName)
            dialog = QDialog(self.centralwidget)
            windowsFlags = dialog.windowFlags()
            windowsFlags |= Qt.WindowMaximizeButtonHint
            dialog.setWindowFlags(windowsFlags)
            FundChartMain(dialog, fundCode, fundName)
            dialog.setWindowTitle(title)
            dialog.exec_()
        except Exception as e:
            print(e)
            QMessageBox.warning(self.parent(), '提示', '出现异常请重试!{}\t\t\n'.format(e))

    def setting_btn_clicked(self):
        dialog = QDialog(self.centralwidget)
        ui = Ui_FundSettingDialog()
        ui.setupUi(dialog)

        ui.isRecoveryTxt.hide()
        ui.fontNameCob.setCurrentText(FundConfig.FONT_NAME)
        ui.fontSizeCob.setCurrentText(str(FundConfig.FONT_SIZE))
        ui.enableRefreshChb.setChecked(FundConfig.AUTO_REFRESH_ENABLE)
        ui.refreshTimeoutTxt.setValue(FundConfig.AUTO_REFRESH_TIMEOUT)
        ui.enableProxyChb.setChecked(FundConfig.ENABLE_PROXY)
        ui.colorCob.setCurrentIndex(FundConfig.FUND_COLOR.value)
        ui.midTxt.setText(FundConfig.FUND_MID)
        ui.midTxt.setCursorPosition(0)
        ui.cloudSyncChb.setChecked(FundConfig.ENABLE_SYNC)

        ui.recoveryBtn.clearFocus()
        ui.saveBtn.setFocus()
        ui.saveBtn.clicked.connect(lambda: self.save_program_setting(ui))
        ui.recoveryBtn.clicked.connect(lambda: ui.isRecoveryTxt.setText('1'))
        ui.syncBtn.clicked.connect(
            lambda: QMessageBox.information(dialog, '提示', '同步成功\t\t\n') if self.sync.backup(
                ui.midTxt.text()) else QMessageBox.warning(
                dialog,
                '提示',
                '同步失败\t\t\n'))
        ui.recoveryBtn.clicked.connect(
            lambda: QMessageBox.information(dialog, '提示',
                                            '恢复成功\t\t\n') if self.sync.recovery(
                ui.midTxt.text()) else QMessageBox.warning(
                dialog,
                '提示',
                '恢复失败\t\t\n'))
        dialog.setWindowTitle("程序设置")
        dialog.exec_()

    def save_program_setting(self, dialog: Ui_FundSettingDialog):
        try:
            print('保存配置')
            FundConfig.FONT_NAME = dialog.fontNameCob.currentText()
            FundConfig.FONT_SIZE = int(dialog.fontSizeCob.currentText())
            FundConfig.AUTO_REFRESH_TIMEOUT = dialog.refreshTimeoutTxt.value()
            lastAutoRefreshEnable = FundConfig.AUTO_REFRESH_ENABLE
            FundConfig.AUTO_REFRESH_ENABLE = dialog.enableRefreshChb.isChecked()
            FundConfig.FUND_COLOR = ColorSwitch(dialog.colorCob.currentIndex())
            FundConfig.ENABLE_PROXY = dialog.enableProxyChb.isChecked()
            FundConfig.PROXY_POOL = dialog.proxyUrlTxt.text()
            FundConfig.ENABLE_SYNC = dialog.cloudSyncChb.isChecked()

            oldFundMid = FundConfig.FUND_MID
            newFundMid = dialog.midTxt.text()
            FundConfig.FUND_MID = newFundMid
            refreshDataFlag = oldFundMid != newFundMid

            # 更新自动刷新
            if lastAutoRefreshEnable and FundConfig.AUTO_REFRESH_ENABLE:
                self.timer.stop()
                self.timer.start(FundConfig.AUTO_REFRESH_TIMEOUT)
            elif lastAutoRefreshEnable and not FundConfig.AUTO_REFRESH_ENABLE:
                self.timer.stop()
            elif not lastAutoRefreshEnable and FundConfig.AUTO_REFRESH_ENABLE:
                self.timer.start(FundConfig.AUTO_REFRESH_TIMEOUT)

            font = QFont(dialog.fontNameCob.currentText(), FundConfig.FONT_SIZE)
            self.parentWindow.setFont(font)
            for child in self.parentWindow.allWidgets():
                child.setFont(font)

            self.dbSourceCob.setFont(QFont(FundConfig.FONT_NAME, FundConfig.FONT_SIZE - 1))

            self.fundConfigOrigin['fontName'] = FundConfig.FONT_NAME
            self.fundConfigOrigin['fontSize'] = FundConfig.FONT_SIZE
            self.fundConfigOrigin['enableAutoRefresh'] = FundConfig.AUTO_REFRESH_ENABLE
            self.fundConfigOrigin['autoRefreshTimeout'] = FundConfig.AUTO_REFRESH_TIMEOUT
            self.fundConfigOrigin['colorScheme'] = FundConfig.FUND_COLOR.value
            self.fundConfigOrigin['enableProxy'] = FundConfig.ENABLE_PROXY
            self.fundConfigOrigin['proxyAddress'] = FundConfig.PROXY_POOL
            self.fundConfigOrigin['mid'] = FundConfig.FUND_MID
            self.fundConfigOrigin['enableSync'] = FundConfig.ENABLE_SYNC

            # mid变化了 或者 点击过恢复按钮
            if refreshDataFlag or dialog.isRecoveryTxt.text() == '1':
                print('配置文件发生变化')
                self.start_init()
            else:
                self.write_local_config()


        except Exception as e:
            print(e)

    def read_local_config(self):
        """
        读取本地配置文件
        :return: void
        """
        home_dir = os.path.expanduser("~")
        if FundConfig.PLATFORM == 'win32':
            config_dir = home_dir + '/AppData/Roaming/LeekBox'
        else:
            config_dir = home_dir + '/Library/Application Support/LeekBox'
        is_dir_exists = os.path.exists(config_dir)
        if not is_dir_exists:
            os.makedirs(config_dir)
        self.config_path = config_dir + "/fund.json"
        try:
            config_old = 'fund.json'
            config = config_dir + '/fund.json'
            if os.path.exists(config_old):
                config = config_old
            with open(config, 'r', encoding='utf-8') as f:
                self.fundConfigOrigin = json.load(f)
                # 检查key值
                for key in FundConfig.CONFIG_KEYS:
                    if key not in self.fundConfigOrigin:
                        self.fundConfigOrigin[key] = None

                if type(self.fundConfigOrigin['positions']) != list:
                    self.fundConfigOrigin['positions'] = []

                if type(self.fundConfigOrigin['optional']) != list:
                    self.fundConfigOrigin['optional'] = []

                if type(self.fundConfigOrigin['crypto-coin']) != list:
                    self.fundConfigOrigin['crypto-coin'] = []
            # 删除旧的配置文件
            if os.path.exists(config_old):
                os.remove(config_old)
                self.write_local_config()

        except:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                config = {
                    'positions': [
                        {
                            'fundCode': '260108',
                            'fundCost': 1.000,
                            'fundUnits': 500.00
                        }
                    ],
                    'optional': ['260108'],
                    'source': 0,
                    'fontName': FundConfig.FONT_NAME,
                    'fontSize': 9,
                    'enableAutoRefresh': False,
                    'autoRefreshTimeout': 60000,
                    'colorScheme': 0,
                    'enableProxy': False,
                    'proxyAddress': '',
                    'mid': str(uuid.uuid4()),
                    'enableSync': False,
                    'crypto-coin': ["BTC-USDT", "ETH-USDT", "DOGE-USDT"],
                    'crypto-api': ""
                }
                self.fundConfigOrigin = config
                json.dump(config, f, indent=4, ensure_ascii=False)

    def write_local_config(self, fundCode: str = '', fundCost: float = 0, fundUnits: float = 0, isDelete: bool = False,
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
            # 单纯保存配置
            if fundCode is None or fundCode == '':
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.fundConfigOrigin, f, indent=4, ensure_ascii=False)
                    return
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
            with open(self.config_path, 'w', encoding='utf-8') as f:
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

        # 如果是darwin平台 则重置字体
        if FundConfig.PLATFORM == 'darwin':
            self.fundConfigOrigin['fontName'] = ''
            self.fundConfigOrigin['fontSize'] = ''

        db_source = min(int(self.getOrDefault('source', 0)), 1)

        FundConfig.DB_SWITCH = DBSource(db_source)
        FundConfig.FONT_NAME = self.getOrDefault('fontName', FundConfig.FONT_NAME)
        FundConfig.FONT_SIZE = self.getOrDefault('fontSize', FundConfig.FONT_SIZE)
        FundConfig.AUTO_REFRESH_ENABLE = self.getOrDefault('enableAutoRefresh', False)
        FundConfig.AUTO_REFRESH_TIMEOUT = self.getOrDefault('autoRefreshTimeout', 60000)
        FundConfig.FUND_COLOR = ColorSwitch(int(self.getOrDefault('colorScheme', 0)))
        FundConfig.ENABLE_PROXY = self.getOrDefault('enableProxy', False)
        FundConfig.PROXY_POOL = self.getOrDefault('proxyAddress', '')
        FundConfig.FUND_MID = self.getOrDefault('mid', str(uuid.uuid4()))
        FundConfig.ENABLE_SYNC = self.getOrDefault('enableSync', False)

        self.dbSourceCob.setCurrentIndex(FundConfig.DB_SWITCH.value)

    def getOrDefault(self, key, value):
        if key not in self.fundConfigOrigin \
                or self.fundConfigOrigin[key] is None \
                or self.fundConfigOrigin[key] == '':
            self.fundConfigOrigin[key] = value
            return value
        else:
            return self.fundConfigOrigin[key]

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

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        print('窗口隐藏')
        event.ignore()
        self.hide()
        if self.tip_cnt == 0:
            self.tip_cnt += 1
            self.trayIcon.showMessage(FundConfig.APP_NAME, '程序已隐藏到任务栏，双击图标可恢复！', self.icon)

    def except_hook(self, excType, excValue, traceBack):
        """
        全局异常捕捉
        :param excType:
        :param excValue:
        :param traceBack:
        :return:
        """

        err_msg = ''.join(traceback.format_exception(excType, excValue, traceBack))
        QMessageBox.critical(self, '异常', err_msg)

    # subscribe channels un_need login
    async def subscribe_without_login(self, url, channels):
        l = []
        while True:
            try:
                async with websockets.connect(url) as ws:
                    sub_param = {"op": "subscribe", "args": channels}
                    sub_str = json.dumps(sub_param)
                    await ws.send(sub_str)

                    while True:
                        try:
                            res_b = await asyncio.wait_for(ws.recv(), timeout=25)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                            try:
                                await ws.send('ping')
                                res_b = await ws.recv()
                                timestamp = get_timestamp()
                                res = inflate(res_b).decode('utf-8')
                                print(timestamp + res)
                                continue
                            except Exception as e:
                                timestamp = get_timestamp()
                                print(timestamp + "正在重连……")
                                print(e)
                                break

                        timestamp = get_timestamp()
                        res = inflate(res_b).decode('utf-8')
                        # print(timestamp + res)

                        # 停止运行
                        if not self.socket_running:
                            await self.unsubscribe_without_login(url, channels, timestamp)
                            break

                        res = eval(res)
                        if 'event' in res:
                            continue
                        for i in res:
                            if 'index/ticker' in res[i]:
                                self.refresh_coin_board(res)
                            elif 'spot/ticker' in res[i]:
                                self.refresh_coin_table(res)
                            elif 'depth' in res[i] and 'depth5' not in res[i]:
                                # 订阅频道是深度频道
                                if res['action'] == 'partial':
                                    for m in l:
                                        if res['data'][0]['instrument_id'] == m['instrument_id']:
                                            l.remove(m)
                                    # 获取首次全量深度数据
                                    bids_p, asks_p, instrument_id = partial(res, timestamp)
                                    d = {}
                                    d['instrument_id'] = instrument_id
                                    d['bids_p'] = bids_p
                                    d['asks_p'] = asks_p
                                    l.append(d)

                                    # 校验checksum
                                    checksum = res['data'][0]['checksum']
                                    # print(timestamp + '推送数据的checksum为：' + str(checksum))
                                    check_num = check(bids_p, asks_p)
                                    # print(timestamp + '校验后的checksum为：' + str(check_num))
                                    if check_num == checksum:
                                        print("校验结果为：True")
                                    else:
                                        print("校验结果为：False，正在重新订阅……")

                                        # 取消订阅
                                        await self.unsubscribe_without_login(url, channels, timestamp)
                                        # 发送订阅
                                        async with websockets.connect(url) as ws:
                                            sub_param = {"op": "subscribe", "args": channels}
                                            sub_str = json.dumps(sub_param)
                                            await ws.send(sub_str)
                                            timestamp = get_timestamp()
                                            print(timestamp + f"send: {sub_str}")

                                elif res['action'] == 'update':
                                    for j in l:
                                        if res['data'][0]['instrument_id'] == j['instrument_id']:
                                            # 获取全量数据
                                            bids_p = j['bids_p']
                                            asks_p = j['asks_p']
                                            # 获取合并后数据
                                            bids_p = update_bids(res, bids_p, timestamp)
                                            asks_p = update_asks(res, asks_p, timestamp)

                                            # 校验checksum
                                            checksum = res['data'][0]['checksum']
                                            # print(timestamp + '推送数据的checksum为：' + str(checksum))
                                            check_num = check(bids_p, asks_p)
                                            # print(timestamp + '校验后的checksum为：' + str(check_num))
                                            if check_num == checksum:
                                                print("校验结果为：True")
                                            else:
                                                print("校验结果为：False，正在重新订阅……")

                                                # 取消订阅
                                                await self.unsubscribe_without_login(url, channels, timestamp)
                                                # 发送订阅
                                                async with websockets.connect(url) as ws:
                                                    sub_param = {"op": "subscribe", "args": channels}
                                                    sub_str = json.dumps(sub_param)
                                                    await ws.send(sub_str)
                                                    timestamp = get_timestamp()
                                                    print(timestamp + f"send: {sub_str}")
                    if not self.socket_running:
                        print(timestamp + "手动结束……")
                        break
            except Exception as e:
                timestamp = get_timestamp()
                print(timestamp + "连接断开，正在重连……")
                print(e)
                continue

    # subscribe channels need login
    async def subscribe(self, url, api_key, passphrase, secret_key, channels):
        while True:
            try:
                async with websockets.connect(url) as ws:
                    # login
                    timestamp = str(server_timestamp())
                    login_str = login_params(timestamp, api_key, passphrase, secret_key)
                    await ws.send(login_str)
                    # time = get_timestamp()
                    # print(time + f"send: {login_str}")
                    res_b = await ws.recv()
                    res = inflate(res_b).decode('utf-8')
                    time = get_timestamp()
                    print(time + res)

                    # subscribe
                    sub_param = {"op": "subscribe", "args": channels}
                    sub_str = json.dumps(sub_param)
                    await ws.send(sub_str)
                    time = get_timestamp()
                    print(time + f"send: {sub_str}")

                    while True:
                        try:
                            res_b = await asyncio.wait_for(ws.recv(), timeout=25)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                            try:
                                await ws.send('ping')
                                res_b = await ws.recv()
                                time = get_timestamp()
                                res = inflate(res_b).decode('utf-8')
                                print(time + res)
                                continue
                            except Exception as e:
                                time = get_timestamp()
                                print(time + "正在重连……")
                                print(e)
                                break

                        time = get_timestamp()
                        res = inflate(res_b).decode('utf-8')
                        print(time + res)

            except Exception as e:
                time = get_timestamp()
                print(time + "连接断开，正在重连……")
                print(e)
                continue

    # unsubscribe channels
    async def unsubscribe(self, url, api_key, passphrase, secret_key, channels):
        async with websockets.connect(url) as ws:
            # login
            timestamp = str(server_timestamp())
            login_str = login_params(str(timestamp), api_key, passphrase, secret_key)
            await ws.send(login_str)
            # time = get_timestamp()
            # print(time + f"send: {login_str}")

            res_1 = await ws.recv()
            res = inflate(res_1).decode('utf-8')
            time = get_timestamp()
            print(time + res)

            # unsubscribe
            sub_param = {"op": "unsubscribe", "args": channels}
            sub_str = json.dumps(sub_param)
            await ws.send(sub_str)
            time = get_timestamp()
            print(time + f"send: {sub_str}")

            res_1 = await ws.recv()
            res = inflate(res_1).decode('utf-8')
            time = get_timestamp()
            print(time + res)

    # unsubscribe channels
    async def unsubscribe_without_login(self, url, channels, timestamp):
        async with websockets.connect(url) as ws:
            # unsubscribe
            sub_param = {"op": "unsubscribe", "args": channels}
            sub_str = json.dumps(sub_param)
            await ws.send(sub_str)
            print(timestamp + f"send: {sub_str}")

            res_1 = await ws.recv()
            res = inflate(res_1).decode('utf-8')
            print(timestamp + f"recv: {res}")

    def refresh_coin_board(self, data: dict):
        list = data['data']
        if self.tabWidget.currentIndex() != 2:
            return
        for item in list:
            coin_type = item['instrument_id']
            last_price = float(item['last'])
            open_price = float(item['open_utc8'])
            price_diff = last_price - open_price
            colorString = get_color(price_diff, 'str')
            changePercent = '{}%'.format(format(price_diff / open_price * 100, '.2f'))
            # priceChange = colorString.format(priceChange)
            changePercent = colorString.format(changePercent)
            if 'BTC' in coin_type:
                last_price_str = colorString.format(format(last_price, '.1f'))
                self.BoardChange.emit(1, [last_price_str, '', changePercent])
            elif 'ETH' in coin_type:
                last_price_str = colorString.format(format(last_price, '.2f'))
                self.BoardChange.emit(2, [last_price_str, '', changePercent])
            elif 'ADA' in coin_type:
                last_price_str = colorString.format(format(last_price, '.4f'))
                self.BoardChange.emit(3, [last_price_str, '', changePercent])
            elif 'XRP' in coin_type:
                last_price_str = colorString.format(format(last_price, '.4f'))
                self.BoardChange.emit(4, [last_price_str, '', changePercent])
            elif 'DOT' in coin_type:
                last_price_str = colorString.format(format(last_price, '.3f'))
                self.BoardChange.emit(5, [last_price_str, '', changePercent])

    def refresh_coin_table(self, data: dict):
        list = data['data']
        # print(list)
        if self.tabWidget.currentIndex() != 2:
            return
        self.TableChange.emit(list)

    def change_table_coneten(self, list: dict):
        self.coinMarketTable.setRowCount(len(self.op_coin))
        for item in list:
            coin_type = item['instrument_id']
            row_index = self.op_coin.index("spot/ticker:" + coin_type)
            coin_price = float(item['last'])
            coin_open = float(item['open_utc8'])
            change_percent = (coin_price - coin_open) / coin_open * 100
            change_color = get_color(change_percent, 'brush')

            # 货币名称
            coin_name_item = QTableWidgetItem(coin_type)
            self.coinMarketTable.setItem(row_index, 0, coin_name_item)

            # 最新价
            coin_price_str = '₮ {}'.format(coin_price)
            coin_price_item = QTableWidgetItem(coin_price_str)
            self.coinMarketTable.setItem(row_index, 1, coin_price_item)

            # 今日涨跌
            change_percent_item = QTableWidgetItem('{}%'.format(format(change_percent, '.2f')))
            self.coinMarketTable.setItem(row_index, 2, change_percent_item)
            self.coinMarketTable.item(row_index, 2).setForeground(change_color)

            # 24h最低
            low_24h = '₮ {}'.format(item['low_24h'])
            low_24h_item = QTableWidgetItem(low_24h)
            self.coinMarketTable.setItem(row_index, 3, low_24h_item)

            # 24h最高
            high_24h = '₮ {}'.format(item['high_24h'])
            high_24h_item = QTableWidgetItem(high_24h)
            self.coinMarketTable.setItem(row_index, 4, high_24h_item)

            # 24h成交量
            base_volume_24h = float(item['base_volume_24h'])
            base_volume_24h_str = ''
            if base_volume_24h > 100000000:
                base_volume_24h_str = '{} 亿'.format(format(base_volume_24h / 100000000, '.2f'))
            elif base_volume_24h > 10000:
                base_volume_24h_str = '{} 万'.format(format(base_volume_24h / 10000, '.2f'))
            base_volume_24h_item = QTableWidgetItem(base_volume_24h_str)
            self.coinMarketTable.setItem(row_index, 5, base_volume_24h_item)

            # 24h成交金额
            base_amount_24h = base_volume_24h * coin_price
            base_amount_24h_str = ''
            if base_amount_24h > 100000000:
                base_amount_24h_str = '₮ {} 亿'.format(format(base_amount_24h / 100000000, '.2f'))
            elif base_amount_24h > 10000:
                base_amount_24h_str = '₮ {} 万'.format(format(base_amount_24h / 10000, '.2f'))
            base_amount_24h_item = QTableWidgetItem(base_amount_24h_str)
            self.coinMarketTable.setItem(row_index, 6, base_amount_24h_item)
        self.coinMarketTable.viewport().update()

    def change_board_text(self, position: int, text: list):
        if position == 1:
            self.SHZ_Price.setText(text[0])
            self.SHZ_PriceChange.setText(text[1])
            self.SHZ_ChangePercent.setText(text[2])
        if position == 2:
            self.SZZ_Price.setText(text[0])
            self.SZZ_PriceChange.setText(text[1])
            self.SZZ_ChangePercent.setText(text[2])
        if position == 3:
            self.CY_Price.setText(text[0])
            self.CY_PriceChange.setText(text[1])
            self.CY_ChangePercent.setText(text[2])
        if position == 4:
            self.HS_Price.setText(text[0])
            self.HS_PriceChange.setText(text[1])
            self.HS_ChangePercent.setText(text[2])
        if position == 5:
            self.SZ_Price.setText(text[0])
            self.SZ_PriceChange.setText(text[1])
            self.SZ_ChangePercent.setText(text[2])

    def coin_double_clicked(self, index: QModelIndex):
        try:
            rowIndex = index.row()
            coin_pair = self.coinMarketTable.item(rowIndex, 0).text()
            coin_pair = coin_pair.lower()
            url = 'https://www.ouyi.cc/markets/spot-info/' + coin_pair
            # title = "行情"
            # dialog = QDialog(self.centralwidget)
            # windowsFlags = dialog.windowFlags()
            # windowsFlags |= Qt.WindowMaximizeButtonHint
            # dialog.setWindowFlags(windowsFlags)
            # dialog.setWindowTitle(title)
            # ui = Ui_FundBrowser()
            # ui.setupUi(dialog)
            # ui.grid_layout.addWidget(browser)
            # dialog.exec_()
        except Exception as e:
            print(e)
            QMessageBox.warning(self.parent(), '提示', '出现异常请重试!{}\t\t\n'.format(e))

    def add_coin_btn_clicked(self):
        print('add_coin_btn_clicked')
        coin_pair = self.coinPairText.text()
        if not coin_pair or len(coin_pair) < 5:
            return
        coin_pair = coin_pair.split(' ')[0]
        coin_pair = coin_pair.upper()
        self.fundConfigOrigin['crypto-coin'].append(coin_pair)
        self.write_local_config()
        self.start_websocket(True)
