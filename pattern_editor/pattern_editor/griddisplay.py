import pyglet
import numpy as np

from .control import Control


class GridDisplay(Control):
    h = 512
    pole_w = 5
    light_w = 15

    def resize(self):
        if hasattr(self, 'pole_verticies'):
            del self.pole_verticies
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

        self.pole_verticies = pyglet.graphics.vertex_list(
            8 * 7 * 7, ('v2i\static', verts))
        self.update_grid(self.state)

    def update_grid(self, state):
        self.state = state
        if hasattr(self, 'lit_verticies'):
            del self.lit_verticies
        cw = self.w // 7
        lw = self.light_w
        verts = []
        for xx in range(7):
            for yy in range(7):
                if not state[xx][yy]:
                    continue

                x = self.x + cw/2 + xx * cw
                y = self.y + cw/2 + yy * cw

                verts.extend((x, y))
                angles = np.linspace(0, 2*np.pi, 25)
                xs = x + np.sin(angles) * lw
                ys = y + np.cos(angles) * lw
                vs = np.vstack((xs, ys)).T.reshape((-1))
                verts.extend(vs.tolist())
        self.lit_verticies = pyglet.graphics.vertex_list(
            len(verts)//2, ('v2f\static', verts))

    def draw(self):
        self.pole_verticies.draw(pyglet.gl.GL_LINES)
        self.lit_verticies.draw(pyglet.gl.GL_TRIANGLE_FAN)
