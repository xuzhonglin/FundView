# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fundDealDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FundDealDialog(object):
    def setupUi(self, FundDealDialog):
        FundDealDialog.setObjectName("FundDealDialog")
        FundDealDialog.resize(381, 284)
        self.gridLayout = QtWidgets.QGridLayout(FundDealDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.fundCodeLabel = QtWidgets.QLabel(FundDealDialog)
        self.fundCodeLabel.setObjectName("fundCodeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fundCodeLabel)
        self.fundCodeTxt = QtWidgets.QLineEdit(FundDealDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fundCodeTxt.sizePolicy().hasHeightForWidth())
        self.fundCodeTxt.setSizePolicy(sizePolicy)
        self.fundCodeTxt.setMinimumSize(QtCore.QSize(250, 20))
        self.fundCodeTxt.setMaximumSize(QtCore.QSize(500, 16777215))
        self.fundCodeTxt.setObjectName("fundCodeTxt")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fundCodeTxt)
        self.netWorthLabel = QtWidgets.QLabel(FundDealDialog)
        self.netWorthLabel.setObjectName("netWorthLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.netWorthLabel)
        self.netWorthTxt = QtWidgets.QLineEdit(FundDealDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.netWorthTxt.sizePolicy().hasHeightForWidth())
        self.netWorthTxt.setSizePolicy(sizePolicy)
        self.netWorthTxt.setMinimumSize(QtCore.QSize(250, 20))
        self.netWorthTxt.setMaximumSize(QtCore.QSize(500, 16777215))
        self.netWorthTxt.setObjectName("netWorthTxt")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.netWorthTxt)
        self.buyRateLabel = QtWidgets.QLabel(FundDealDialog)
        self.buyRateLabel.setObjectName("buyRateLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.buyRateLabel)
        self.buyRateTxt = QtWidgets.QLineEdit(FundDealDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buyRateTxt.sizePolicy().hasHeightForWidth())
        self.buyRateTxt.setSizePolicy(sizePolicy)
        self.buyRateTxt.setMinimumSize(QtCore.QSize(250, 20))
        self.buyRateTxt.setMaximumSize(QtCore.QSize(500, 16777215))
        self.buyRateTxt.setObjectName("buyRateTxt")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buyRateTxt)
        self.buyAmountLabel = QtWidgets.QLabel(FundDealDialog)
        self.buyAmountLabel.setObjectName("buyAmountLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.buyAmountLabel)
        self.buyAmountTxt = QtWidgets.QLineEdit(FundDealDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buyAmountTxt.sizePolicy().hasHeightForWidth())
        self.buyAmountTxt.setSizePolicy(sizePolicy)
        self.buyAmountTxt.setMinimumSize(QtCore.QSize(250, 20))
        self.buyAmountTxt.setMaximumSize(QtCore.QSize(500, 16777215))
        self.buyAmountTxt.setObjectName("buyAmountTxt")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.buyAmountTxt)
        self.allUnitsLabel = QtWidgets.QLabel(FundDealDialog)
        self.allUnitsLabel.setObjectName("allUnitsLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.allUnitsLabel)
        self.allUnitsTxt = QtWidgets.QLineEdit(FundDealDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allUnitsTxt.sizePolicy().hasHeightForWidth())
        self.allUnitsTxt.setSizePolicy(sizePolicy)
        self.allUnitsTxt.setMinimumSize(QtCore.QSize(250, 20))
        self.allUnitsTxt.setObjectName("allUnitsTxt")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.allUnitsTxt)
        self.saleUnitsLabel = QtWidgets.QLabel(FundDealDialog)
        self.saleUnitsLabel.setObjectName("saleUnitsLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.saleUnitsLabel)
        self.saleUnitsTxt = QtWidgets.QLineEdit(FundDealDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saleUnitsTxt.sizePolicy().hasHeightForWidth())
        self.saleUnitsTxt.setSizePolicy(sizePolicy)
        self.saleUnitsTxt.setMinimumSize(QtCore.QSize(250, 20))
        self.saleUnitsTxt.setMaximumSize(QtCore.QSize(500, 16777215))
        self.saleUnitsTxt.setObjectName("saleUnitsTxt")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.saleUnitsTxt)
        self.saleRateLayout = QtWidgets.QHBoxLayout()
        self.saleRateLayout.setObjectName("saleRateLayout")
        self.rate20Btn = QtWidgets.QPushButton(FundDealDialog)
        self.rate20Btn.setMinimumSize(QtCore.QSize(0, 22))
        self.rate20Btn.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.rate20Btn.setFont(font)
        self.rate20Btn.setObjectName("rate20Btn")
        self.saleRateLayout.addWidget(self.rate20Btn)
        self.rate30Btn = QtWidgets.QPushButton(FundDealDialog)
        self.rate30Btn.setMinimumSize(QtCore.QSize(0, 22))
        self.rate30Btn.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.rate30Btn.setFont(font)
        self.rate30Btn.setObjectName("rate30Btn")
        self.saleRateLayout.addWidget(self.rate30Btn)
        self.rate50Btn = QtWidgets.QPushButton(FundDealDialog)
        self.rate50Btn.setMinimumSize(QtCore.QSize(0, 20))
        self.rate50Btn.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.rate50Btn.setFont(font)
        self.rate50Btn.setObjectName("rate50Btn")
        self.saleRateLayout.addWidget(self.rate50Btn)
        self.rate100Btn = QtWidgets.QPushButton(FundDealDialog)
        self.rate100Btn.setMinimumSize(QtCore.QSize(0, 22))
        self.rate100Btn.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.rate100Btn.setFont(font)
        self.rate100Btn.setObjectName("rate100Btn")
        self.saleRateLayout.addWidget(self.rate100Btn)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.saleRateLayout)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 3)
        self.cancelBtn = QtWidgets.QPushButton(FundDealDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.gridLayout.addWidget(self.cancelBtn, 1, 2, 1, 1)
        self.saveBtn = QtWidgets.QPushButton(FundDealDialog)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(FundDealDialog)
        self.cancelBtn.clicked.connect(FundDealDialog.reject)
        self.saveBtn.clicked.connect(FundDealDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(FundDealDialog)

    def retranslateUi(self, FundDealDialog):
        _translate = QtCore.QCoreApplication.translate
        FundDealDialog.setWindowTitle(_translate("FundDealDialog", "Dialog"))
        self.fundCodeLabel.setText(_translate("FundDealDialog", "基金代码"))
        self.netWorthLabel.setText(_translate("FundDealDialog", "最新净值"))
        self.buyRateLabel.setText(_translate("FundDealDialog", "申购费率"))
        self.buyAmountLabel.setText(_translate("FundDealDialog", "加仓金额"))
        self.allUnitsLabel.setText(_translate("FundDealDialog", "全部份额"))
        self.saleUnitsLabel.setText(_translate("FundDealDialog", "卖出份额"))
        self.rate20Btn.setText(_translate("FundDealDialog", "20%"))
        self.rate30Btn.setText(_translate("FundDealDialog", "30%"))
        self.rate50Btn.setText(_translate("FundDealDialog", "50%"))
        self.rate100Btn.setText(_translate("FundDealDialog", "全部"))
        self.cancelBtn.setText(_translate("FundDealDialog", "取消"))
        self.saveBtn.setText(_translate("FundDealDialog", "保存"))
