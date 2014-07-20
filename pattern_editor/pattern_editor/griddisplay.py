import pyglet
import numpy as np

from .control import Control


class GridDisplay(Control):
    """
    Display current state of the grid lights.
    Click to edit current frame.
    """
    h = 512
    pole_w = 5
    light_w = 15

    def __init__(self, *args, **kwarsg):
        self.pole_verticies = pyglet.graphics.vertex_list(0, ('v2f', []))
        self.lit_verticies = pyglet.graphics.vertex_list(0, ('v2f', []))

    def resize(self):
        self.compute_grid()
        self.compute_lit()

    def compute_grid(self):
        cw = self.w // 7
        pw = self.pole_w
        verts = []
        for xx in range(7):
            for yy in range(7):
                x = self.x + cw//2 + xx * cw
                y = self.y + cw//2 + yy * cw

                verts.extend((x, y))
                verts.extend((x+pw, y))

                verts.extend((x+pw, y))
                verts.extend((x+pw, y+pw))

                verts.extend((x+pw, y+pw))
                verts.extend((x, y+pw))

                verts.extend((x, y+pw))
                verts.extend((x, y))

        self.pole_verticies.delete()
        self.pole_verticies = pyglet.graphics.vertex_list(
            8 * 7 * 7, ('v2i\static', verts))

    def compute_lit(self):
        cw = self.w // 7
        lw = self.light_w
        verts = []
        for xx in range(7):
            for yy in range(7):
                if not self.state[xx][yy]:
                    continue

                x = np.repeat([self.x + cw/2 + xx * cw], 25)
                y = np.repeat([self.y + cw/2 + yy * cw], 25)
                angles = np.linspace(0, 2*np.pi, 25)
                xs = x + np.sin(angles) * lw
                ys = y + np.cos(angles) * lw
                vs = np.vstack((x, y, xs, ys, np.roll(xs, 1), np.roll(ys, 1)))
                vs = vs.T.reshape((-1))

                verts.extend(vs.tolist())
        self.lit_verticies.delete()
        self.lit_verticies = pyglet.graphics.vertex_list(
            len(verts)//2, ('v2f\static', verts))

    def draw(self):
        self.pole_verticies.draw(pyglet.gl.GL_LINES)
        self.lit_verticies.draw(pyglet.gl.GL_TRIANGLES)

    def mousepress(self, x, y, btn, mod):
        if btn == pyglet.window.mouse.LEFT:
            self.turnon(*self.polefrompos(x, y))
        if btn == pyglet.window.mouse.RIGHT:
            self.turnoff(*self.polefrompos(x, y))

    def mousedrag(self, x, y, dx, dy, btn, mod):
        if btn == pyglet.window.mouse.LEFT:
            self.turnon(*self.polefrompos(x, y))
        if btn == pyglet.window.mouse.RIGHT:
            self.turnoff(*self.polefrompos(x, y))

    def polefrompos(self, x, y):
        cw = self.w // 7
        return x // cw, y // cw

    def turnon(self, xx, yy):
        self.state[xx][yy] = True
        self.compute_lit()

    def turnoff(self, xx, yy):
        self.state[xx][yy] = False
        self.compute_lit()

    def blanking(self, mod):
        if mod & pyglet.window.key.MOD_SHIFT:
            self.state = np.ones((7, 7), dtype=np.bool)
            self.compute_lit()
        else:
            self.state = np.zeros((7, 7), dtype=np.bool)
            self.compute_lit()
