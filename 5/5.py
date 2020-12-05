#!/usr/bin python3

lines = [l.rstrip("\n") for l in open("input.txt")]

def decode_seat(bp):
    lookup = {"F": 0, "B": 1, "L": 0, "R": 1}
    row = sum((lookup[c] * 2**i for i, c in enumerate(reversed(bp[:7]))))
    col = sum((lookup[c] * 2**i for i, c in enumerate(reversed(bp[7:]))))
    return row * 8 + col

def part1():
    return max(decode_seat(bp) for bp in lines)

def part2():
    seats = [False for i in range(833)]
    for bp in lines:
        seats[decode_seat(bp)] = True
    i_first_occupied = next((i for i, occupied in enumerate(seats) if occupied))
    for offset, occupied in enumerate(seats[i_first_occupied:]):
        if not occupied: return i_first_occupied + offset


print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
