#!/usr/bin/env python3

# Not very efficient solution but I leave it like this because it is christmas.

import numpy as np

lines = [l.strip() for l in open("input.txt")]
#lines = [l.strip() for l in open("input_test.txt")]

VECTORS_EVEN = {
    "e":  np.array([ 0,  1], dtype=np.int32),
    "w":  np.array([ 0, -1], dtype=np.int32),
    "nw": np.array([-1, -1], dtype=np.int32), # x depends on row!
    "sw": np.array([ 1, -1], dtype=np.int32), # x depends on row!
    "se": np.array([ 1,  0], dtype=np.int32), # x depends on row!
    "ne": np.array([-1,  0], dtype=np.int32)  # x depends on row!
}
VECTORS_ODD = {
    "e":  np.array([ 0,  1], dtype=np.int32),
    "w":  np.array([ 0, -1], dtype=np.int32),
    "nw": np.array([-1,  0], dtype=np.int32), # x depends on row!
    "sw": np.array([ 1,  0], dtype=np.int32), # x depends on row!
    "se": np.array([ 1,  1], dtype=np.int32), # x depends on row!
    "ne": np.array([-1,  1], dtype=np.int32)  # x depends on row!
}
def get_vec(row, direction):
    if row % 2 == 0:
        return VECTORS_EVEN[direction]
    else:
        return VECTORS_ODD[direction]

def line_to_centered_coord(line):
    centered_coord = np.array([0, 0], dtype=np.int32) # Assumed even!
    i = 0
    while i < len(line):
        direction = line[i]
        if direction in "sn":
            direction += line[i+1]
            i += 1
        i += 1
        centered_coord += get_vec(centered_coord[0], direction)
    return centered_coord

assert np.array_equal(line_to_centered_coord("esew"), np.array([1, 0], dtype=np.int32))
assert np.array_equal(line_to_centered_coord("nwwswee"), np.array([0, 0], dtype=np.int32))
# Test:
#centered_coords = [
#        line_to_centered_coord("nwwswee"),
#        line_to_centered_coord("se"),
#        line_to_centered_coord("e"),
#    ]

centered_coords = [line_to_centered_coord(l) for l in lines]

PRINT_CHARS = {
    0: ".",
    1: "#"
}
def print_grid(grid):
    for row in range(grid.shape[0]):
        line = " ".join([PRINT_CHARS[v] for v in grid[row, :]])
        if row % 2 == 1:
            line = " " + line
        print("{:3} {}".format(row, line))

def part1():
    padding = np.array([max(abs(c[0]) for c in centered_coords), max(abs(c[1]) for c in centered_coords)], dtype=np.int32)
    # Make sure center row is even!
    if padding[0] % 2 != 0: padding[0] += 1
    grid = np.zeros((2 * padding[0] + 1, 2 * padding[1] + 1), dtype=np.int32)
    for cc in centered_coords:
        c = padding + cc
        grid[c[0], c[1]] = 1 - grid[c[0], c[1]] # Flip
    print_grid(grid)
    print("Part 1: {}".format(np.sum(grid)))
    return grid

def get_neighbor_coords(coords):
    if coords[0] % 2 == 0:
        return [coords + v for v in VECTORS_EVEN.values()]
    return [coords + v for v in VECTORS_ODD.values()]

def zero_pad_grid(grid, padding):
    assert padding % 2 == 0
    enlarged_grid = np.zeros((grid.shape[0] + padding * 2, grid.shape[1] + padding * 2), dtype=np.int32)
    enlarged_grid[padding:padding + grid.shape[0], padding:padding + grid.shape[1]] = grid
    return enlarged_grid

def part2(grid):
    PADDING = 52 # NOTE: Must be even.
    grid = zero_pad_grid(grid, PADDING)
    next_grid = np.copy(grid)
    for day in range(100):
        # Check if padding must be increased.
        if np.any(grid[0, :] == 1) or np.any(grid[-1, :] == 1) or np.any(grid[:, 0] == 1) or np.any(grid[:, -1] == 1):
            print("Day {}: Padding not sufficient anymore! Increase it.".format(day))
            print_grid(grid)
            print("ABORTING.")
            exit(1)
        for row in range(grid.shape[0] - 1):
            for col in range(grid.shape[1] - 1):
                neighbor_coords = get_neighbor_coords(np.array([row, col], dtype=np.int32))
                num_flipped_neighbors = sum(grid[nc[0], nc[1]] for nc in neighbor_coords)
                if grid[row, col] == 1 and num_flipped_neighbors == 0 or num_flipped_neighbors > 2:
                    next_grid[row, col] = 0
                elif grid[row, col] == 0 and num_flipped_neighbors == 2:
                    next_grid[row, col] = 1
                else:
                    next_grid[row, col] = grid[row, col]
        grid, next_grid = next_grid, grid # Swap
        #print("Day {}: ({} flipped)".format(day + 1, np.sum(grid)))
        #print_grid(grid)
    #print_grid(grid)
    print("Part 2: {}".format(np.sum(grid)))

grid = part1()
part2(grid)
