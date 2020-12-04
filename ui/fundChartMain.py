import json
import os, requests
import sys
from math import ceil, floor

from PyQt5 import QtGui
from PyQt5.QtChart import QCategoryAxis, QLegend, QChart, QLineSeries, QChartView
from PyQt5.QtCore import Qt, QRectF, QPoint, QPointF
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QImage, QPixmap, QPen, QPainter
from PyQt5.QtWidgets import QMainWindow, QGraphicsProxyWidget, QVBoxLayout, QLabel, QWidget, QHBoxLayout, \
    QGraphicsLineItem, QApplication, QDialog

from ui.fundChartDialog import Ui_FundChartDialog
from src.fundCrawler import FundCrawler
# import jpype
import traceback

RED_STR = '<span style=" color:#ff0000;">{}</span>'
GREEN_STR = '<span style=" color:#00aa00;">{}</span>'
RED = QBrush(QColor('#ff0000'))
GREEN = QBrush(QColor('#00aa00'))
STYLE_RED = 'color: rgb(255, 0, 0);'
STYLE_GREEN = 'color: rgb(0, 170, 0);'


class FundChartMain(QMainWindow, Ui_FundChartDialog):

    def __init__(self, parent, fundCode: str, chartType: int):
        """
        构造函数
        :param fundCode: 基金代码
        :param chartType: 表格类型 ：1 历史净值，2 持仓股票
        """
        super().__init__()
        self.setupUi(parent)
        chart = ChartView(self, fundCode=fundCode)
        self.chartLayout.addWidget(chart)


class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):
    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50, 50, 50, 100);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, points):
        self.titleLabel.setText(title)
        for serie, point in points:
            if serie not in self.Cache:
                item = ToolTipItem(
                    serie.color(),
                    (serie.name() or "-") + ":" + str(point.y()), self)
                self.layout().addWidget(item)
                self.Cache[serie] = item
            else:
                self.Cache[serie].setText(
                    (serie.name() or "-") + ":" + str(point.y()))
            self.Cache[serie].setVisible(serie.isVisible())  # 隐藏那些不可用的项
        self.adjustSize()  # 调整大小


