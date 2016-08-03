#!/usr/bin/python3

print("Serial cable patch lengths")

pole_spacing = 2.0      # Spacing between grid poles
reel_length = 98.0     # Length of reels of serial cable
real_reel_length = 100
inside_col_slack = 1.2  # Slack added to inter-pole patches in each column
end_col_slack = 3.2     # Slack added to patches between cols and tent

cuts = []

for x in range(7):
    # 2m patches between poles in each column
    for y in range(1, 7):
        cuts.append(pole_spacing + inside_col_slack)
    # Variable length patches from tents to starts of columns
    cuts.append(pole_spacing * abs(x - 3) + end_col_slack)

# Spares: one inter-pole and one end-col
cuts.append(pole_spacing + inside_col_slack)
cuts.append(pole_spacing * abs(x - 3) + end_col_slack)


print("\nTotal length: {:.1f}\n".format(sum(cuts)))

bins = [[], []]
unbinned = []

for cut in reversed(sorted(cuts)):
    for b in bins:
        if reel_length - sum(b) >= cut:
            b.append(cut)
            break
    else:
        unbinned.append(cut)

for idx, b in enumerate(bins):
    print("Bin {}: {}".format(idx, ', '.join(
        ["{:.2f}m".format(cut) for cut in b])))
    print("Total length: {:.1f}m, spare {:.1f}m\n".format(sum(b),
        reel_length - sum(b)))

if len(unbinned) != 0:
    print("Unbinned: {}".format(
        ', '.join(["{}m ".format(c) for c in unbinned])))
else:
    print("None unbinned.")


# Cutting list:
print("")
print("")
print("--== CUTTING LIST ==--")
for idx, b in enumerate(bins):
    print("--- Reel {} ---".format(idx+1))
    for cut in b:
        print("{:.1f}m\t[ ]".format(cut))
    print("Leftover: {:.1f}m".format(real_reel_length - sum(b)))
    print("")

if len(unbinned) != 0:
    print("--- Leftover ---")
    for cut in unbinned:
        print("{:.1f}m\t[ ]".format(cut))
