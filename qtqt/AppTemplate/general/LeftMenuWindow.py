from ...style import Blur
from ...widgets import Button, ButtonGroup


class MainAPP(Blur):
    def __init__(self, width=55):
        self.APP = Blur.app()
        self._width = width
        super().__init__(self._width, "#fff")
        self.resize(800, 600)


class LMenuButton(Button):

    def __init__(self, window: MainAPP):
        global y, buttongroup

        super().__init__(window=window)
        super().resize(45, 45)
        super().setStyleSheet("background: transparent; border: 1.5px solid #dddddd;border-radius: 5px;")

        try:
            buttongroup.addButton(self)
        except NameError:
            buttongroup = ButtonGroup(window, self.styleSheet(), self.styleSheet()+"background: #fff;"
                                      "border: 1.2px solid #e0e0e0")
            buttongroup.addButton(self)

        try:
            y += self.height() + 5
        except NameError:
            y = 10
        super().move(window._width // 2-self.width() // 2, y)
