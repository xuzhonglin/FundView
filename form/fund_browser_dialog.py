# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fund_browser_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FundBrowser(object):
    def setupUi(self, FundBrowser):
        FundBrowser.setObjectName("FundBrowser")
        FundBrowser.resize(885, 520)
        self.gridLayout = QtWidgets.QGridLayout(FundBrowser)
        self.gridLayout.setObjectName("gridLayout")
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.gridLayout.addLayout(self.grid_layout, 0, 0, 1, 1)

        self.retranslateUi(FundBrowser)
        QtCore.QMetaObject.connectSlotsByName(FundBrowser)

    def retranslateUi(self, FundBrowser):
        _translate = QtCore.QCoreApplication.translate
        FundBrowser.setWindowTitle(_translate("FundBrowser", "Dialog"))
