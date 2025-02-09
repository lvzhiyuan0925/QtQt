import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton
from qframelesswindow import AcrylicWindow


class Blur(AcrylicWindow):
    """ 磨砂效果的实现 """

    def __init__(self, width: int | None = None, color: str = "#fff"):
        super().__init__()

        self.canvas_width = width
        self.color = color
        self.resize_event = lambda event: None

        if self.canvas_width is not None:
            self.canvas = QLabel(self)
            self.canvas.setStyleSheet("background: {}".format(self.color))
            self.canvas.resize(self.width() - self.canvas_width, self.height())
            self.canvas.move(self.canvas_width, 0)
            self.canvas.lower()
            self.canvas.show()

        self.titleBar.raise_()

    @staticmethod
    def app():
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        return QApplication([])

    def resizeEvent(self, event):
        self.resize_event(event)
        if self.canvas_width is not None:
            self.canvas.deleteLater()
            self.canvas = QLabel(self)
            self.canvas.setStyleSheet("background: {}".format(self.color))
            self.canvas.resize(self.width() - self.canvas_width, self.height())
            self.canvas.move(self.canvas_width, 0)
            self.canvas.lower()
            self.canvas.show()
        super().resizeEvent(event)


if __name__ == "__main__":

    class MyAPP(Blur):
        def __init__(self):
            super().__init__(55, "#fff")
            self.resize(800, 600)

    app = Blur.app()
    window = MyAPP()

    window.show()
    sys.exit(app.exec_())
