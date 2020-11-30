import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

from src.fundViewMain import FundViewMain
import ui.fundViewResource_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FundViewMain()
    fontFamily = "PingFang SC" if sys.platform == 'darwin' else "等线"
    font = QtGui.QFont()
    font.setFamily(fontFamily)
    w.setFont(font)

    w.setWindowTitle('基金')
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    # w.setWindowIcon(QIcon(':/icon/windows/icon_mac.icns'))
    # w.setFixedSize(w.width(), w.height())
    w.show()

    sys.exit(app.exec_())
