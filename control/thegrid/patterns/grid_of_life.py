# Game of life pattern (hark)


import numpy as np
from .pattern import Pattern, register_pattern

grid_size = 7


@register_pattern("Life_WhiteGlider", {'colour': False, 'pattern': 'glider'})
@register_pattern("Life_WhiteRandom", {'colour': False, 'pattern': 'random'})
@register_pattern("Life_ColourRandom", {'colour': True, 'pattern': 'random'})
class PatternColourwheel(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator(cfg)

    def generator(self, cfg):
        cells = np.zeros((7, 7, 1), dtype=np.bool)
        next_cells = np.zeros((7, 7, 1), dtype=np.bool)
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

        # Initial setup:
        if cfg['pattern'].lower() == 'glider':
            cells[2, 3] = True
            cells[3, 4] = True
            cells[4, 2:5] = True
        elif cfg['pattern'].lower() == 'random':
            cells[:, :, 0] = np.random.randint(0, 2, (7, 7))

        # We do colours by maintaining memory of the colour of each cell,
        # even when it has yet to be born.  Each time a cell dies we reset
        # its colour to a random one so if it is reborn it comes back as
        # a new colour!
        # In white mode we just leave all the cells as white.
        if cfg['colour']:
            cell_colours = np.random.randint(0, 255, (7, 7, 3))
        else:
            cell_colours = np.zeros((7, 7, 3), dtype=np.uint8)
            cell_colours[:, :, :] = 255

        lights = cells * cell_colours
        yield lights, 1.0 / ups

        # Remember which cells died in each iteration so we can change their
        # colour once fading completes.
        has_died = np.zeros((7, 7), dtype=np.bool)

        while True:
            for x in range(7):
                for y in range(7):
                    n = neighbours(x, y)
                    if cells[x][y]:
                        next_cells[x][y] = (n in [2, 3])
                        has_died[x, y] = (n not in [2, 3])
                    else:
                        next_cells[x][y] = (n == 3)

            frames = fps*ups
            for i in range(frames):
                # We are fading between lights and next_cells*cell_colours
                # with respective weighting cur, new
                cur = 1 - i/frames
                new = i/frames
                lights[:, :, :] = (cells * cell_colours * cur +
                                   next_cells * cell_colours * new)
                yield lights, 1/fps
            cells[:] = next_cells
            if cfg['colour']:
                cell_colours[has_died] = np.random.randint(0, 255,
                    (np.sum(has_died), 3))

    def update(self):
        return self.gen.__next__()
