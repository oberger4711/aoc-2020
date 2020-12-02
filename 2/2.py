#!/usr/bin/env python3
import re

lines = [l for l in open("input.txt")]
regex = re.compile("^(\d+)-(\d+) (\w): (\w+)")

def part1():
    valids = 0
    for l in lines:
        s_lower, s_upper, letter, pw = regex.match(l).groups()
        lower, upper = int(s_lower), int(s_upper)
        occurances = sum((1 for c in pw if c == letter))
        if occurances >= lower and occurances <= upper:
            valids += 1
    return valids

def part2():
    valids = 0
    for l in lines:
        s_first, s_second, letter, pw = regex.match(l).groups()
        first, second = int(s_first) - 1, int(s_second) - 1
        if (pw[first] == letter) != (pw[second] == letter):
            valids += 1
    return valids

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
