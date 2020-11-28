import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from src.fundViewMain import FundViewMain
import ui.fundViewResource

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = FundViewMain()
    w.setWindowTitle('基金')
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    # w.setFixedSize(w.width(), w.height())
    w.show()

    sys.exit(app.exec_())
