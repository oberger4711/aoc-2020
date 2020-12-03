#!/usr/bin/env python3

area = [l.rstrip("\n") for l in open("input.txt")]
height, width = len(area), len(area[0])

def count_trees(slope):
    trees, row, col = 0, 0, 0
    while True:
        if area[row][col] == "#":
            trees += 1
        row += slope[0]
        col = (col + slope[1]) % width
        if row >= height:
            break
    return trees
print("Part 1: {}".format(count_trees((1, 3))))
# Part 2
slopes = [
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1)
    ]
prod = 1
for slope in slopes:
    prod *= count_trees(slope)
print("Part 2: {}".format(prod))
