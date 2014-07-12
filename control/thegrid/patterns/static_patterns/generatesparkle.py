#!/usr/bin/python3

from random import randrange

width, height = 7, 7

print("Sparkle")

for _ in range(100):
    field = [['.'] * width for _ in range(height)]

    # Space between flashes
    print()
    for row in field:
        print("".join(row))
    print(randrange(0, 500))
    print()

    x, y = randrange(0, width), randrange(0, height)
    field[y][x] = '*'

    for row in field:
        print("".join(row))
    print("50")
