import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from fundViewMain import FundViewMain

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = FundViewMain()
    w.setWindowTitle('基金')
    w.setWindowIcon(QIcon('icon_windows.ico'))
    # w.setFixedSize(w.width(), w.height())
    w.show()

    sys.exit(app.exec_())
