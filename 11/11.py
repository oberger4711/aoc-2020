#!/usr/bin/env python3

from time import sleep

ANIMATE = True

#input_grid = [[c for c in l.rstrip("\n")] for l in open("input_test.txt")]
input_grid = [[c for c in l.rstrip("\n")] for l in open("input.txt")]

def print_grid(grid):
    for row in grid:
        print("".join(row))

def in_bounds(grid, coord):
    return 0 <= coord[0] and coord[0] < len(grid) and 0 <= coord[1] and coord[1] < len(grid[0])

def count_all_occupied(grid):
    return sum((sum((1 for v in row if v == "#")) for row in grid))

def simulate_step(grid, count_occupied_neighbors, occupied_tolerance):
    changed = False
    next_grid = []
    for y, row in enumerate(grid):
        next_row = []
        for x, v in enumerate(row):
            if v == ".":
                next_v = "."
            else:
                occupied_neighbors = count_occupied_neighbors(grid, y, x)
                # The rules.
                if v == "L" and occupied_neighbors == 0:
                    next_v = "#"
                    changed = True
                elif v == "#" and occupied_neighbors >= occupied_tolerance:
                    next_v = "L"
                    changed = True
                else:
                    next_v = v
            next_row += [next_v]
        next_grid += [next_row]
    return next_grid, changed

def simulate_until_converged(grid, count_occupied_neighbors, occupied_tolerance):
    changed = True
    while changed:
        grid, changed = simulate_step(grid, count_occupied_neighbors, occupied_tolerance)
        if ANIMATE:
            print_grid(grid)
            print()
            sleep(0.1)
    return count_all_occupied(grid)

def part1():
    def count_eight_connected_occupied(grid, y, x):
        neighbors = [
                (y - 1, x - 1), (y - 1, x    ), (y - 1, x + 1),
                (y,     x - 1),                 (y,     x + 1),
                (y + 1, x - 1), (y + 1, x    ), (y + 1, x + 1)
                ]
        return sum((1 for coord in neighbors if in_bounds(grid, coord) and grid[coord[0]][coord[1]] == "#"))
    return simulate_until_converged(input_grid, count_eight_connected_occupied, 4)

def part2():
    def count_next_visible_occupied(grid, y, x, step):
        cur = (y + step[0], x + step[1])
        while in_bounds(grid, cur):
            cur_v = grid[cur[0]][cur[1]]
            if cur_v == "#":
                return 1
            elif cur_v == "L":
                return 0
            cur = (cur[0] + step[0], cur[1] + step[1])
        return 0

    def count_eight_visible_occupied(grid, y, x):
        steps = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1)
                 ]
        return sum((count_next_visible_occupied(grid, y, x, s) for s in steps))
    return simulate_until_converged(input_grid, count_eight_visible_occupied, 5)

#print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
