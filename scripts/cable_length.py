acc = 0
for x in range(7):
    for y in range(7):
        xlength = 12 - 2 * x
        ylength = 2 * abs(y - 3)
        pad = 2.5
        total = xlength + ylength + pad
        acc += total
        print("LED ({}, {}): {}m + {}m + {}m = {}m".format(
              x, y, xlength, ylength, pad, total))

print("Total length: {}".format(acc))
