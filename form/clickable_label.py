from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    # 自定义信号, 注意信号必须为类属性
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked.emit()
