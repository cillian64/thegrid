import pyglet


class Control(pyglet.event.EventDispatcher):
    """Base class for things that get drawn and interacted with on the GUI."""
    x = y = 0
    w = h = 0

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super(Control, self).__init__()

    def draw(self):
        pass

    def resize(self):
        pass

    def set_time(self, t):
        pass

    def set_times(self, start, end):
        pass

    def __point_inside(self, x, y):
        if self.x <= x <= self.x + self.w:
            if self.y <= y <= self.y + self.h:
                return True
        return False

    def check_mousepress(self, x, y, btn, mod):
        if self.__point_inside(x, y):
            self.mousepress(x - self.x, y - self.y, btn, mod)

    def check_mousedrag(self, x, y, dx, dy, btns, mod):
        if self.__point_inside(x, y):
            self.mousedrag(x - self.x, y - self.y, dx, dy, btns, mod)

    def mousepress(self, x, y, btn, mod):
        pass

    def mousedrag(self, x, y, dx, dy, btns, mod):
        pass
