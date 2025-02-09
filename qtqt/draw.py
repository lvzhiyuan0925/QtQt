import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget

class RectangleWidget(QWidget):
    def __init__(self, window, width, height, color: bool | str = True):
        super().__init__(window)
        self.setGeometry(0, 0, 100, 100)
        self.rect_width = width  # 矩形的宽度
        self.rect_height = height  # 矩形的高度
        self.color = window.palette().color(self.backgroundRole()).name() if color is True else color

    def paintEvent(self, event):
        # 创建QPainter并绘制矩形
        painter = QPainter(self)
        painter.setPen(QColor(self.color))  # 设置矩形边框颜色
        painter.setBrush(QColor(self.color))  # 设置矩形填充颜色
        painter.drawRect(0, 0, self.rect_width, self.rect_height)  # 绘制矩形


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()

    rect = RectangleWidget(window, 100, 100, True)
    rect.move(100, 100)
    rect.show()

    window.show()

    app.exec_()