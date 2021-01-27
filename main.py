#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/27 17:16
@Author   : colinxu
@File     : main.py
@Desc     : 主函数
"""
import sys, os

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication

from src.fund_config import FundConfig
from src.fund_main import FundMain

if __name__ == '__main__':

    try:
        if os.path.isfile("upgrade.bat"):
            os.remove("upgrade.bat")
    except:
        pass

    app = QApplication(sys.argv)
    w = FundMain(app)

    # 设置全局字体
    font = QFont(FundConfig.FONT_NAME, FundConfig.FONT_SIZE)
    app.setFont(font)

    w.setWindowTitle(FundConfig.APP_NAME + ' ' + FundConfig.VERSION)
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    w.show()

    sys.exit(app.exec_())
