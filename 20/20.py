#!/usr/bin/env python3

import math

# Idea:
# * Use a map to resolve (flipped) interfaces to tile
# * Use backtracking algorithm to try all possible variations until a solution is found.

TFS = [
        "flip0_rot0",
        "flip0_rot1",
        "flip0_rot2",
        "flip0_rot3",

        "flipx_rot0",
        "flipx_rot1",
        "flipx_rot2",
        "flipx_rot3",

        "flipy_rot0",
        "flipy_rot1",
        "flipy_rot2",
        "flipy_rot3",
    ]

def get_interface(lines):
    return {
            "top": lines[0],
            "bottom": lines[-1],
            "left": "".join((l[0] for l in lines)),
            "right": "".join((l[-1] for l in lines))
        }

def rotate(interface, rotations):
    res = dict(interface)
    for i in range(rotations):
        res = {
            "top": res["right"],
            "left": res["top"][::-1], # Reverse
            "bottom": res["left"],
            "right": res["bottom"][::-1] # Reverse
        }
    return res

def flip_x(interface):
    return {
        "top": interface["bottom"],
        "bottom": interface["top"],
        "left": interface["left"][::-1], # Reverse
        "right": interface["right"][::-1] # Reverse
    }

def flip_y(interface):
    return {
        "left": interface["right"],
        "right": interface["left"],
        "top": interface["top"][::-1], # Reverse
        "bottom": interface["bottom"][::-1]
    }

inp = open("input.txt").read().rstrip("\n\n")
#inp = open("input_test.txt").read().rstrip("\n\n")

tiles = {} # tile id -> rotation -> iface
interfaces = {} # direction, iface -> tile id, rotation
for inp_tile in inp.split("\n\n"):
    lines = inp_tile.split("\n")
    id = lines[0][5:-1]
    iface_flip0_rot0 = get_interface(lines[1:])
    iface_flipx_rot0 = flip_x(iface_flip0_rot0)
    iface_flipy_rot0 = flip_y(iface_flip0_rot0)
    tfs = {
            "flip0_rot0": iface_flip0_rot0,
            "flip0_rot1": rotate(iface_flip0_rot0, 1),
            "flip0_rot2": rotate(iface_flip0_rot0, 2),
            "flip0_rot3": rotate(iface_flip0_rot0, 3),

            "flipx_rot0": iface_flipx_rot0,
            "flipx_rot1": rotate(iface_flipx_rot0, 1),
            "flipx_rot2": rotate(iface_flipx_rot0, 2),
            "flipx_rot3": rotate(iface_flipx_rot0, 3),

            "flipy_rot0": iface_flipy_rot0,
            "flipy_rot1": rotate(iface_flipy_rot0, 1),
            "flipy_rot2": rotate(iface_flipy_rot0, 2),
            "flipy_rot3": rotate(iface_flipy_rot0, 3),
        }
    # Id lookup
    tiles[id] = tfs
    # Reverse lookup:
    for tf, ifaces in tfs.items():
        for direction, iface in ifaces.items():
            if (direction, iface) not in interfaces: interfaces[(direction, iface)] = []
            interfaces[(direction, iface)] += [(id, tf, ifaces)]
            #print("{} = {}, {}, {}".format(iface, id, tf, direction))

#print(tiles["2311"]["flipx_rot0"])
#print(interfaces[("right", ".#..#####.")])
#print(interfaces[("left", ".#..#####.")])

#print(tiles["3079"]["flip0_rot0"])
#print(interfaces[("left", "#..##.#...")])

#print(tiles["2729"]["flip0_rot0"])

def print_grid(grid):
    for row in grid:
        ids = [t[0] for t in row if t is not None]
        print(("{} "*len(ids)).format(*ids))

def part1():
    # Recursive backtracking algorithm similar as for e. g. n queens problem.
    # Start at top left. We only have to check if interfaces at left and top match for the next tile.
    def find_solution_(y, x, side_len, grid, used_tile_ids):
        #print(y, x)
        #print_grid(grid)
        # Find options for the next tile.
        options = None # Items are (tile_id, tf, ifaces(tf))
        required_iface_left, required_iface_top = None, None
        if x > 0:
            tile_left = grid[y][x - 1]
            required_iface_left = ("left", tile_left[2]["right"])
            if required_iface_left not in interfaces:
                return None # Dead end!
            options = [o for o in interfaces[required_iface_left] if o[0] not in used_tile_ids]
        if y > 0:
            tile_top = grid[y - 1][x]
            required_iface_top = ("top", tile_top[2]["bottom"])
            if required_iface_top not in interfaces:
                return None # Dead end!
            options_top = interfaces[required_iface_top]
            #print(options_top)
            if options is None:
                options = [o for o in options_top if o[0] not in used_tile_ids]
            else:
                #print("{} x {}".format(len(options), len(options_top)))
                # Options is intersection set of options in top and left iface.
                options = [o for o in options if o in options_top] # Used id already checked.
        x_next = x + 1
        if x_next == side_len:
            # Next row.
            x_next = 0
            y_next = y + 1
        else: y_next = y
        #print("Options:")
        #print(options)
        for o in options:
            #print(o)
            grid[y][x] = o
            used_tile_ids.add(o[0])
            if y == x == side_len - 1:
                # Grid is full of valid tiles! We found a solution!
                return grid
            grid_res = find_solution_(y_next, x_next, side_len, grid, used_tile_ids)
            used_tile_ids.remove(o[0]) # Undo change to used_tile_ids for next iterations and recursions.
            if grid_res is not None:
                #print("SDFKJLKASDJLKSAJD")
                return grid_res
        # Reset changes to grid reference for previous recursion.
        grid[y][x] = None
        return None

    def find_solution():
        side_len = round(math.sqrt(len(tiles)))
        grid = [([None] * side_len) for _ in range(side_len)] # Items are (tile_id, tf, ifaces(tf))
        # Begin recursion. First tile could be anything.
        # This for loop could be parallelized (not sure how simple this is in python though...
        #print("Root recursion iterations: {}".format(len(tiles) * len(TFS)))
        for i, (tile_id, tile) in enumerate(tiles.items()):
            print("{} / {}".format(i, len(tiles)))
            for tf in TFS:
                grid[0][0] = (tile_id, tf, tile[tf])
                grid_res = find_solution_(0, 1, side_len, grid, {tile_id})
                if grid_res is not None: return grid_res
        return None

    grid_res = find_solution()
    print_grid(grid_res)

def part2():
    pass

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
