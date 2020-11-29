# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fundViewForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(943, 614)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("PingFang SC")
        MainWindow.setFont(font)
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
        self.tabWidget.setStyleSheet("QTabBar::tab[width:80]")
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
        self.gridLayout.setContentsMargins(10, 0, 10, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.positionRefreshBtn = QtWidgets.QPushButton(self.tab)
        self.positionRefreshBtn.setObjectName("positionRefreshBtn")
        self.gridLayout.addWidget(self.positionRefreshBtn, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(748, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setContentsMargins(10, 0, 10, 10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_8.addWidget(self.tabWidget)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 10, 0, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
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
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
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
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_6.addWidget(self.label_11)
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
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ZZ_Price = QtWidgets.QLabel(self.centralwidget)
        self.ZZ_Price.setAlignment(QtCore.Qt.AlignCenter)
        self.ZZ_Price.setObjectName("ZZ_Price")
        self.horizontalLayout_5.addWidget(self.ZZ_Price)
        self.ZZ_PriceChange = QtWidgets.QLabel(self.centralwidget)
        self.ZZ_PriceChange.setAlignment(QtCore.Qt.AlignCenter)
        self.ZZ_PriceChange.setObjectName("ZZ_PriceChange")
        self.horizontalLayout_5.addWidget(self.ZZ_PriceChange)
        self.ZZ_ChangePercent = QtWidgets.QLabel(self.centralwidget)
        self.ZZ_ChangePercent.setAlignment(QtCore.Qt.AlignCenter)
        self.ZZ_ChangePercent.setObjectName("ZZ_ChangePercent")
        self.horizontalLayout_5.addWidget(self.ZZ_ChangePercent)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
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
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "添加"))
        self.positionRefreshBtn.setText(_translate("MainWindow", "刷新"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "持仓"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "自选"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>上证指数（SH000001）</p></body></html>"))
        self.SHZ_Price.setText(_translate("MainWindow", "3408.31"))
        self.SHZ_PriceChange.setText(_translate("MainWindow", "+38.58"))
        self.SHZ_ChangePercent.setText(_translate("MainWindow", "+1.14%"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p>深证指数（SZ399001 ）</p></body></html>"))
        self.SZZ_Price.setText(_translate("MainWindow", "13690.88"))
        self.SZZ_PriceChange.setText(_translate("MainWindow", "+90.89"))
        self.SZZ_ChangePercent.setText(_translate("MainWindow", "+0.67%"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p>沪深300 （SZ399300 ）</p></body></html>"))
        self.HS_Price.setText(_translate("MainWindow", "4980.77"))
        self.HS_PriceChange.setText(_translate("MainWindow", "+61.18"))
        self.HS_ChangePercent.setText(_translate("MainWindow", "+1.24%"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p>中证500（ SH000905 ）</p></body></html>"))
        self.ZZ_Price.setText(_translate("MainWindow", "6351.61"))
        self.ZZ_PriceChange.setText(_translate("MainWindow", "+17.31"))
        self.ZZ_ChangePercent.setText(_translate("MainWindow", "+0.27%"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p>创业板指 （SZ399006 ）</p></body></html>"))
        self.CY_Price.setText(_translate("MainWindow", "2618.99"))
        self.CY_PriceChange.setText(_translate("MainWindow", "+9.60"))
        self.CY_ChangePercent.setText(_translate("MainWindow", "+0.37%"))
