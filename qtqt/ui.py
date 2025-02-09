from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget


class ResponseArea(QWidget):
    def __init__(self, window=None):
        super().__init__(window)
        self.interval = 2
        self.widget_interval = 5

        self.__widgets: list[QWidget] = []

    def add_widget(self, widget: QWidget) -> None:
        x = self.x() + self.interval
        y = self.y() + self.interval

        for i in self.__widgets:
            x += i.width() + self.widget_interval

            if x + widget.width() > self.x() + self.width() - self.interval:
                x = self.x() + self.interval
                y += max(i.height(), widget.height()) + self.widget_interval

        widget.move(x, y)
        self.__widgets.append(widget)

    def add_widgets(self, widgets: list[QWidget]) -> None:
        for i in widgets:
            self.add_widget(i)

    def refresh_widgets(self) -> None:
        x = self.x() + self.interval
        y = self.y() + self.interval

        for i in self.__widgets:
            i.move(x, y)
            x += i.width() + self.widget_interval

            if x + i.width() > self.x() + self.width() - self.interval:
                x = self.x() + self.interval
                y += i.height() + self.widget_interval

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.refresh_widgets()

    def moveEvent(self, a0):
        super().moveEvent(a0)
        self.refresh_widgets()


class Responsive:

    def __init__(self, window: QWidget):
        self.window = window
        self.widgets: dict = {}

    def responsive(self) -> None:
        """
        按照add_widget的参数进行响应式布局
        """

        for widget in self.widgets:
            # widget: QWidget = widget
            x: tuple = self.widgets[widget]["x"]
            y: tuple = self.widgets[widget]["y"]
            w: int = self.widgets[widget]["w"]
            h: int = self.widgets[widget]["h"]

            if x is not None:
                if x[1] == "L":  # LEFT
                    widget.move(x[0], widget.y())

                elif x[1] == "R":  # RIGHT
                    widget.move(self.window.width()-widget.width()-x[0], widget.y())

            if y is not None:
                if y[1] == "T":  # TOP
                    widget.move(widget.x(), y[0])

                elif y[1] == "D":  # DOWN
                    widget.move(widget.x(), self.window.height()+widget.height()+y[0])

            if w is not None:
                widget.resize(self.window.width() - widget.x() - w, widget.height())

            if h is not None:
                widget.resize(widget.width(), self.window.height() - widget.y() - h)

    def add_widget(self, widget: QWidget, x: tuple[int, str] | None = None, y: tuple[int, str] | None = None,
                   w: int | None = None, h: int | None = None) -> None:
        """
        添加响应式布局组件
        :param widget: 组件
        :param x: 响应x坐标
        :param y: 响应y坐标
        :param w: 响应width宽度
        :param h: 响应height长度
        """

        self.widgets[widget] = {"x": x, "y": y, "w": w, "h": h}


class UITool:
    def __init__(self, widget: QWidget, window: QWidget):
        self.widget = widget
        self.window = window
        self.is_drag = False
        self.drag_func = lambda: None
        self.drag_func_start = lambda: None

        self.__dragging = False
        self.__on_top = False
        self.__drag_offset = ...
        self.__original_mousePressEvent = self.widget.mousePressEvent
        self.__original_mouseMoveEvent = self.widget.mouseMoveEvent
        self.__original_mouseReleaseEvent = self.widget.mouseReleaseEvent

    def enlarge(self, w: int, h: int) -> None:
        if w % 2 != 0 or h % 2 != 0:
            raise ValueError("Parameter must be divisible by 2")

        self.widget.move(self.widget.x()-w // 2, self.widget.y()-h // 2)
        self.widget.resize(self.widget.width()+w, self.widget.height()+h)

    def narrow(self, w: int, h: int) -> None:
        if w % 2 != 0 or h % 2 != 0:
            raise ValueError("Parameter must be divisible by 2")

        self.widget.move(self.widget.x()+w // 2, self.widget.y()+h // 2)
        self.widget.resize(self.widget.width()-w, self.widget.height()-h)

    def drag_widget(self, _bool: bool, on_top: bool = True):
        self.is_drag = _bool
        self.__on_top = on_top
        self.widget.mousePressEvent = self.mousePressEvent if _bool else self.__original_mousePressEvent
        self.widget.mouseMoveEvent = self.mouseMoveEvent if _bool else self.__original_mouseMoveEvent
        self.widget.mouseReleaseEvent = self.mouseReleaseEvent if _bool else self.__original_mouseReleaseEvent

    def set_drag_end(self, func) -> "UITool":
        self.drag_func = func
        return self

    def set_drag_start(self, func) -> "UITool":
        self.drag_func_start = func
        return self

    def mousePressEvent(self, event):
        self.__original_mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.widget.raise_() if self.__on_top else None
            self.drag_func_start()
            self.__dragging = True
            self.__drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        self.__original_mouseMoveEvent(event)
        if self.__dragging:
            old_pos = event.globalPos()
            pos = self.window.mapFromGlobal(old_pos)-self.__drag_offset
            pos.setX(max(0, min(pos.x(), self.window.width()-self.widget.width())))
            pos.setY(max(0, min(pos.y(), self.window.height()-self.widget.height())))

            self.widget.move(pos)

    def mouseReleaseEvent(self, event):
        self.__original_mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.__dragging = False
            self.drag_func()

    def independent_coordinates(self, x, y):
        pos = self.widget.parent_widget.mapToGlobal(QPoint(0, 0))
        window_x = pos.x() + x
        window_y = pos.y() + y
        return window_x, window_y


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from widgets import Button

    app = QApplication([])

    window = QWidget()
    ui = Responsive(window)
    window.resize(900, 600)
    buttons = []
    area = ResponseArea(window)
    for _i in range(30):
        UITool(Button(title="button", window=window)[buttons] @ "100 100" & True, window).drag_widget(True)

    ui.add_widget(area, (25, "L"), (25, "T"), 25, 25)
    ui.responsive()
    area.add_widgets(buttons)

    window.resizeEvent = lambda e: ui.responsive()

    window.show()

    app.exec_()
