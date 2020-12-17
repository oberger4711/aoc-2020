#!/usr/bin/env python3

import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

lines = [l.rstrip("\n") for l in open("input.txt")]
#lines = [l.rstrip("\n") for l in open("input_test.txt")]

grid_init = np.zeros((len(lines[0]), len(lines)), dtype=np.int16)
for y, l in enumerate(lines):
    for x, c in enumerate(l):
        if c == "#": grid_init[y, x] = 1

def step(grid):
    grid_next = np.copy(grid)
    for z in range(grid.shape[0]):
        bounds_z = (max(z - 1, 0), min(z + 2, grid.shape[0]))
        for y in range(grid.shape[1]):
            bounds_y = (max(y - 1, 0), min(y + 2, grid.shape[1]))
            for x in range(grid.shape[2]):
                bounds_x = (max(x - 1, 0), min(x + 2, grid.shape[2]))
                value = grid[z, y, x]
                active_neighbors = np.sum(grid[bounds_z[0]:bounds_z[1], bounds_y[0]:bounds_y[1], bounds_x[0]:bounds_x[1]]) - value
                active = (value == 1)
                active_next = active
                # Rules
                if active and (active_neighbors < 2 or active_neighbors > 3):
                    active_next = 0
                elif not active and active_neighbors == 3:
                    active_next = 1
                grid_next[z, y, x] = active_next
    return grid_next

def part1():
    steps = 6
    # Pessimistically choose a size for the grid, assuming it grows by one in each direction in each dim per step.
    padding_init = steps
    grid = np.zeros((1 + 2 * padding_init, grid_init.shape[0] + 2 * padding_init, grid_init.shape[1] + 2 * padding_init), dtype=np.int16)
    grid[padding_init, padding_init:padding_init+grid_init.shape[0], padding_init:padding_init+grid_init.shape[1]] = grid_init
    #print(grid)
    for i in range(steps):
        #print("Step {}".format(i + 1))
        grid = step(grid)
        #print(grid)
    return np.sum(grid)

def part2():
    pass

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
