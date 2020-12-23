#!/usr/bin/env python3

# NOTE: This is the really slow variant which I came up first.
# NOTE: During implementation I came up with a better solution. See part 2 (C++).

def part1():
    def play_move(cups, i_current_cup, l_lowest, l_highest):
        l_current_cup = cups[i_current_cup]
        # Pick up.
        #print("Cups: {}".format(", ".join(str(c) for c in cups)))
        pick_up_warp = max(0, i_current_cup + 4 - len(cups))
        picked_up = cups[i_current_cup+1:i_current_cup+4] + cups[:pick_up_warp]
        assert(len(picked_up) == 3)
        cups = cups[pick_up_warp:i_current_cup+1] + cups[i_current_cup+4:] # Remove picked up from cups.
        #print("Picked up: {}".format(", ".join(str(c) for c in picked_up)))
        # Select destination.
        l_dest = l_current_cup
        while True:
            l_dest -= 1
            if l_dest < l_lowest: l_dest = l_highest
            if l_dest not in picked_up: break
        #print("Label dest: {}".format(l_dest))
        i_dest = cups.index(l_dest) + 1
        # Place.
        cups = cups[:i_dest] + picked_up + cups[i_dest:]
        # Hack: Rotate left until i_current_cup is in position again.
        wrong_i_current_cup = cups.index(l_current_cup)
        warp_around = (i_current_cup - wrong_i_current_cup) % len(cups)
        cups = cups[-warp_around:] + cups[:-warp_around]
        # Now it should be okay again.
        #print("Placed: {}".format(", ".join(str(c) for c in cups)))
        return cups, (i_current_cup + 1) % len(cups)
    cups = [3, 2, 6, 5, 1, 9, 4, 7, 8] # Real input
    #cups = [3, 8, 9, 1, 2, 5, 4, 6, 7] # Test input
    i_current_cup = 0
    l_lowest, l_highest = min(cups), max(cups)
    for i in range(100):
    #for i in range(10):
        #print("\nMove {}:".format(i + 1))
        cups, i_current_cup = play_move(cups, i_current_cup, l_lowest, l_highest)
    i_after_one = (cups.index(1) + 1) % len(cups)
    return "".join(str(c) for c in cups[i_after_one:] + cups[:i_after_one-1])

print("Part 1: {}".format(part1()))
# Part 2 in CPP.
