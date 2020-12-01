#!/usr/bin/env python3

from measure import measure

numbers = [int(line) for line in open("input.txt")]

@measure
def part1():
    lookup = [False for _ in range(2020)]
    for n in numbers:
        lookup[n] = True
    for n in numbers:
        if lookup[2020 - n]:
            return n * (2020 - n)

@measure
def part2_on3():
    for a in numbers:
        for b in numbers:
            for c in numbers:
                if a + b + c == 2020:
                    return a * b * c

@measure
def part2_on2():
    lookup = [False for _ in range(2020)]
    for n in numbers:
        lookup[n] = True
    for a in numbers:
        for b in numbers:
            c = 2020 - a - b
            if c > 0 and lookup[c]:
                return a * b * c

print("Part 1:         {}".format(part1()))
print("Part 2 (O(n^3): {}".format(part2_on3()))
print("Part 2 (O(n^2): {}".format(part2_on2()))
