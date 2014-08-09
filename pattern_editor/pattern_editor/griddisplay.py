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
    n_angles = 20

    def __init__(self, *args, **kwargs):
        super(GridDisplay, self).__init__(*args, **kwargs)
        self.state = np.zeros((7, 7), dtype=np.bool)
        self.pole_verticies = pyglet.graphics.vertex_list(0, 'v2f')
        self.light_verticies = pyglet.graphics.vertex_list(0, 'v2f', 'c3B')
        self.light_colours = np.zeros(self.n_angles*3*3*7*7, dtype=np.uint8)

    def resize(self):
        self.compute_poles()
        self.compute_lights()
        self.compute_lit()

    def compute_poles(self):
        cw = self.w // 7
        pw = self.pole_w / 2

        xs = (self.x + cw/2 + cw * np.arange(7.0)).repeat(8)
        ys = (self.y + cw/2 + cw * np.arange(7.0)).repeat(8)
        xs = np.repeat(xs, 7)
        ys = np.tile(ys, 7)
        dxs = np.tile([-pw, pw, pw, pw, pw, -pw, -pw, -pw], 7*7)
        dys = np.tile([pw, pw, pw, -pw, -pw, -pw, -pw, pw], 7*7)
        vs = np.vstack((xs + dxs, ys + dys)).T.reshape((-1))

        self.pole_verticies.delete()
        self.pole_verticies = pyglet.graphics.vertex_list(
            vs.size//2, ('v2f\static', vs))

    def compute_lights(self):
        cw = self.w // 7

        xs = (self.x + cw/2 + cw * np.arange(7.0)).repeat(3*self.n_angles)
        ys = (self.y + cw/2 + cw * np.arange(7.0)).repeat(3*self.n_angles)
        xs = np.repeat(xs, 7)
        ys = np.tile(ys, 7)

        angles = np.linspace(0, 2*np.pi, self.n_angles)
        dxs = np.sin(angles) * self.light_w
        dys = np.cos(angles) * self.light_w

        z = np.zeros(self.n_angles)

        ddxs = np.vstack((z, dxs, np.roll(dxs, 1))).T.reshape((-1))
        ddys = np.vstack((z, dys, np.roll(dys, 1))).T.reshape((-1))

        vs = np.vstack((xs + np.tile(ddxs, 49), ys + np.tile(ddys, 49)))
        vs = vs.T.reshape((-1))

        self.light_verticies.delete()
        self.light_verticies = pyglet.graphics.vertex_list(
            vs.size//2, ('v2f\static', vs), ('c3B', self.light_colours))

    def compute_lit(self):
        lit = self.state.reshape((-1)).repeat(3*self.n_angles*3)
        whites = np.array((255, 255, 255), np.uint8).repeat(self.n_angles*147)
        self.light_colours = whites * lit
        self.light_verticies.colors = self.light_colours

    def draw(self):
        self.light_verticies.draw(pyglet.gl.GL_TRIANGLES)
        self.pole_verticies.draw(pyglet.gl.GL_LINES)

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
        if 0 <= xx <= 6 and 0 <= yy <= 6:
            self.state[xx][yy] = True
            na = self.n_angles
            idx = xx*(7*3*3*na) + yy*(3*3*na)
            whites = np.array((255, 255, 255), np.uint8).repeat(na * 3)
            self.light_colours[idx:idx+(3*3*na)] = whites
            self.light_verticies.colors[idx:idx+(3*3*na)] = whites

    def turnoff(self, xx, yy):
        if 0 <= xx <= 6 and 0 <= yy <= 6:
            self.state[xx][yy] = False
            na = self.n_angles
            idx = xx*(7*3*3*na) + yy*(3*3*na)
            offs = np.array((0, 0, 0), np.uint8).repeat(na * 3)
            self.light_colours[idx:idx+(3*3*na)] = offs
            self.light_verticies.colors[idx:idx+(3*3*na)] = offs

    def blanking(self, mod):
        if mod & pyglet.window.key.MOD_SHIFT:
            self.state = np.ones((7, 7), dtype=np.bool)
            self.compute_lit()
        else:
            self.state = np.zeros((7, 7), dtype=np.bool)
            self.compute_lit()
