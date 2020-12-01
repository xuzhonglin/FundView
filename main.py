import sys

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication

from src.fundViewMain import FundViewMain
import ui.fundViewResource_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FundViewMain()

    # 设置全局字体
    fontFamily = "PingFang SC" if sys.platform == 'darwin' else "微软雅黑"
    fontSize = 13 if sys.platform == 'darwin' else 9
    font = QFont(fontFamily, fontSize)
    app.setFont(font)

    w.setWindowTitle('基金')
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    w.show()

    sys.exit(app.exec_())
