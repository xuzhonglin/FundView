import sys

from PyQt5.QtCore import QFile, QTextStream
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

    # set stylesheet
    # file = QFile(":/dark.qss")
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())

    # qss = ''
    # with open('new1.qss', 'r',encoding='gbk') as f:
    #     qss = f.read()
    #     app.setStyleSheet(qss)

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w.setWindowTitle('韭菜盒子 ' + FundConfig.VERSION)
    w.setWindowIcon(QIcon(':/icon/windows/icon_windows.ico'))
    w.show()

    sys.exit(app.exec_())
