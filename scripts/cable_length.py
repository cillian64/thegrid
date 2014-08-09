lengths = []
for x in range(7):
    for y in range(7):
        xlength = 12 - 2 * x
        ylength = 2 * abs(y - 3)
        pad = 2.5
        total = xlength + ylength + pad
        lengths.append(total)
        print("LED ({}, {}): {}m + {}m + {}m = {}m".format(
              x, y, xlength, ylength, pad, total))

print("\nTotal length: {}\n".format(sum(lengths)))

bins = [[], [], [], [], [], []]
unbinned = []

for length in reversed(sorted(lengths)):
    for b in bins:
        if 100.0 - sum(b) >= length:
            b.append(length)
            break
    else:
        unbinned.append(length)

for idx, b in enumerate(bins):
    print("Bin {}: {}".format(idx, ', '.join(["{}m".format(l) for l in b])))
    print("Total length: {}m\n".format(sum(b)))

print("Unbinned: {}".format(', '.join(["{}m".format(l) for l in unbinned])))
