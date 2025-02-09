import multiprocessing
import traceback
from abc import abstractmethod
from sys import stderr
from PyQt5.QtCore import QTimer, QPoint, Qt, QRect
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow, QLabel, QTextEdit, QButtonGroup


def _run_debug(queue: multiprocessing.Queue):
    is_copy = True
    try:
        import pyperclip

    except ImportError:
        is_copy = False

    def messagebox(msg):
        label = QLabel(window)
        label.setText(msg)
        label.setStyleSheet("background-color: #f6f5ea; font-size: 50px; color: black; border: 2px solid #edeef2")
        label.move(0, 0)
        label.raise_()
        label.show()

        QTimer.singleShot(2000, lambda: label.deleteLater())

    message = queue.get()

    clean_text = message["info"].replace('\n', '')

    result = []
    for i in range(0, len(clean_text), 62):
        result.append(clean_text[i:i + 62])

    info = '\n'.join(result)

    app = QApplication([])

    app.setStyleSheet("#menubutton {background: #f2fcf3; font-size: 20px; color: #1bc900; border: 1px solid #409a58;}"
                      "#menubutton:hover {color: red; border: 1px solid red}")

    window = QWidget()
    window.setFixedSize(800, 600)
    window.setStyleSheet("background: #f8f9fb")
    window.setWindowTitle("RUN ERROR")

    label1 = QLabel(window)
    label1.setText("(!) 程序在运行时发生错误")
    label1.setStyleSheet("color: red; font-size: 30px")
    label1.show()

    label2 = QLabel(window)
    label2.setText("错误类型: {}\n错误信息: {}\n在行数: {}".format(
        message["type"], info, message["line"]))
    label2.move(10, 50)
    label2.setStyleSheet("font-size: 20px; color: #DC143C")
    label2.show()
    text_edit = QTextEdit(window)
    text_edit.resize(500, 300)
    text_edit.move(window.width() // 2 - text_edit.width() // 2, window.height() // 2)
    text_edit.setText("详细信息: \n\n" + message["message"])
    text_edit.setStyleSheet("font-size: 20px; color: red; background-color: #f5f8fe; border: 1px solid #edeef2")
    text_edit.setReadOnly(True)
    text_edit.show()

    menu = QPushButton(window)
    menu.resize(55, window.height())
    menu.move(window.width() - menu.width(), 0)
    menu.setStyleSheet("background: #f5f8fe; border: 2px solid #edeef2")
    menu.show()

    mainbutton = QPushButton(window)
    mainbutton.setText("CP")
    mainbutton.resize(47, 47)
    mainbutton.move(menu.x() + (menu.width() - mainbutton.width()) // 2, menu.y())
    mainbutton.setObjectName("menubutton")
    mainbutton.setToolTip("复制错误信息")
    if is_copy:
        mainbutton.clicked.connect(
            lambda: (pyperclip.copy(message["message"]), messagebox("已将错误信息复制到粘贴板！")))
    else:
        mainbutton.setToolTip(mainbutton.toolTip() + "(不可用)")
        mainbutton.clicked.connect(lambda: messagebox("缺少pyperclip库！"))
    mainbutton.show()

    window.show()
    app.exec_()


class Code:
    def __init__(self):
        self.thisWidget: QWidget = ...

    def __and__(self, other):
        if other is True:
            self.thisWidget.show()

        elif other is False:
            self.thisWidget.hide()

        elif isinstance(other, str):
            for i in other.split("||"):
                exec("self.thisWidget.{}".format(i))

        else:
            raise TypeError("No this type")

        return self.thisWidget

    def __enter__(self):
        return self.thisWidget

    def __exit__(self, exc_type, exc_val, exc_tb) -> False:

        self.thisWidget.show()

        return False

    def __rshift__(self, other: str):

        _ = other.split(" ")

        self.thisWidget.move(int(_[0]), int(_[1]))

        return self.thisWidget

    def __getitem__(self, _list: list):

        _list.append(self.thisWidget)

        return self.thisWidget

    def __matmul__(self, other):
        _ = other.split(" ")

        self.thisWidget.resize(int(_[0]), int(_[1]))

        return self.thisWidget

    def __invert__(self):
        self.thisWidget.show()

        return self.thisWidget

    @abstractmethod
    def set_widget(self, widget):
        self.thisWidget = widget


class MainWindow(QMainWindow):
    def __init__(self, title: str = "window"):
        super().__init__()
        super().setWindowTitle(title)


class Button(QPushButton, Code):
    def __init__(self, title: str = "Button", window: QWidget = None):
        super().__init__(window)
        super().setText(title)
        super().hide()
        self.set_widget()

    def set_widget(self):
        super().set_widget(self)

    def link(self, func):
        self.clicked.connect(func)


class Box(QLabel, Code):
    def __init__(self, color="#fff", radius=10, window=None):
        super().__init__(window)
        super().setText("")
        super().setStyleSheet("background: {}; border-radius: {}".format(color, radius))
        self.set_widget()

    def set_widget(self):
        super().set_widget(self)


class CoordinateSystemWidget(QWidget):
    """带独立坐标系的容器组件"""

    def __init__(self, window, alignment=Qt.AlignCenter):
        super().__init__(window)
        self._alignment = alignment
        self._offset = QPoint(0, 0)
        self._update_position()

    def _update_position(self):
        """根据对齐方式更新容器位置"""
        if not self.parent():
            return

        parent_rect = self.parent().rect()
        self.adjustSize()

        # 计算对齐偏移量
        if self._alignment & Qt.AlignLeft:
            x = 0
        elif self._alignment & Qt.AlignRight:
            x = parent_rect.width() - self.width()
        elif self._alignment & Qt.AlignHCenter:
            x = (parent_rect.width() - self.width()) // 2
        else:
            x = self._offset.x()

        if self._alignment & Qt.AlignTop:
            y = 0
        elif self._alignment & Qt.AlignBottom:
            y = parent_rect.height() - self.height()
        elif self._alignment & Qt.AlignVCenter:
            y = (parent_rect.height() - self.height()) // 2
        else:
            y = self._offset.y()

        self.move(x, y)
        self._offset = QPoint(x, y)

    def mapToParentCoordinates(self, x, y):
        """将局部坐标转换为父级坐标系的实际坐标"""
        return QPoint(
            self._offset.x() + x,
            self._offset.y() + y
        )

    def resizeEvent(self, event):
        self._update_position()
        super().resizeEvent(event)


class ButtonGroup(QButtonGroup):
    def __init__(self, window, old_style, new_style):
        super().__init__(window)
        self.old_style = old_style
        self.new_style = new_style
        super().buttonClicked.connect(self.clicked)

    def clicked(self, button):
        for i in self.buttons():
            i.setStyleSheet(self.old_style)

        button.setStyleSheet(self.new_style)

    def add_buttons(self, buttons: list[QWidget]):
        for i in buttons:
            self.addButton(i)


class Container(object):
    def __init__(self, widgets: list[QWidget] = []):
        self.widget = widgets

    def move_x(self, _x):
        for i in self.widget:
            i.move(i.x() + _x, i.y())

    def move_y(self, _y):
        for i in self.widget:
            i.move(i.x(), i.y() + _y)

    def show(self, _y):
        for i in self.widget:
            i.show()

    def hide(self):
        for i in self.widget:
            i.hide()


class APP(QApplication):
    def __init__(self, debug: bool = False):
        self.window: QWidget = ...
        self.debug = debug
        super().__init__([])

    def run(self):
        super().exec_()

    def __enter__(self) -> MainWindow:
        self.window = MainWindow()
        return self.window

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            formatted_tb = traceback.format_exception(exc_type, exc_val, exc_tb)
            if exc_type is SystemExit:
                raise SystemExit(int(str(exc_val)))

            text = ""
            stack = traceback.extract_tb(exc_tb)
            for line in formatted_tb:
                text += line

            if not self.debug:
                print(text, file=stderr)

            else:

                queue = multiprocessing.Queue()

                process = multiprocessing.Process(target=_run_debug, args=(queue,))
                process.daemon = True
                process.start()

                queue.put({"message": text, "type": exc_type.__name__, "info": str(exc_val), "line": stack[-1].lineno})

        self.window.show()
        self.run()

        return True


class SizeBox:
    def __init__(self, widget: QWidget):
        self.button = widget
        self._dragging = False
        self._resize_direction = None
        self.initial_geometry = QRect()
        self._drag_start_global_pos = QPoint()
        self.corner_buttons = {}
        self.create_resize_buttons()

    def create_resize_buttons(self):
        positions = {
            'top_left': (0, 0),
            'top_right': (self.button.width(), 0),
            'bottom_left': (0, self.button.height()),
            'bottom_right': (self.button.width(), self.button.height())
        }

        for name, (x, y) in positions.items():
            btn = QPushButton(self.button.parentWidget())  # Create the button on the same parent widget
            btn.setStyleSheet("background-color: #fff; border-radius: 0px; width: 5px; height: 5px;border: 0.5px solid "
                              "black")
            btn.move(self.button.x() + x - 5, self.button.y() + y - 5)
            btn.setCursor(QCursor(self.get_resize_cursor(name)))

            # Bind events explicitly and pass the button and direction
            btn.mousePressEvent = lambda e, _btn=btn, _name=name: self.on_press(e, _btn, _name)
            btn.mouseMoveEvent = self.on_move
            btn.mouseReleaseEvent = lambda e, _btn=btn: self.on_release(e, _btn)
            self.corner_buttons[name] = btn

    def get_resize_cursor(self, direction):
        cursors = {
            'top_left': Qt.SizeFDiagCursor,
            'top_right': Qt.SizeBDiagCursor,
            'bottom_left': Qt.SizeBDiagCursor,
            'bottom_right': Qt.SizeFDiagCursor
        }
        return cursors[direction]

    def on_press(self, event, button, direction):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._resize_direction = direction
            self.initial_geometry = self.button.geometry()
            self._drag_start_global_pos = event.globalPos()

            # Use the passed button directly
            button.grabMouse()

    def on_move(self, event):
        if self._dragging and self._resize_direction:
            current_global_pos = event.globalPos()
            delta = current_global_pos - self._drag_start_global_pos

            x = self.initial_geometry.x()
            y = self.initial_geometry.y()
            w = self.initial_geometry.width()
            h = self.initial_geometry.height()

            new_geo = self.calculate_new_geometry(x, y, w, h, delta)
            self.button.setGeometry(new_geo)
            self.update_resize_buttons()

    def calculate_new_geometry(self, x, y, w, h, delta):
        direction = self._resize_direction
        new_x, new_y, new_w, new_h = x, y, w, h

        if direction == 'top_left':
            new_w = max(w - delta.x(), 1)
            new_h = max(h - delta.y(), 1)
            new_x = x + (w - new_w)
            new_y = y + (h - new_h)
        elif direction == 'top_right':
            new_w = max(w + delta.x(), 1)
            new_h = max(h - delta.y(), 1)
            new_y = y + (h - new_h)
        elif direction == 'bottom_left':
            new_w = max(w - delta.x(), 1)
            new_h = max(h + delta.y(), 1)
            new_x = x + (w - new_w)
        elif direction == 'bottom_right':
            new_w = max(w + delta.x(), 1)
            new_h = max(h + delta.y(), 1)

        return QRect(new_x, new_y, new_w, new_h)

    def on_release(self, event, button):
        self._dragging = False
        button.releaseMouse()

    def update_resize_buttons(self):
        m = self.button
        self.corner_buttons['top_left'].move(m.x() - 5, m.y() - 5)
        self.corner_buttons['top_left'].raise_()
        self.corner_buttons['top_right'].move(m.x() + m.width() - 5, m.y() - 5)
        self.corner_buttons['top_right'].raise_()
        self.corner_buttons['bottom_left'].move(m.x() - 5, m.y() + m.height() - 5)
        self.corner_buttons['bottom_left'].raise_()
        self.corner_buttons['bottom_right'].move(m.x() + m.width() - 5, m.y() + m.height() - 5)
        self.corner_buttons['bottom_right'].raise_()

    def refresh_position(self):
        """刷新按钮和角部按钮的位置"""
        m = self.button
        self.button.move(m.x(), m.y())
        self.update_resize_buttons()

    def hide(self):
        for i in self.corner_buttons:
            self.corner_buttons[i].hide()

    def show(self):
        for i in self.corner_buttons:
            self.corner_buttons[i].show()

        self.refresh_position()


if __name__ == '__main__':
    with APP(debug=True) as window:
        buttons = []

        for i in range(5):
            Button(window=window)[buttons] >> "0 {}".format(i * 50) & True

        buttongroup = ButtonGroup(window, "", "background: red")
        buttongroup.add_buttons(buttons)

        window.resize(800, 600)
