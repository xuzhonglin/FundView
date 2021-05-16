from enum import Enum

from PyQt5.QtGui import QBrush, QColor


class DBSource(Enum):
    TTT = 0
    ANT = 1


class ColorSwitch(Enum):
    RED_GREEN = 0
    GREEN_RED = 1
    BLACK_ONLY = 2


class _FundColor:
    RED_STR = '<span style=" color:#ff0000;">{}</span>'
    GREEN_STR = '<span style=" color:#00aa00;">{}</span>'
    BLACK_STR = '<span style=" color:#000000;">{}</span>'
    RED_BRUSH = QBrush(QColor('#ff0000'))
    GREEN_BRUSH = QBrush(QColor('#00aa00'))
    BLACK_BRUSH = QBrush(QColor('#000000'))
    STYLE_RED = 'color: rgb(255, 0, 0);'
    STYLE_GREEN = 'color: rgb(0, 170, 0);'
    STYLE_BLACK = 'color: rgb(0, 0, 0);'
