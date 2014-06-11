#!/usr/bin/python3

from random import randrange

width, height = 7, 7

print("Sparkle")
print("Kinda cool and sparkley and stuff...")
print("")

field = []
for _ in range(0, height):
    field.append(['.']*10)

for _ in range(0, 100):
    for x in range(0, width):
        for y in range(0, height):
            field[y][x]='.'

    for row in field:
        print("".join(row))
    print(randrange(0, 500))

    x, y = randrange(0, width), randrange(0, height)
    field[y][x] = '*'

    for row in field:
        print("".join(row))
    print("50")
    print("")
