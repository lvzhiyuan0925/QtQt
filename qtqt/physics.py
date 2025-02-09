from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from time import sleep


class Physics(QThread):
    def __init__(self, widget: QWidget, window: QWidget):
        super().__init__()
        self.widget = widget
        self.speed = 1
        self.direction = "v"
        self.window = window

    def vertical(self, speed: int):
        self.speed = speed
        self.direction = "v"

    def run(self):
        while True:
            if self.widget.y() > self.window.height() + 10:
                #self.widget.deleteLater() if is_del else None
                break

            if self.direction == "v":
                print(1)
                #self.widget.move(self.widget.x(), self.widget.y()+self.speed)
                sleep(0.05)

            else:
                raise TypeError


if __name__ == '__main__':
    app = QApplication([])

    window = QWidget()
    window.resize(800, 600)

    button = QPushButton(window)
    button.setText("测试")
    button.show()
    physics = Physics(button, window)
    physics.vertical(1)
    physics.run()
    physics.start()

    window.show()

    app.exec_()
