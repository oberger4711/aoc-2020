#!/usr/bin/env python3

numbers = [int(line) for line in open("input.txt")]

def part1():
    lookup = [False for _ in range(2020)]
    for n in numbers:
        lookup[n] = True
    for n in numbers:
        if lookup[2020 - n]:
            print("Part 1: {}".format(n * (2020 - n)))
            return

def part2():
    # O(n^3) is fast enough for only 200 numbers.
    for a in numbers:
        for b in numbers:
            for c in numbers:
                if a + b + c == 2020:
                    print("Part 2: {}".format(a * b * c))
                    return

part1()
part2()
