import sys

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication

from src.fundConfig import FundConfig
from src.fundViewMain import FundViewMain
import ui.fundViewResource_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FundViewMain(app)

    # 设置全局字体
    font = QFont(FundConfig.FONT_NAME, FundConfig.FONT_SIZE)
    app.setFont(font)

    w.setWindowTitle('基金')
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    w.show()

    sys.exit(app.exec_())
