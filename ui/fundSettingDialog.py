# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fundSettingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FundSettingDialog(object):
    def setupUi(self, FundSettingDialog):
        FundSettingDialog.setObjectName("FundSettingDialog")
        FundSettingDialog.resize(398, 268)
        FundSettingDialog.setAutoFillBackground(False)
        FundSettingDialog.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(FundSettingDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(FundSettingDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setMinimumSize(QtCore.QSize(50, 0))
        self.label_6.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.enableProxyChb = QtWidgets.QCheckBox(self.groupBox_2)
        self.enableProxyChb.setEnabled(False)
        self.enableProxyChb.setMinimumSize(QtCore.QSize(70, 0))
        self.enableProxyChb.setMaximumSize(QtCore.QSize(80, 16777215))
        self.enableProxyChb.setObjectName("enableProxyChb")
        self.gridLayout_2.addWidget(self.enableProxyChb, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setMinimumSize(QtCore.QSize(50, 0))
        self.label_7.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.cloudSyncChb = QtWidgets.QCheckBox(self.groupBox_2)
        self.cloudSyncChb.setEnabled(True)
        self.cloudSyncChb.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cloudSyncChb.setObjectName("cloudSyncChb")
        self.gridLayout_2.addWidget(self.cloudSyncChb, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.recoveryBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.recoveryBtn.setEnabled(False)
        self.recoveryBtn.setMinimumSize(QtCore.QSize(80, 0))
        self.recoveryBtn.setObjectName("recoveryBtn")
        self.gridLayout_2.addWidget(self.recoveryBtn, 2, 3, 1, 1)
        self.proxyUrlTxt = QtWidgets.QLineEdit(self.groupBox_2)
        self.proxyUrlTxt.setEnabled(False)
        self.proxyUrlTxt.setObjectName("proxyUrlTxt")
        self.gridLayout_2.addWidget(self.proxyUrlTxt, 1, 2, 1, 2)
        self.midTxt = QtWidgets.QLineEdit(self.groupBox_2)
        self.midTxt.setEnabled(False)
        self.midTxt.setObjectName("midTxt")
        self.gridLayout_2.addWidget(self.midTxt, 3, 1, 1, 3)
        self.enableRefreshChb = QtWidgets.QCheckBox(self.groupBox_2)
        self.enableRefreshChb.setMinimumSize(QtCore.QSize(70, 0))
        self.enableRefreshChb.setMaximumSize(QtCore.QSize(80, 16777215))
        self.enableRefreshChb.setObjectName("enableRefreshChb")
        self.gridLayout_2.addWidget(self.enableRefreshChb, 0, 1, 1, 1)
        self.syncBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.syncBtn.setEnabled(False)
        self.syncBtn.setObjectName("syncBtn")
        self.gridLayout_2.addWidget(self.syncBtn, 2, 2, 1, 1)
        self.refreshTimeoutTxt = QtWidgets.QSpinBox(self.groupBox_2)
        self.refreshTimeoutTxt.setEnabled(False)
        self.refreshTimeoutTxt.setMinimumSize(QtCore.QSize(80, 0))
        self.refreshTimeoutTxt.setSuffix("")
        self.refreshTimeoutTxt.setPrefix("")
        self.refreshTimeoutTxt.setMinimum(30000)
        self.refreshTimeoutTxt.setMaximum(999000)
        self.refreshTimeoutTxt.setSingleStep(1000)
        self.refreshTimeoutTxt.setObjectName("refreshTimeoutTxt")
        self.gridLayout_2.addWidget(self.refreshTimeoutTxt, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 3)
        self.saveBtn = QtWidgets.QPushButton(FundSettingDialog)
        self.saveBtn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout.addWidget(self.saveBtn, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(FundSettingDialog)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(FundSettingDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(50, 0))
        self.label.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.fontNameCob = QtWidgets.QFontComboBox(self.groupBox)
        self.fontNameCob.setMaximumSize(QtCore.QSize(120, 16777215))
        self.fontNameCob.setFocusPolicy(QtCore.Qt.TabFocus)
        self.fontNameCob.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.fontNameCob.setFontFilters(QtWidgets.QFontComboBox.ScalableFonts)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.fontNameCob.setCurrentFont(font)
        self.fontNameCob.setObjectName("fontNameCob")
        self.gridLayout_3.addWidget(self.fontNameCob, 0, 1, 1, 1)
        self.colorCob = QtWidgets.QComboBox(self.groupBox)
        self.colorCob.setMaximumSize(QtCore.QSize(120, 16777215))
        self.colorCob.setObjectName("colorCob")
        self.colorCob.addItem("")
        self.colorCob.addItem("")
        self.colorCob.addItem("")
        self.gridLayout_3.addWidget(self.colorCob, 1, 1, 1, 1)
        self.fontSizeCob = QtWidgets.QComboBox(self.groupBox)
        self.fontSizeCob.setMinimumSize(QtCore.QSize(120, 0))
        self.fontSizeCob.setObjectName("fontSizeCob")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.fontSizeCob.addItem("")
        self.gridLayout_3.addWidget(self.fontSizeCob, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setMinimumSize(QtCore.QSize(50, 0))
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setMinimumSize(QtCore.QSize(50, 0))
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)

        self.retranslateUi(FundSettingDialog)
        self.pushButton.clicked.connect(FundSettingDialog.reject)
        self.saveBtn.clicked.connect(FundSettingDialog.accept)
        self.enableProxyChb.toggled['bool'].connect(self.proxyUrlTxt.setEnabled)
        self.enableRefreshChb.toggled['bool'].connect(self.refreshTimeoutTxt.setEnabled)
        self.cloudSyncChb.toggled['bool'].connect(self.syncBtn.setEnabled)
        self.cloudSyncChb.toggled['bool'].connect(self.recoveryBtn.setEnabled)
        self.cloudSyncChb.toggled['bool'].connect(self.midTxt.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(FundSettingDialog)

    def retranslateUi(self, FundSettingDialog):
        _translate = QtCore.QCoreApplication.translate
        FundSettingDialog.setWindowTitle(_translate("FundSettingDialog", "Dialog"))
        self.groupBox_2.setTitle(_translate("FundSettingDialog", "数据设置"))
        self.label_6.setText(_translate("FundSettingDialog", "代理："))
        self.enableProxyChb.setText(_translate("FundSettingDialog", "开启代理"))
        self.label_8.setText(_translate("FundSettingDialog", "毫秒"))
        self.label_7.setText(_translate("FundSettingDialog", "刷新："))
        self.cloudSyncChb.setText(_translate("FundSettingDialog", "云端同步"))
        self.label_2.setText(_translate("FundSettingDialog", "MID："))
        self.recoveryBtn.setText(_translate("FundSettingDialog", "恢复"))
        self.proxyUrlTxt.setPlaceholderText(_translate("FundSettingDialog", "代理地址"))
        self.enableRefreshChb.setText(_translate("FundSettingDialog", "自动刷新"))
        self.syncBtn.setText(_translate("FundSettingDialog", "同步"))
        self.label_4.setText(_translate("FundSettingDialog", "同步："))
        self.saveBtn.setText(_translate("FundSettingDialog", "保存"))
        self.pushButton.setText(_translate("FundSettingDialog", "取消"))
        self.groupBox.setTitle(_translate("FundSettingDialog", "外观设置"))
        self.label.setText(_translate("FundSettingDialog", "字体："))
        self.colorCob.setItemText(0, _translate("FundSettingDialog", "红涨绿跌"))
        self.colorCob.setItemText(1, _translate("FundSettingDialog", "绿涨红跌"))
        self.colorCob.setItemText(2, _translate("FundSettingDialog", "单色纯黑"))
        self.fontSizeCob.setCurrentText(_translate("FundSettingDialog", "7"))
        self.fontSizeCob.setItemText(0, _translate("FundSettingDialog", "7"))
        self.fontSizeCob.setItemText(1, _translate("FundSettingDialog", "8"))
        self.fontSizeCob.setItemText(2, _translate("FundSettingDialog", "9"))
        self.fontSizeCob.setItemText(3, _translate("FundSettingDialog", "10"))
        self.fontSizeCob.setItemText(4, _translate("FundSettingDialog", "11"))
        self.fontSizeCob.setItemText(5, _translate("FundSettingDialog", "12"))
        self.fontSizeCob.setItemText(6, _translate("FundSettingDialog", "13"))
        self.fontSizeCob.setItemText(7, _translate("FundSettingDialog", "14"))
        self.fontSizeCob.setItemText(8, _translate("FundSettingDialog", "15"))
        self.fontSizeCob.setItemText(9, _translate("FundSettingDialog", "16"))
        self.label_5.setText(_translate("FundSettingDialog", "配色："))
        self.label_9.setText(_translate("FundSettingDialog", "字号："))
