import pyglet


class Control(pyglet.event.EventDispatcher):
    x = y = 0
    w = h = 0

    def __init__(self, parent):
        self.parent = parent
        super(Control, self).__init__()

    def draw(self):
        pass

    def resize(self):
        pass
