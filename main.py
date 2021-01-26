import sys, os

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication

from src.fundConfig import FundConfig
from src.fundViewMain import FundViewMain
from src.fund_update import FundUpdate

if __name__ == '__main__':

    is_update = False
    update_param = ''
    for index, item in enumerate(sys.argv):
        if item == '--update' or item == '-u':
            is_update = True
            update_param = sys.argv[index + 1]
            break

    if is_update:
        os.rename(sys.argv[0], 'main.py')
    #
    # print(is_update, update_param)

    app = QApplication(sys.argv)
    w = FundViewMain(app)

    # 设置全局字体
    font = QFont(FundConfig.FONT_NAME, FundConfig.FONT_SIZE)
    app.setFont(font)

    w.setWindowTitle(FundConfig.APP_NAME + ' ' + FundConfig.VERSION)
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    w.show()

    sys.exit(app.exec_())
