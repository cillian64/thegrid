# Convert coordinate pair to a nice formatted string
def coords(x, y):
    letters = "ABCDEFG"
    return "{}{}".format(letters[y], x+1)

cuts = []

cuts.append((20.7, 0, 0))
cuts.extend([(14.7, 0, 0)]*7)
cuts.extend([(12.7, 0, 0)]*4)
cuts.extend([(10.7, 0, 0)]*7)
cuts.extend([(8.7, 0, 0)]*7)
cuts.extend([(6.7, 0, 0)]*5)
cuts.extend([(4.7, 0, 0)]*3)
cuts.append((2.7, 0, 0))

print("\nTotal length: {:.1f}\n".format(sum([c[0] for c in cuts])))

bins = [[], [], [], [], []]
binsizes = [25, 39.9, 100, 100, 100]
unbinned = []

for cut in reversed(sorted(cuts, key=lambda cut: cut[0])):
    length = cut[0]
    for idx, b in enumerate(bins):
        if binsizes[idx] - sum([c[0] for c in b]) >= length:
            b.append(cut)
            break
    else:
        unbinned.append(cut)

for idx, b in enumerate(bins):
    print("Bin {}: {}".format(idx, ', '.join(
        ["{:.2f}m".format(c[0]) for c in b])))
    print("Total length: {:.1f}m\n".format(sum([c[0] for c in b])))
print(unbinned)
print("Unbinned: {}".format(', '.join(["{}m ".format(c[0]) for c in unbinned])))


# Cutting list:
print("")
print("")
print("--== CUTTING LIST ==--")
for idx, b in enumerate(bins):
    print("--- Reel {} ---".format(idx+1))
    for cut in b:
        print("{}: {:.1f}m\t[ ]".format(coords(cut[1], cut[2]), cut[0]))
    print("")

print("--- Leftover ---")
for cut in unbinned:
    print("{}: {:.1f}m\t[ ]".format(coords(cut[1], cut[2]), cut[0]))
