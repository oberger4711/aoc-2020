#!/usr/bin/env python3

import string

abc = string.ascii_lowercase
raw_groups = open("input.txt").read().split("\n\n")
groups = [rg.split() for rg in raw_groups]

def part1():
    total = 0
    for g in groups:
        yes = {}
        for l in abc: yes[l] = False
        for f in g:
            for l in f:
                yes[l] = True
        total += sum((1 for k, v in yes.items() if v))
    return total

def part2():
    total = 0
    for g in groups:
        yes = {}
        for l in abc: yes[l] = 0
        for f in g:
            for l in f:
                yes[l] += 1
        total += sum((1 for k, v in yes.items() if v == len(g)))
    return total

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
