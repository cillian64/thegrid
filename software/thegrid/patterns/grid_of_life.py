# Game of life pattern (by hark originally, dirty hacks by David Turner)


import numpy as np
from ..pattern import Pattern, register_pattern

grid_size = 7


@register_pattern("[MONOCHROME] Game of Life: Glider",
                  {'colour': False, 'pattern': 'glider'})
@register_pattern("[MONOCHROME] Game of Life",
                  {'colour': False, 'pattern': 'random'})
@register_pattern("[COLOUR] Game of Life: Glider",
                  {'colour': True, 'pattern': 'glider'})
@register_pattern("[COLOUR] Game of Life",
                  {'colour': True, 'pattern': 'random'})
class PatternColourwheel(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator(cfg)

    def generator(self, cfg):
        cells = np.zeros((7, 7, 1), dtype=np.bool)
        next_cells = np.zeros((7, 7, 1), dtype=np.bool)
        lights = np.zeros((7, 7, 6), dtype=np.uint8)

        # Frames per second
        fps = 30
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

        lights[:, :, :3] = cells * cell_colours
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

            if cfg['pattern'].lower() == 'random':
                if self.is_boring(cells):
                    # If the pattern is not extinction, hold it for a few
                    # updates of appreciation and then fade it out.
                    if np.sum(cells) != 0:
                            # Hold for a few updates
                            yield lights, 1.0/ups*3
                            # Now fade out.
                            frames = fps*ups*3
                            for i in range(fps*ups*3):
                                cur = 1 - i/frames
                                lights[:, :, :3] = cells * cell_colours * cur
                                yield lights, 1/fps

                    # Give a few updates of black to divide:
                    yield np.zeros((7, 7, 3), dtype=np.uint8), 1.0/ups*3

                    # Reinitialise!
                    cells[:, :] = 0
                    next_cells[:, :] = np.random.randint(0, 2, (7, 7, 1))
                    has_died[:, :] = True

            frames = fps*ups
            for i in range(frames):
                # We are fading between lights and next_cells*cell_colours
                # with respective weighting cur, new
                cur = 1 - i/frames
                new = i/frames
                lights[:, :, :3] = (cells * cell_colours * cur +
                                   next_cells * cell_colours * new)
                for x in range(7):
                    for y in range(7):
                        lights[x, y, 3] = 1 # sine
                        # If we're fading up, make a happy coming-to-life sound
                        if next_cells[x, y] and not cells[x, y]:
                            lights[x, y, 4] = 120 # higher freq
                            lights[x, y, 5] = 200 # vol
                        # if we're fading down, make a sad dying noise
                        elif not next_cells[x, y] and cells[x, y]:
                            lights[x, y, 4] = 80 # higher freq
                            lights[x, y, 5] = 200 # vol
                        else:
                            lights[x, y, 5] = 0 # vol
                yield lights, 1/fps
            cells[:] = next_cells
            if cfg['colour']:
                cell_colours[has_died] = np.random.randint(0, 255,
                    (np.sum(has_died), 3))
                has_died[:, :] = False


    def update(self):
        return self.gen.__next__()


    def is_boring(self, cells):
        """Decide if the current configuration is boring enough to trigger
        a reset.  We do this using a buffer of the previous N cells
        states.  If the current state is equal to any of the previous N
        states, the current system is oscillating with a period of less
        than N.  This implicitly detects extinction.  We also include
        a total life timer of T to catch possible long, boring,
        oscillations or unexpected mishaps (like a glider!)"""

        # We don't need to worry about checking against the buffer before it
        # is full, because empty buffer slots are all zeros, and all zeros is
        # a good sign of boringness.

        N = 5 # State change buffer
        T = 60 # State change life timer

        if not hasattr(self, 'buffer'):
                self.buffer = np.zeros((N, 7, 7), dtype=np.uint8)
        if not hasattr(self, 'ttl'):
                self.ttl = T

        if self.ttl == 0:
            print("Resetting due to age limit")
            self.ttl = T
            self.buffer = np.zeros((N, 7, 7), dtype=np.uint8)
            return True # Boring due to age
        else:
            self.ttl -= 1

        # Don't know why I can't do 'if cells[:, :, 0] in self.buffer' here
        for buf in self.buffer:
            if np.allclose(cells[:, :, 0], buf):
                print("Resetting because of oscillation or extinction")
                self.ttl = T
                self.buffer = np.zeros((N, 7, 7), dtype=np.uint8)
                return True # Boring due to oscillation

        self.buffer[:, :, :] = np.roll(self.buffer, 1, 0)
        self.buffer[0, :, :] = cells[:, :, 0]  # implicit copy

        return False # Not boring!
