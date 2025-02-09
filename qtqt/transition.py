from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsOpacityEffect
try:
    from .tools.pos import generate_trajectory_with_step
except ImportError:
    from tools.pos import generate_trajectory_with_step


class Transition:
    """
    注意：此类的所有方法均在子线程运行，并没有前后顺序
    所有指针参数参见：https://docs.python.org/zh-cn/3.13/library/copy.html
    """
    def __init__(self, widget: QWidget, window):
        self.widget = widget
        self.window = window
        self.__is_h_run = False
        self.__is_s_run = False

    def show_floating(self, speed=50, offset=40, run=10):
        """
        :param speed: 初始速率
        :param offset: 上下偏移量
        :param run: 动画的步数
        """
        opacity_effect = QGraphicsOpacityEffect(self.widget)
        opacity_effect.setOpacity(0.0)  # 初始透明度为0
        self.widget.setGraphicsEffect(opacity_effect)

        # 计算每次移动的步长
        step_offset = int(offset / run)  # 强制转换为整数
        step_opacity = 1.0 / run  # 透明度每步增加的量

        i = 0

        def update():
            nonlocal i
            if i < run:
                # 更新透明度，确保其在0.0到1.0之间
                new_opacity = round(opacity_effect.opacity() + step_opacity, 2)
                opacity_effect.setOpacity(min(new_opacity, 1.0))  # 确保透明度不超过1
                self.widget.setGraphicsEffect(opacity_effect)

                # 更新位置
                self.widget.move(self.widget.x(), self.widget.y() - step_offset)

                i += 1
            else:
                # 动画完成
                timer.stop()

        # 初始位置设置为下方
        self.widget.move(self.widget.x(), self.widget.y() + offset)
        self.widget.show()

        timer = QTimer(self.window)
        timer.setInterval(speed)
        timer.timeout.connect(update)
        timer.start()

    def show_floating_left(self, speed=50, offset=40, run=10):
        """
        :param speed: 初始速率
        :param offset: 左右偏移量
        :param run: 动画的步数
        """
        opacity_effect = QGraphicsOpacityEffect(self.widget)
        opacity_effect.setOpacity(0.0)  # 初始透明度为0
        self.widget.setGraphicsEffect(opacity_effect)

        # 计算每次移动的步长
        step_offset = int(offset / run)  # 强制转换为整数
        step_opacity = 1.0 / run  # 透明度每步增加的量

        i = 0

        def update():
            nonlocal i
            if i < run:
                # 更新透明度，确保其在0.0到1.0之间
                new_opacity = round(opacity_effect.opacity() + step_opacity, 2)
                opacity_effect.setOpacity(min(new_opacity, 1.0))  # 确保透明度不超过1
                self.widget.setGraphicsEffect(opacity_effect)

                # 更新位置（向右移动）
                self.widget.move(self.widget.x() + step_offset, self.widget.y())

                i += 1
            else:
                # 动画完成
                timer.stop()

        # 初始位置设置为左侧
        self.widget.move(self.widget.x() - offset, self.widget.y())
        self.widget.show()

        timer = QTimer(self.window)
        timer.setInterval(speed)
        timer.timeout.connect(update)
        timer.start()

    def hide_down(self, delete=False, sp=50, acceleration: int | float = 10, gravity=10, _is_ok: list[bool] = [False]):
        """
        :param delete: 是否在完成时删除组件
        :param sp: 初始速率
        :param acceleration: 重力加速度
        :param gravity: 初始重力
        :param _is_ok: 动画是否完成（引用）
        """
        if self.__is_h_run:
            return

        self.__is_h_run = True
        i = 0

        def update():
            nonlocal i, gravity, _is_ok
            i += 1
            if i <= 10:
                timer.setInterval(35)
                self.widget.move(x, self.widget.y()-(10-i))

            else:
                timer.setInterval(sp)
                if self.widget.y() >= self.window.height():
                    self.widget.hide() if not delete else self.widget.deleteLater()
                    self.widget.move(x, y)
                    _is_ok[0] = True
                    self.__is_h_run = False
                    timer.stop()

                else:
                    self.widget.move(x, self.widget.y()+int(gravity))
                    gravity += acceleration

        x, y = self.widget.x(), self.widget.y()
        timer = QTimer(self.window)
        timer.timeout.connect(update)
        timer.start()

    def TypeWriterEffect(self, text: str, speed=30, _is_ok: list[bool] = [False]):
        i = 1

        def update():
            nonlocal i
            if i != len(text)+1:
                self.widget.setText(text[:i])
                i += 1

            else:
                timer.stop()
                _is_ok[0] = True

        timer = QTimer(self.window)
        timer.setInterval(speed)
        timer.timeout.connect(update)
        timer.start()

    def smooth_movement(self, x, y, step=3, speed=50, _is_ok: list[bool] = [False]):
        if self.__is_s_run is True:
            return
        self.__is_s_run = True
        pos = generate_trajectory_with_step(self.widget.x(), self.widget.y(), x, y, step)
        i = 0

        def update():
            nonlocal i, pos
            if len(pos) <= i:
                timer.stop()
                self.__is_s_run = False

            else:
                self.widget.move(pos[i][0], pos[i][1])
                i += 1

        timer = QTimer(self.window)
        timer.setInterval(speed)
        timer.timeout.connect(update)
        timer.start()


if __name__ == '__main__':
    app = QApplication([])

    is_ok = [False]

    window = QWidget()
    window.resize(800, 600)

    button = QPushButton(window)
    button.move(200, 200)
    button.resize(200, 200)
    button.hide()
    t = Transition(button, window)
    t.show_floating(20, 10)
    t.TypeWriterEffect("测试按钮\n请点击我\n(喵喵喵喵喵喵~)", speed=100)
    button.clicked.connect(lambda: t.hide_down(gravity=1, acceleration=0.1, sp=5, _is_ok=is_ok))

    is_ok_timer = QTimer(window)
    is_ok_timer.setInterval(100)
    is_ok_timer.timeout.connect(lambda: (print("动画完成！"), is_ok_timer.stop()) if is_ok[0] else None)
    is_ok_timer.start()

    window.show()

    app.exec_()
