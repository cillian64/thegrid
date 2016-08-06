# Radar patterns with static targets and moving targets

import numpy as np
from ..pattern import Pattern, register_pattern

grid_size = 7

@register_pattern("[COLOUR] Radar (Static)")
class PatternRadarStatic(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        lights = np.zeros((7, 7, 6), dtype=np.uint8)
        lights[:, :, 3] = 1 # sine
        lights[:, :, 4] = 100 # freq
        targets = [(1, 1), (5, 5)]
        beam_angle = 0.0

        empty_decay_rate = 20
        target_decay_rate = int(empty_decay_rate / 4)

        while True:
            for x in range(7):
                for y in range(7):
                    # Draw the beam sweep:
                    angle = np.arctan2((y - 3.0), (x - 3.0)) + np.pi
                    lag = beam_angle - angle
                    if lag < 0:
                        lag += 2*np.pi
                    if lag < 2*np.pi*10/360:
                        if (x, y) in targets:
                            lights[y, x, 1] = 255.0
                            lights[y, x, 5] = 200
                        else:
                            lights[y, x, 1] = 150.0

                    if (x, y) in targets:
                        decay_rate = target_decay_rate
                    else:
                        decay_rate = empty_decay_rate

                    if lights[y, x, 1] >= decay_rate:
                        lights[y, x, 1] -= decay_rate
                    else:
                        lights[y, x, 1] = 0
                    if lights[y, x, 5] > empty_decay_rate:
                        lights[y, x, 5] -= empty_decay_rate
                    else:
                        lights[y, x, 5] = 0

                    if lights[y, x, 1] > 200:
                        q = lights[y, x, 1] - 200
                        q *= 2
                        lights[y, x, 0] = q
                        lights[y, x, 2] = q
                    else:
                        lights[y, x, 0] = 0
                        lights[y, x, 2] = 0

            lights[3, 3, 1] = 255
            yield lights, 0.03
            beam_angle += 0.1 # Sweep speed
            if beam_angle > 2*np.pi:
                beam_angle -= 2*np.pi

    def update(self):
        return self.gen.__next__()

@register_pattern("[COLOUR] Radar (Moving)")
class PatternRadarMoving(Pattern):
    def __init__(self, cfg, tracking):
        self.gen = self.generator()

    def generator(self):
        lights = np.zeros((7,7, 6), dtype=np.uint8)
        lights[:, :, 3] = 1 # sine
        lights[:, :, 4] = 100 # freq
        target = [-1, -1]
        target_velocity = [0.01, 0.01]
        beam_angle = 0.0

        empty_decay_rate = 20
        target_decay_rate = int(empty_decay_rate / 4)

        while True:
            for x in range(7):
                for y in range(7):
                    # Draw the beam sweep:
                    angle = np.arctan2((y - 3.0), (x - 3.0)) + np.pi
                    lag = beam_angle - angle
                    if lag < 0:
                        lag += 2*np.pi
                    if lag < 2*np.pi*10/360:
                        if [x, y] == [round(x) for x in target]:
                            lights[y, x, 1] = 255.0
                            lights[y, x, 5] = 200
                        else:
                            lights[y, x, 1] = 150.0

                    if [x, y] == [round(x) for x in target]:
                        decay_rate = target_decay_rate
                    else:
                        decay_rate = empty_decay_rate

                    if lights[y, x, 1] >= decay_rate:
                        lights[y, x, 1] -= decay_rate
                    else:
                        lights[y, x, 1] = 0
                    if lights[y, x, 5] > empty_decay_rate:
                        lights[y, x, 5] -= empty_decay_rate
                    else:
                        lights[y, x, 5] = 0

                    if lights[y, x, 1] > 200:
                        q = lights[y, x, 1] - 200
                        q *= 2
                        lights[y, x, 0] = q
                        lights[y, x, 2] = q
                    else:
                        lights[y, x, 0] = 0
                        lights[y, x, 2] = 0

            lights[3, 3, 1] = 150
            yield lights, 0.03
            beam_angle += 0.1 # Sweep speed
            if beam_angle > 2*np.pi:
                beam_angle -= 2*np.pi

            target[0] += target_velocity[0]
            target[1] += target_velocity[1]

            if (round(target[0]) < 0 or round(target[0]) > 7 or
                round(target[1]) < 0 or round(target[1]) > 7):
                # Reset target.  Must be on an edge, see which:
                r = np.random.randint(4)
                if r == 0:
                    target = [0, np.random.randint(7)]
                    # Must give positive X component
                    target_velocity = ((np.random.random() + 1) / 100,
                        (-1)**np.random.randint(2)*(np.random.random()+1)/100)
                elif r == 1:
                    target = [6, np.random.randint(7)]
                    # Must give negative X component
                    target_velocity = ((np.random.random() + 1) / -100,
                        (-1)**np.random.randint(2)*(np.random.random()+1)/100)
                elif r == 2:
                    target = [np.random.randint(7), 0]
                    # Must give positive Y component
                    target_velocity = (
                        (-1)**np.random.randint(2)*(np.random.random()+1)/100,
                        (np.random.random() + 1) / 100)
                elif r == 3:
                    target = [np.random.randint(7), 6]
                    # Must give negative Y component
                    target_velocity = (
                        (-1)**np.random.randint(2)*(np.random.random()+1)/100,
                        (np.random.random() + 1) / -100)

    def update(self):
        return self.gen.__next__()