class GraphicsProxyWidget(QGraphicsProxyWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def width(self):
        return self.size().width()

    def height(self):
        return self.size().height()

    def show(self, title, points, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, points)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, *args, fundCode):
        super(ChartView, self).__init__(*args)
        self.fundCode = fundCode
        self.resize(650, 350)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        self.FundCrawler = FundCrawler()

        self.initChart()

        # 提示widget
        self.toolTipWidget = GraphicsProxyWidget(self._chart)

        # line
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        # 一些固定计算，减少mouseMoveEvent中的计算量
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.min_x, self.max_x = axisX.min(), axisX.max()
        self.min_y, self.max_y = axisY.min(), axisY.max()

    def initChart(self):
        originData = self.FundCrawler.get_fund_performance_ydi(self.fundCode)
        # print(data['netWorthData'][-10:])
        data = originData['netWorthData'][-90:]
        self.get_pre_index(data)
        x = []
        for item in data:
            x.append(item[0])
        self.category = x
        self._chart = QChart(title="业绩走势：{} ({})".format(originData['name'], originData['code']))
        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        dataList = []
        baseWorth = float(data[0][1])
        for item in data:
            curWorth = float(item[1])
            growth = (curWorth - baseWorth) / baseWorth * 100
            dataList.append(round(growth, 2))
        dataTable = [
            [self.fundCode, dataList],
        ]

        for series_name, data_list in dataTable:
            series = QLineSeries(self._chart)
            for j, v in enumerate(data_list):
                series.append(j, v)
            series.setName(series_name)
            series.setPointsVisible(True)  # 显示圆点
            series.hovered.connect(self.handleSeriesHoverd)  # 鼠标悬停
            self._chart.addSeries(series)

        self._chart.createDefaultAxes()  # 创建默认的轴
        axisX = self._chart.axisX()  # x轴
        axisX.setTickCount(3)  # x轴设置7个刻度
        axisX.setGridLineVisible(False)  # 隐藏从x轴往上的线条
        axisY = self._chart.axisY()
        axisY.setTickCount(6)  # y轴设置7个刻度

        down, up = self.get_pre_index(data)
        axisY.setRange(down, up)  # 设置y轴范围
        # 自定义x轴
        axis_x = QCategoryAxis(self._chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
        axis_x.setTickCount(len(self.category))
        axis_x.setGridLineVisible(False)
        min_x = axisX.min()
        max_x = axisX.max()
        # step = (max_x - min_x) / (6 - 1)  # 7个tick

        axis_x.append(self.category[0], min_x)
        axis_x.append(self.category[int(len(self.category) * 0.25)], (max_x - min_x) * 0.25)
        axis_x.append(self.category[int(len(self.category) * 0.5)], (max_x - min_x) * 0.5)
        axis_x.append(self.category[int(len(self.category) * 0.75)], (max_x - min_x) * 0.75)
        axis_x.append(self.category[-1], max_x)

        # for i in range(0, 6):
        #     print(self.category[i], min_x + i * step)
        #     axis_x.append(self.category[i], min_x + i * step)
        self._chart.setAxisX(axis_x, self._chart.series()[-1])
        # chart的图例
        legend = self._chart.legend()
        # legend.
        # 设置图例由Series来决定样式
        legend.setMarkerShape(QLegend.MarkerShapeFromSeries)
        # 遍历图例上的标记并绑定信号
        for marker in legend.markers():
            # 隐藏图例
            marker.setVisible(False)
            # 点击事件
            # marker.clicked.connect(self.handleMarkerClicked)
            # 鼠标悬停事件
            marker.hovered.connect(self.handleMarkerHovered)

        self.setChart(self._chart)

    def get_pre_index(self, data):
        baseValue = float(data[0][1])
        maxValue = 0
        minValue = 0
        for item in data:
            value = (float(item[1]) - baseValue) / baseValue * 100
            maxValue = max(maxValue, value)
            minValue = min(minValue, value)
        # floor(minValue)

        print(floor(minValue), ceil(maxValue))
        return floor(minValue) - 5, ceil(maxValue) + 5

    def resizeEvent(self, event):
        super(ChartView, self).resizeEvent(event)
        # 当窗口大小改变时需要重新计算
        # 坐标系中左上角顶点
        self.point_top = self._chart.mapToPosition(QPointF(self.min_x, self.max_y))
        # 坐标原点坐标
        self.point_bottom = self._chart.mapToPosition(QPointF(self.min_x, self.min_y))
        self.step_x = (self.max_x - self.min_x) / (self._chart.axisX().tickCount() - 1)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round((x - self.min_x) / self.step_x)
        # 得到在坐标系中的所有正常显示的series的类型和点
        points = [(serie, serie.at(index))
                  for serie in self._chart.series()
                  if self.min_x <= x <= self.max_x and
                  self.min_y <= y <= self.max_y]
        if points:
            pos_x = self._chart.mapToPosition(
                QPointF(index * self.step_x + self.min_x, self.min_y))
            self.lineItem.setLine(pos_x.x(), self.point_top.y(),
                                  pos_x.x(), self.point_bottom.y())
            self.lineItem.show()
            try:
                title = self.category[index]
            except:
                title = ""
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            # 如果鼠标位置离右侧的距离小于tip宽度
            x = pos.x() - t_width if self.width() - pos.x() - 20 < t_width else pos.x()
            # 如果鼠标位置离底部的高度小于tip高度
            y = pos.y() - t_height if self.height() - pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(title, points, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def handleMarkerClicked(self):
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        visible = not marker.series().isVisible()
        #         # 隐藏或显示series
        marker.series().setVisible(visible)
        marker.setVisible(True)  # 要保证marker一直显示
        # 透明度
        alpha = 1.0 if visible else 0.4
        # 设置label的透明度
        brush = marker.labelBrush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)
        # 设置marker的透明度
        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)
        # 设置画笔透明度
        pen = marker.pen()
        color = pen.color()
        color.setAlphaF(alpha)
        pen.setColor(color)
        marker.setPen(pen)

    def handleMarkerHovered(self, status):
        # 设置series的画笔宽度
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        series = marker.series()
        if not series:
            return
        pen = series.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        series.setPen(pen)

    def handleSeriesHoverd(self, point, state):
        # 设置series的画笔宽度
        series = self.sender()  # 信号发送者
        pen = series.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if state else -1))
        series.setPen(pen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ChartView(fundCode='110011')
    view.show()
    sys.exit(app.exec_())
