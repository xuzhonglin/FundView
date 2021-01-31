import sys
from math import ceil, floor

from PyQt5.QtChart import QCategoryAxis, QChart, QLineSeries, QChartView, QLegend
from PyQt5.QtCore import Qt, QRectF, QPoint, QPointF, QMargins
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter
from PyQt5.QtWidgets import QMainWindow, QGraphicsProxyWidget, QVBoxLayout, QLabel, QWidget, QHBoxLayout, \
    QGraphicsLineItem, QApplication, QDialog, QMessageBox

from form.fund_chart_dialog import Ui_FundChartDialog
from src.fund_crawler import FundCrawler


class FundChartMain(QMainWindow, Ui_FundChartDialog):

    def __init__(self, parent: QDialog, fundCode: str, fundName: str):
        """
        构造函数
        :param fundCode: 基金代码
        :param chartType: 表格类型 ：1 历史净值，2 持仓股票
        """
        super().__init__()
        self.setupUi(parent)
        self.fund_code = fundCode
        self.chart = ChartView(self, fundCode=fundCode, fundName=fundName)
        self.chartLayout.addWidget(self.chart)
        self.init_slot()
        self.init_period_increase()

    def init_slot(self):
        self.oneMonthRadio.toggled.connect(lambda a: self.radio_button_check(a, 'ONE_MONTH'))
        self.threeMonthRadio.toggled.connect(lambda a: self.radio_button_check(a, 'THREE_MONTH'))
        self.sixMonthRadio.toggled.connect(lambda a: self.radio_button_check(a, 'SIX_MONTH'))
        self.oneYearRadio.toggled.connect(lambda a: self.radio_button_check(a, 'ONE_YEAR'))
        self.threeYearRadio.toggled.connect(lambda a: self.radio_button_check(a, 'THREE_YEAR'))

    def radio_button_check(self, isChecked: bool, type: str):
        if not isChecked: return
        self.chart.initChart(type)

    def init_period_increase(self):
        fund_crawler = FundCrawler()
        data = fund_crawler.get_fund_growth(self.fund_code)
        self.one_month_txt.setText('{}%（{}）'.format(data['lastMonthGrowth'], data['lastMonthGrowthRank']))
        self.three_month_txt.setText('{}%（{}）'.format(data['lastThreeMonthsGrowth'], data['lastThreeMonthsGrowthRank']))
        self.six_month_txt.setText('{}%（{}）'.format(data['lastSixMonthsGrowth'], data['lastSixMonthsGrowthRank']))
        self.one_year_txt.setText('{}%（{}）'.format(data['lastYearGrowth'], data['lastYearGrowthRank']))
        print(data)


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
        layout.setContentsMargins(8, 8, 8, 8)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, points, fmt: str = '{}'):
        self.titleLabel.setText(title)
        for serie, point in points:
            if serie not in self.Cache:
                item = ToolTipItem(
                    serie.color(),
                    (serie.name().split('：')[0] or "-") + "：" + fmt.format(point.y()), self)

                self.layout().addWidget(item)
                self.Cache[serie] = item
            else:
                self.Cache[serie].setText(
                    (serie.name().split('：')[0] or "-") + "：" + fmt.format(point.y()))
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

    def show(self, title, fmt, points, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, points, fmt)
        super(GraphicsProxyWidget, self).show()


