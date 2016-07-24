# Game of life pattern (hark)


import numpy as np
from .pattern import Pattern, register_pattern

grid_size = 7


@register_pattern("GridOfLife")
class PatternColourwheel(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        cells = np.zeros((7, 7), dtype=np.bool)
        next_cells = np.zeros((7, 7), dtype=np.bool)
        lights = np.zeros((7, 7, 3), dtype=np.uint8)

        # Frames per second
        fps = 10
        # Updates per second
        ups = 1

        def neighbours(px, py):
            total = 0
            for ox in [-1, 0, 1]:
                for oy in [-1, 0, 1]:
                    if ox == 0 and oy == 0:
                        continue
                    total += cells[(px + ox) % 7][(py + oy) % 7]
            return total

        cells[2, 3] = True
        cells[3, 4] = True
        cells[4, 2:5] = True

        lights[:, :, 0] = cells * 255
        lights[:, :, 1] = cells * 255
        lights[:, :, 2] = cells * 255
        yield lights, 1.

        while True:
            for x in range(7):
                for y in range(7):
                    n = neighbours(x, y)
                    if cells[x][y]:
                        next_cells[x][y] = (n in [2, 3])
                    else:
                        next_cells[x][y] = (n == 3)
            frames = fps*ups
            for i in range(frames):
                cur = 1 - i/frames
                new = i/frames
                lights[:, :, 0] = cells * 255 * cur + next_cells * 255 * new
                lights[:, :, 1] = cells * 255 * cur + next_cells * 255 * new
                lights[:, :, 2] = cells * 255 * cur + next_cells * 255 * new
                yield lights, 1/fps
            cells[:] = next_cells

    def update(self):
        return self.gen.__next__()
