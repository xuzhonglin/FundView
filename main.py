#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/27 17:16
@Author   : colinxu
@File     : main.py
@Desc     : 主函数
"""
import io
import sys, os
import traceback

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication, QMessageBox

from src.fund_config import FundConfig
from src.fund_main import FundMain

if __name__ == '__main__':

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
    usr_home = os.path.expanduser('~')
    print(usr_home)

    try:
        if os.path.isfile("upgrade.bat"):
            os.remove("upgrade.bat")
    except:
        pass

    app = QApplication(sys.argv)

    serverName = 'LeekBox'
    socket = QLocalSocket()
    socket.connectToServer(serverName)

    # 如果连接成功，表明server已经存在，当前已有实例在运行
    if socket.waitForConnected(500):
        print('程序已经存在运行实例')
        sys.exit(app.quit())

    # 没有实例运行，创建服务器
    localServer = QLocalServer()
    localServer.listen(serverName)

    try:
        w = FundMain(app)

        # 设置全局字体
        font = QFont(FundConfig.FONT_NAME, FundConfig.FONT_SIZE)
        app.setFont(font)

        w.setWindowTitle(FundConfig.APP_NAME + ' ' + FundConfig.VERSION)
        w.setWindowIcon(QIcon(':/icon/new/windows/leekbox-icon-256.ico'))
        w.show()

        # 有新client连接，激活窗口
        localServer.newConnection.connect(lambda: w.showNormal())

        sys.exit(app.exec_())

    except Exception as e:
        print(e)
        print('traceback.format_exc():\n%s' % traceback.format_exc())  # 字符串
        QMessageBox.critical(None, '提醒', '启动异常，{}\t\n'.format(traceback.format_exc()))

    finally:
        localServer.close()
