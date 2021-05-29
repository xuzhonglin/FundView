# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fund_main_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.addFundBtn = QtWidgets.QPushButton(self.tab)
        self.addFundBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.addFundBtn.setObjectName("addFundBtn")
        self.gridLayout.addWidget(self.addFundBtn, 0, 5, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.holdAmount = QtWidgets.QLabel(self.tab)
        self.holdAmount.setStyleSheet("margin-right:5px")
        self.holdAmount.setObjectName("holdAmount")
        self.horizontalLayout_6.addWidget(self.holdAmount)
        self.holdIncomeTxt = QtWidgets.QLabel(self.tab)
        self.holdIncomeTxt.setStyleSheet("margin-right:5px;")
        self.holdIncomeTxt.setObjectName("holdIncomeTxt")
        self.horizontalLayout_6.addWidget(self.holdIncomeTxt)
        self.incomeTxt = QtWidgets.QLabel(self.tab)
        self.incomeTxt.setStyleSheet("margin-right:5px;")
        self.incomeTxt.setObjectName("incomeTxt")
        self.horizontalLayout_6.addWidget(self.incomeTxt)
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.dbSourceCob = QtWidgets.QComboBox(self.tab)
        self.dbSourceCob.setMinimumSize(QtCore.QSize(100, 0))
        self.dbSourceCob.setObjectName("dbSourceCob")
        self.dbSourceCob.addItem("")
        self.dbSourceCob.addItem("")
        self.horizontalLayout_6.addWidget(self.dbSourceCob)
        self.settingLabel = ClickableLabel(self.tab)
        self.settingLabel.setMinimumSize(QtCore.QSize(20, 20))
        self.settingLabel.setMaximumSize(QtCore.QSize(20, 20))
        self.settingLabel.setStyleSheet("QLabel:hover{\n"
"background-color: #ffffff;\n"
"border-radius:5px;\n"
"}")
        self.settingLabel.setText("")
        self.settingLabel.setPixmap(QtGui.QPixmap(":/icon/setting/setting.png"))
        self.settingLabel.setScaledContents(False)
        self.settingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.settingLabel.setObjectName("settingLabel")
        self.horizontalLayout_6.addWidget(self.settingLabel)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 6)
        self.editFundBtn = QtWidgets.QPushButton(self.tab)
        self.editFundBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.editFundBtn.setObjectName("editFundBtn")
        self.gridLayout.addWidget(self.editFundBtn, 0, 4, 1, 1)
        self.positionTable = QtWidgets.QTableWidget(self.tab)
        self.positionTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.positionTable.setAlternatingRowColors(True)
        self.positionTable.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.positionTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.positionTable.setShowGrid(True)
        self.positionTable.setGridStyle(QtCore.Qt.SolidLine)
        self.positionTable.setWordWrap(False)
        self.positionTable.setColumnCount(0)
        self.positionTable.setObjectName("positionTable")
        self.positionTable.setRowCount(0)
        self.positionTable.horizontalHeader().setHighlightSections(False)
        self.positionTable.horizontalHeader().setStretchLastSection(False)
        self.positionTable.verticalHeader().setVisible(False)
        self.positionTable.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.positionTable, 2, 0, 1, 6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.position_refresh_time_txt = QtWidgets.QLabel(self.tab)
        self.position_refresh_time_txt.setObjectName("position_refresh_time_txt")
        self.gridLayout.addWidget(self.position_refresh_time_txt, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setStyleSheet("margin-left:5px")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.positionRefreshBtn = QtWidgets.QPushButton(self.tab)
        self.positionRefreshBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.positionRefreshBtn.setObjectName("positionRefreshBtn")
        self.gridLayout.addWidget(self.positionRefreshBtn, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.optionalTable = QtWidgets.QTableWidget(self.tab_2)
        self.optionalTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.optionalTable.setAlternatingRowColors(True)
        self.optionalTable.setWordWrap(False)
        self.optionalTable.setObjectName("optionalTable")
        self.optionalTable.setColumnCount(0)
        self.optionalTable.setRowCount(0)
        self.optionalTable.horizontalHeader().setHighlightSections(False)
        self.gridLayout_3.addWidget(self.optionalTable, 1, 0, 1, 6)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 3, 1, 1)
        self.addOptionalFundBtn = QtWidgets.QPushButton(self.tab_2)
        self.addOptionalFundBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.addOptionalFundBtn.setObjectName("addOptionalFundBtn")
        self.gridLayout_3.addWidget(self.addOptionalFundBtn, 0, 5, 1, 1)
        self.optionalRefreshBtn = QtWidgets.QPushButton(self.tab_2)
        self.optionalRefreshBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.optionalRefreshBtn.setObjectName("optionalRefreshBtn")
        self.gridLayout_3.addWidget(self.optionalRefreshBtn, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setStyleSheet("margin-left:5px")
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 1, 1, 1)
        self.optionalFundCodeTxt = QtWidgets.QLineEdit(self.tab_2)
        self.optionalFundCodeTxt.setMinimumSize(QtCore.QSize(0, 23))
        self.optionalFundCodeTxt.setMaximumSize(QtCore.QSize(200, 16777215))
        self.optionalFundCodeTxt.setStyleSheet("padding-left:3px;")
        self.optionalFundCodeTxt.setClearButtonEnabled(True)
        self.optionalFundCodeTxt.setObjectName("optionalFundCodeTxt")
        self.gridLayout_3.addWidget(self.optionalFundCodeTxt, 0, 4, 1, 1)
        self.optional_refresh_time_txt = QtWidgets.QLabel(self.tab_2)
        self.optional_refresh_time_txt.setObjectName("optional_refresh_time_txt")
        self.gridLayout_3.addWidget(self.optional_refresh_time_txt, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.coinPairText = QtWidgets.QLineEdit(self.tab_3)
        self.coinPairText.setMaximumSize(QtCore.QSize(200, 16777215))
        self.coinPairText.setStyleSheet("padding-left:3px;")
        self.coinPairText.setObjectName("coinPairText")
        self.gridLayout_4.addWidget(self.coinPairText, 0, 3, 1, 1)
        self.addCoinPairBtn = QtWidgets.QPushButton(self.tab_3)
        self.addCoinPairBtn.setObjectName("addCoinPairBtn")
        self.gridLayout_4.addWidget(self.addCoinPairBtn, 0, 4, 1, 1)
        self.total_assets_txt = ClickableLabel(self.tab_3)
        self.total_assets_txt.setMinimumSize(QtCore.QSize(70, 0))
        self.total_assets_txt.setObjectName("total_assets_txt")
        self.gridLayout_4.addWidget(self.total_assets_txt, 0, 1, 1, 1)
        self.coinMarketTable = QtWidgets.QTableWidget(self.tab_3)
        self.coinMarketTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.coinMarketTable.setObjectName("coinMarketTable")
        self.coinMarketTable.setColumnCount(0)
        self.coinMarketTable.setRowCount(0)
        self.gridLayout_4.addWidget(self.coinMarketTable, 1, 0, 1, 5)
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout_8.addWidget(self.tabWidget)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 10, 0, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.headLabelOne = QtWidgets.QLabel(self.centralwidget)
        self.headLabelOne.setAlignment(QtCore.Qt.AlignCenter)
        self.headLabelOne.setObjectName("headLabelOne")
        self.verticalLayout.addWidget(self.headLabelOne)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SHZ_Price = QtWidgets.QLabel(self.centralwidget)
        self.SHZ_Price.setAlignment(QtCore.Qt.AlignCenter)
        self.SHZ_Price.setObjectName("SHZ_Price")
        self.horizontalLayout_2.addWidget(self.SHZ_Price)
        self.SHZ_PriceChange = QtWidgets.QLabel(self.centralwidget)
        self.SHZ_PriceChange.setAlignment(QtCore.Qt.AlignCenter)
        self.SHZ_PriceChange.setObjectName("SHZ_PriceChange")
        self.horizontalLayout_2.addWidget(self.SHZ_PriceChange)
        self.SHZ_ChangePercent = QtWidgets.QLabel(self.centralwidget)
        self.SHZ_ChangePercent.setAlignment(QtCore.Qt.AlignCenter)
        self.SHZ_ChangePercent.setObjectName("SHZ_ChangePercent")
        self.horizontalLayout_2.addWidget(self.SHZ_ChangePercent)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.headLabelTwo = QtWidgets.QLabel(self.centralwidget)
        self.headLabelTwo.setAlignment(QtCore.Qt.AlignCenter)
        self.headLabelTwo.setObjectName("headLabelTwo")
        self.verticalLayout_5.addWidget(self.headLabelTwo)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.SZZ_Price = QtWidgets.QLabel(self.centralwidget)
        self.SZZ_Price.setAlignment(QtCore.Qt.AlignCenter)
        self.SZZ_Price.setObjectName("SZZ_Price")
        self.horizontalLayout_3.addWidget(self.SZZ_Price)
        self.SZZ_PriceChange = QtWidgets.QLabel(self.centralwidget)
        self.SZZ_PriceChange.setAlignment(QtCore.Qt.AlignCenter)
        self.SZZ_PriceChange.setObjectName("SZZ_PriceChange")
        self.horizontalLayout_3.addWidget(self.SZZ_PriceChange)
        self.SZZ_ChangePercent = QtWidgets.QLabel(self.centralwidget)
        self.SZZ_ChangePercent.setAlignment(QtCore.Qt.AlignCenter)
        self.SZZ_ChangePercent.setObjectName("SZZ_ChangePercent")
        self.horizontalLayout_3.addWidget(self.SZZ_ChangePercent)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headLabelThree = QtWidgets.QLabel(self.centralwidget)
        self.headLabelThree.setAlignment(QtCore.Qt.AlignCenter)
        self.headLabelThree.setObjectName("headLabelThree")
        self.verticalLayout_2.addWidget(self.headLabelThree)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.CY_Price = QtWidgets.QLabel(self.centralwidget)
        self.CY_Price.setAlignment(QtCore.Qt.AlignCenter)
        self.CY_Price.setObjectName("CY_Price")
        self.horizontalLayout_7.addWidget(self.CY_Price)
        self.CY_PriceChange = QtWidgets.QLabel(self.centralwidget)
        self.CY_PriceChange.setAlignment(QtCore.Qt.AlignCenter)
        self.CY_PriceChange.setObjectName("CY_PriceChange")
        self.horizontalLayout_7.addWidget(self.CY_PriceChange)
        self.CY_ChangePercent = QtWidgets.QLabel(self.centralwidget)
        self.CY_ChangePercent.setAlignment(QtCore.Qt.AlignCenter)
        self.CY_ChangePercent.setObjectName("CY_ChangePercent")
        self.horizontalLayout_7.addWidget(self.CY_ChangePercent)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.headLabelFour = QtWidgets.QLabel(self.centralwidget)
        self.headLabelFour.setAlignment(QtCore.Qt.AlignCenter)
        self.headLabelFour.setObjectName("headLabelFour")
        self.verticalLayout_6.addWidget(self.headLabelFour)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.HS_Price = QtWidgets.QLabel(self.centralwidget)
        self.HS_Price.setAlignment(QtCore.Qt.AlignCenter)
        self.HS_Price.setObjectName("HS_Price")
        self.horizontalLayout_4.addWidget(self.HS_Price)
        self.HS_PriceChange = QtWidgets.QLabel(self.centralwidget)
        self.HS_PriceChange.setAlignment(QtCore.Qt.AlignCenter)
        self.HS_PriceChange.setObjectName("HS_PriceChange")
        self.horizontalLayout_4.addWidget(self.HS_PriceChange)
        self.HS_ChangePercent = QtWidgets.QLabel(self.centralwidget)
        self.HS_ChangePercent.setAlignment(QtCore.Qt.AlignCenter)
        self.HS_ChangePercent.setObjectName("HS_ChangePercent")
        self.horizontalLayout_4.addWidget(self.HS_ChangePercent)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.headLabelFive = QtWidgets.QLabel(self.centralwidget)
        self.headLabelFive.setAlignment(QtCore.Qt.AlignCenter)
        self.headLabelFive.setObjectName("headLabelFive")
        self.verticalLayout_4.addWidget(self.headLabelFive)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.SZ_Price = QtWidgets.QLabel(self.centralwidget)
        self.SZ_Price.setAlignment(QtCore.Qt.AlignCenter)
        self.SZ_Price.setObjectName("SZ_Price")
        self.horizontalLayout_5.addWidget(self.SZ_Price)
        self.SZ_PriceChange = QtWidgets.QLabel(self.centralwidget)
        self.SZ_PriceChange.setAlignment(QtCore.Qt.AlignCenter)
        self.SZ_PriceChange.setObjectName("SZ_PriceChange")
        self.horizontalLayout_5.addWidget(self.SZ_PriceChange)
        self.SZ_ChangePercent = QtWidgets.QLabel(self.centralwidget)
        self.SZ_ChangePercent.setAlignment(QtCore.Qt.AlignCenter)
        self.SZ_ChangePercent.setObjectName("SZ_ChangePercent")
        self.horizontalLayout_5.addWidget(self.SZ_ChangePercent)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.dbSourceCob.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addFundBtn.setText(_translate("MainWindow", "添加"))
        self.holdAmount.setText(_translate("MainWindow", "持有金额：5177.94"))
        self.holdIncomeTxt.setText(_translate("MainWindow", "持有收益：219.94"))
        self.incomeTxt.setText(_translate("MainWindow", "预估收益：-58.8"))
        self.label_6.setText(_translate("MainWindow", "数据仅供参考"))
        self.label_4.setText(_translate("MainWindow", "数据源："))
        self.dbSourceCob.setCurrentText(_translate("MainWindow", "天天基金"))
        self.dbSourceCob.setItemText(0, _translate("MainWindow", "天天基金"))
        self.dbSourceCob.setItemText(1, _translate("MainWindow", "蚂蚁财富"))
        self.editFundBtn.setText(_translate("MainWindow", "编辑"))
        self.positionTable.setSortingEnabled(True)
        self.position_refresh_time_txt.setText(_translate("MainWindow", "2020-11-30 12:20:20"))
        self.label_2.setText(_translate("MainWindow", "刷新时间："))
        self.positionRefreshBtn.setText(_translate("MainWindow", "刷新"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "持仓基金"))
        self.addOptionalFundBtn.setText(_translate("MainWindow", "添加"))
        self.optionalRefreshBtn.setText(_translate("MainWindow", "刷新"))
        self.label_7.setText(_translate("MainWindow", "刷新时间："))
        self.optionalFundCodeTxt.setPlaceholderText(_translate("MainWindow", "基金代码或名称"))
        self.optional_refresh_time_txt.setText(_translate("MainWindow", "2020-11-30 12:20:20"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "自选基金"))
        self.coinPairText.setPlaceholderText(_translate("MainWindow", "搜索交易对 BTC-USDT"))
        self.addCoinPairBtn.setText(_translate("MainWindow", "添加"))
        self.total_assets_txt.setText(_translate("MainWindow", "----"))
        self.label.setText(_translate("MainWindow", "总资产估值："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "虚拟货币"))
        self.headLabelOne.setText(_translate("MainWindow", "上证指数（000001）"))
        self.SHZ_Price.setText(_translate("MainWindow", "3408.31"))
        self.SHZ_PriceChange.setText(_translate("MainWindow", "+38.58"))
        self.SHZ_ChangePercent.setText(_translate("MainWindow", "+1.14%"))
        self.headLabelTwo.setText(_translate("MainWindow", "深证成指（399001 ）"))
        self.SZZ_Price.setText(_translate("MainWindow", "13690.88"))
        self.SZZ_PriceChange.setText(_translate("MainWindow", "+90.89"))
        self.SZZ_ChangePercent.setText(_translate("MainWindow", "+0.67%"))
        self.headLabelThree.setText(_translate("MainWindow", "创业板指 （399006 ）"))
        self.CY_Price.setText(_translate("MainWindow", "2618.99"))
        self.CY_PriceChange.setText(_translate("MainWindow", "+9.60"))
        self.CY_ChangePercent.setText(_translate("MainWindow", "+0.37%"))
        self.headLabelFour.setText(_translate("MainWindow", "沪深300 （000300 ）"))
        self.HS_Price.setText(_translate("MainWindow", "4980.77"))
        self.HS_PriceChange.setText(_translate("MainWindow", "+61.18"))
        self.HS_ChangePercent.setText(_translate("MainWindow", "+1.24%"))
        self.headLabelFive.setText(_translate("MainWindow", "上证50（ 000016 ）"))
        self.SZ_Price.setText(_translate("MainWindow", "6351.61"))
        self.SZ_PriceChange.setText(_translate("MainWindow", "+17.31"))
        self.SZ_ChangePercent.setText(_translate("MainWindow", "+0.27%"))
from form.clickable_label import ClickableLabel
import form.fund_resource_rc