class ChartView(QChartView):

    def __init__(self, *args, fundCode, fundName):
        super(ChartView, self).__init__(*args)
        self.fundCode = fundCode
        self.cacheData = []
        self.resize(650, 350)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        # 基金爬虫
        self.FundCrawler = FundCrawler()
        self.cacheData = {}
        self.fundName = fundName
        self.initChart()

    def initChart_bak(self, type: str = 'THREE_MONTH'):

        if type not in self.cacheData:
            tempData = self.FundCrawler.get_fund_performance_ttt(self.fundCode, type)
            self.cacheData[type] = tempData

        data = self.cacheData[type]

        if len(data) == 0:
            print('渲染异常')
            self.setDisabled(True)
            QMessageBox.warning(self, '提示', '图形渲染失败，请稍后重试！\t')
            data = [['', 1.0, 2.0, 3.0]]

        if not self.isEnabled():
            self.setEnabled(True)

        self.category = []
        for item in data:
            self.category.append(item[0])
        # self._chart = QChart(title="业绩走势：{} ({})".format(self.fundName, self.fundCode))
        self._chart = QChart()

        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        # 设置图表margin
        self._chart.setMargins(QMargins(20, 5, 35, 20))

        self._chart.setContentsMargins(0, 0, 0, 0)

        if len(data[0]) == 4:
            dataList = [[], [], []]
        else:
            dataList = [[], []]

        # 插入数据
        for item in data:
            for i in range(len(item) - 1):
                dataList[i].append(item[i + 1])

        if len(dataList) == 3:
            dataTable = [
                ['本基金：{}%'.format(dataList[0][-1]), dataList[0]],
                ['沪深300：{}%'.format(dataList[1][-1]), dataList[1]],
                ['上证指数：{}%'.format(dataList[2][-1]), dataList[2]],
            ]
        else:
            dataTable = [
                ['本基金：{}%'.format(dataList[0][-1]), dataList[0]],
                ['同类均值：{}%'.format(dataList[1][-1]), dataList[1]],
            ]

        for series_name, data_list in dataTable:
            series = QLineSeries(self._chart)
            for j, v in enumerate(data_list):
                series.append(j, v)
            series.setName(series_name)
            # series.setPointsVisible(True)  # 显示圆点
            # series.setPointLabelsVisible(True) #显示数值
            # series.hovered.connect(self.handleSeriesHoverd)  # 鼠标悬停
            self._chart.addSeries(series)

        # self._chart.setStyle()

        self._chart.createDefaultAxes()  # 创建默认的轴
        axisX = self._chart.axisX()  # x轴
        axisX.setTickCount(6)  # x轴设置7个刻度
        axisX.setGridLineVisible(False)  # 隐藏从x轴往上的线条

        axisY = self._chart.axisY()
        axisY.setTickCount(6)  # y轴设置7个刻度

        down, up = self.get_pre_index(data)
        # down, up = -20, 50
        axisY.setRange(down, up)  # 设置y轴范围
        # 设置坐标格式
        axisY.setLabelFormat("%0.1f%")
        # 自定义x轴
        axis_x = QCategoryAxis(self._chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
        axis_x.setTickCount(len(self.category))
        # axis_x.setGridLineVisible(False)
        min_x = axisX.min()
        max_x = axisX.max()
        # step = (max_x - min_x) / (6 - 1)  # 7个tick

        axis_x.append(self.category[0], min_x)
        axis_x.append(self.category[int(len(self.category) * 0.25)], (max_x - min_x) * 0.25)
        axis_x.append(self.category[int(len(self.category) * 0.5)], (max_x - min_x) * 0.5)
        axis_x.append(self.category[int(len(self.category) * 0.75)], (max_x - min_x) * 0.75)
        axis_x.append(self.category[-1], max_x)

        self._chart.setAxisX(axis_x, self._chart.series()[-1])

        # self._chart.legend(
        # chart的图例
        legend = self._chart.legend()
        # legend.setVisible(False)
        # legend.
        # 设置图例由Series来决定样式
        legend.setMarkerShape(QLegend.MarkerShapeFromSeries)
        # 遍历图例上的标记并绑定信号
        for marker in legend.markers():
            # 隐藏图例
            # marker.setVisible(False)
            # 点击事件
            marker.clicked.connect(self.handleMarkerClicked)
            # 鼠标悬停事件
            marker.hovered.connect(self.handleMarkerHovered)

        self.setChart(self._chart)
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

    def initChart(self, type: str = 'THREE_MONTH'):

        if type not in self.cacheData:
            tempData = self.FundCrawler.get_fund_performance_ttt_new(self.fundCode, type)
            self.cacheData[type] = tempData

        data = self.cacheData[type]['data']
        expansion = self.cacheData[type]['expansion']

        if len(data) == 0:
            print('渲染异常')
            self.setDisabled(True)
            QMessageBox.warning(self, '提示', '图形渲染失败，请稍后重试！\t')
            data = [['', 1.0, 2.0, 3.0]]
            expansion = '暂无'

        if not self.isEnabled():
            self.setEnabled(True)

        self.category = []
        for item in data:
            self.category.append(item[0])
        # self._chart = QChart(title="业绩走势：{} ({})".format(self.fundName, self.fundCode))
        self._chart = QChart()

        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        # 设置图表margin
        self._chart.setMargins(QMargins(20, 5, 35, 20))

        self._chart.setContentsMargins(0, 0, 0, 0)

        dataList = [[], [], []]

        # 插入数据
        for item in data:
            for i in range(len(item) - 1):
                dataList[i].append(item[i + 1])

        dataTable = [
            ['本基金：{}%'.format(dataList[0][-1]), dataList[0]],
            ['同类均值：{}%'.format(dataList[1][-1]), dataList[1]],
            ['{}：{}%'.format(expansion, dataList[2][-1]), dataList[2]],
        ]

        for series_name, data_list in dataTable:
            series = QLineSeries(self._chart)
            for j, v in enumerate(data_list):
                series.append(j, v)
            series.setName(series_name)
            # series.setPointsVisible(True)  # 显示圆点
            # series.setPointLabelsVisible(True) #显示数值
            # series.hovered.connect(self.handleSeriesHoverd)  # 鼠标悬停
            self._chart.addSeries(series)

        # self._chart.setStyle()

        self._chart.createDefaultAxes()  # 创建默认的轴
        axisX = self._chart.axisX()  # x轴
        axisX.setTickCount(6)  # x轴设置7个刻度
        axisX.setGridLineVisible(False)  # 隐藏从x轴往上的线条

        axisY = self._chart.axisY()
        axisY.setTickCount(6)  # y轴设置7个刻度

        down, up = self.get_pre_index(data)
        # down, up = -20, 50
        axisY.setRange(down, up)  # 设置y轴范围
        # 设置坐标格式
        axisY.setLabelFormat("%0.1f%")
        # 自定义x轴
        axis_x = QCategoryAxis(self._chart, labelsPosition=QCategoryAxis.AxisLabelsPositionOnValue)
        axis_x.setTickCount(len(self.category))
        # axis_x.setGridLineVisible(False)
        min_x = axisX.min()
        max_x = axisX.max()
        # step = (max_x - min_x) / (6 - 1)  # 7个tick

        axis_x.append(self.category[0], min_x)
        axis_x.append(self.category[int(len(self.category) * 0.25)], (max_x - min_x) * 0.25)
        axis_x.append(self.category[int(len(self.category) * 0.5)], (max_x - min_x) * 0.5)
        axis_x.append(self.category[int(len(self.category) * 0.75)], (max_x - min_x) * 0.75)
        axis_x.append(self.category[-1], max_x)

        self._chart.setAxisX(axis_x, self._chart.series()[-1])

        # self._chart.legend(
        # chart的图例
        legend = self._chart.legend()
        # legend.setVisible(False)
        # legend.
        # 设置图例由Series来决定样式
        legend.setMarkerShape(QLegend.MarkerShapeFromSeries)
        # 遍历图例上的标记并绑定信号
        for marker in legend.markers():
            # 隐藏图例
            # marker.setVisible(False)
            # 点击事件
            marker.clicked.connect(self.handleMarkerClicked)
            # 鼠标悬停事件
            marker.hovered.connect(self.handleMarkerHovered)

        self.setChart(self._chart)
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

    def get_pre_index(self, data):
        maxValue = 0
        minValue = 0

        for item in data:
            for i in range(1, len(item)):
                maxValue = max(maxValue, item[i])
                minValue = min(minValue, item[i])
        # TODO 包含0
        print(floor(minValue), ceil(maxValue))
        return self.get_seris_y(floor(minValue), ceil(maxValue))

    def get_seris_y(self, x, y):
        if x >= y:
            x = x + 1
            y = y - 1
        else:
            x = x - 1
            y = y + 1
        x1 = abs(x)
        y1 = abs(y)
        minValue = min(x1, y1)
        maxValue = max(x1, y1)

        if maxValue == x1 and x > 0:
            prefix = 1
        elif maxValue == x1 and x <= 0:
            prefix = -1
        elif maxValue == y1 and y > 0:
            prefix = 1
        else:
            prefix = -1

        comValue = 0
        factor = 0
        sub = ceil((abs(minValue) + abs(maxValue)) / 5)
        for i in range(sub, maxValue):
            mainValue = floor(maxValue / i)
            subValue = maxValue % i
            if mainValue >= 5: continue
            if subValue > 0: mainValue = mainValue + 1
            if (5 - mainValue) * i >= minValue:
                comValue = i
                factor = mainValue
                break
        if prefix > 0:
            x2 = factor * comValue
            y2 = -prefix * (5 - factor) * comValue
        else:
            x2 = prefix * factor * comValue
            y2 = (5 - factor) * comValue
        print(min(x2, y2), max(x2, y2))
        return min(x2, y2), max(x2, y2)

    def resizeEvent(self, event):
        super(ChartView, self).resizeEvent(event)
        # 当窗口大小改变时需要重新计算
        # 坐标系中左上角顶点
        self.point_top = self._chart.mapToPosition(QPointF(self.min_x, self.max_y))
        # 坐标原点坐标
        self.point_bottom = self._chart.mapToPosition(QPointF(self.min_x, self.min_y))

        self.point_bottom_right = self._chart.mapToPosition(QPointF(self.max_x, self.min_y))

        self.step_x = (self.max_x - self.min_x) / (self._chart.axisX().tickCount() - 1)
        self.step_y = (self.max_y - self.min_y) / (self._chart.axisY().tickCount() - 1)

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round((x - self.min_x) / self.step_x)
        indexY = round((y - self.min_y) / self.step_y)

        # 得到在坐标系中的所有正常显示的series的类型和点
        points = [(serie, serie.at(index))
                  for serie in self._chart.series()
                  if self.min_x <= x <= self.max_x and
                  self.min_y <= y <= self.max_y]
        if points:
            pos_x = self._chart.mapToPosition(
                QPointF(index * self.step_x + self.min_x, self.min_y))
            pos_y = self._chart.mapToPosition(
                QPointF(self.min_x, indexY * self.step_y + self.min_y))
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
            self.toolTipWidget.show(title, '{}%', points, QPoint(x, y))
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
    view = ChartView(fundCode='110011', fundName='易方达中小盘混合')
    view.show()
    sys.exit(app.exec_())
