# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addFundDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddFundDialog(object):
    def setupUi(self, AddFundDialog):
        AddFundDialog.setObjectName("AddFundDialog")
        AddFundDialog.resize(340, 169)
        self.gridLayout = QtWidgets.QGridLayout(AddFundDialog)
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.cancelBtn = QtWidgets.QPushButton(AddFundDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.gridLayout.addWidget(self.cancelBtn, 2, 2, 1, 1)
        self.saveBtn = QtWidgets.QPushButton(AddFundDialog)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")
        self.Label = QtWidgets.QLabel(AddFundDialog)
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.fundCode = QtWidgets.QLineEdit(AddFundDialog)
        self.fundCode.setObjectName("fundCode")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fundCode)
        self.Label_2 = QtWidgets.QLabel(AddFundDialog)
        self.Label_2.setObjectName("Label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.fundCost = QtWidgets.QLineEdit(AddFundDialog)
        self.fundCost.setObjectName("fundCost")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fundCost)
        self.Label_3 = QtWidgets.QLabel(AddFundDialog)
        self.Label_3.setObjectName("Label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_3)
        self.fundUnits = QtWidgets.QLineEdit(AddFundDialog)
        self.fundUnits.setObjectName("fundUnits")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.fundUnits)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 3)

        self.retranslateUi(AddFundDialog)
        self.saveBtn.clicked.connect(AddFundDialog.accept)
        self.cancelBtn.clicked.connect(AddFundDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddFundDialog)
        AddFundDialog.setTabOrder(self.fundCode, self.fundCost)
        AddFundDialog.setTabOrder(self.fundCost, self.fundUnits)
        AddFundDialog.setTabOrder(self.fundUnits, self.saveBtn)
        AddFundDialog.setTabOrder(self.saveBtn, self.cancelBtn)

    def retranslateUi(self, AddFundDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFundDialog.setWindowTitle(_translate("AddFundDialog", "Dialog"))
        self.cancelBtn.setText(_translate("AddFundDialog", "取消"))
        self.saveBtn.setText(_translate("AddFundDialog", "保存"))
        self.saveBtn.setShortcut(_translate("AddFundDialog", "Return"))
        self.Label.setText(_translate("AddFundDialog", "基金代码"))
        self.Label_2.setText(_translate("AddFundDialog", "持仓成本"))
        self.Label_3.setText(_translate("AddFundDialog", "持有份额"))
