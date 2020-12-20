#!/usr/bin/env python3

import math

# Idea:
# * Use a map to resolve (flipped) interfaces to tile
# * Use backtracking algorithm to try all possible variations until a solution is found.

# NOTE: The code is not very beautiful but it does the job and I won't ever reuse it again.

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

def rotate_iface(interface, rotations):
    res = dict(interface)
    for i in range(rotations):
        res = {
            "top": res["right"],
            "left": res["top"][::-1], # Reverse
            "bottom": res["left"],
            "right": res["bottom"][::-1] # Reverse
        }
    return res

def flip_iface_x(interface):
    return {
        "top": interface["bottom"],
        "bottom": interface["top"],
        "left": interface["left"][::-1], # Reverse
        "right": interface["right"][::-1] # Reverse
    }

def flip_iface_y(interface):
    return {
        "left": interface["right"],
        "right": interface["left"],
        "top": interface["top"][::-1], # Reverse
        "bottom": interface["bottom"][::-1]
    }

def rotate_image(image, rotations):
    res = image
    for i in range(rotations):
        res = ["".join(l[-i-1] for l in res) for i, l in enumerate(res)]
    return res
#print("\n".join(rotate_image(["abc", "def", "ghi"], 3)))
#exit()

def flip_image_x(image):
    return [l for l in reversed(image)]

def flip_image_y(image):
    return [l[::-1] for l in image]

inp = open("input.txt").read().rstrip("\n\n")
#inp = open("input_test.txt").read().rstrip("\n\n")

images = {} # (tile id, tf) -> cropped lines without interfaces
tiles = {} # tile id -> rotation -> iface
interfaces = {} # direction, iface -> tile id, rotation
for inp_tile in inp.split("\n\n"):
    lines = inp_tile.split("\n")
    id = lines[0][5:-1]
    iface_flip0_rot0 = get_interface(lines[1:])
    iface_flipx_rot0 = flip_iface_x(iface_flip0_rot0)
    iface_flipy_rot0 = flip_iface_y(iface_flip0_rot0)
    tfs_to_add = {
            "flip0_rot0": iface_flip0_rot0,
            "flip0_rot1": rotate_iface(iface_flip0_rot0, 1),
            "flip0_rot2": rotate_iface(iface_flip0_rot0, 2),
            "flip0_rot3": rotate_iface(iface_flip0_rot0, 3),

            "flipx_rot0": iface_flipx_rot0,
            "flipx_rot1": rotate_iface(iface_flipx_rot0, 1),
            "flipx_rot2": rotate_iface(iface_flipx_rot0, 2),
            "flipx_rot3": rotate_iface(iface_flipx_rot0, 3),

            "flipy_rot0": iface_flipy_rot0,
            "flipy_rot1": rotate_iface(iface_flipy_rot0, 1),
            "flipy_rot2": rotate_iface(iface_flipy_rot0, 2),
            "flipy_rot3": rotate_iface(iface_flipy_rot0, 3),
        }
    # Check for and remove symmetries.
    # This gives a huge speedup!! Without it, we get stuck in deeper recursions.
    tfs = {}
    for k, v in tfs_to_add.items():
        if v not in tfs.values():
            tfs[k] = v

    # Id lookup
    tiles[id] = tfs
    # Reverse lookup:
    for tf, ifaces in tfs.items():
        for direction, iface in ifaces.items():
            if (direction, iface) not in interfaces: interfaces[(direction, iface)] = []
            interfaces[(direction, iface)] += [(id, tf, ifaces)]

    # For part 2
    image_flip0_rot0 = [l[1:-1] for l in lines[2:-1]]
    image_flipx_rot0 = flip_image_x(image_flip0_rot0)
    image_flipy_rot0 = flip_image_y(image_flip0_rot0)
    images_to_add = {
            "flip0_rot0": image_flip0_rot0,
            "flip0_rot1": rotate_image(image_flip0_rot0, 1),
            "flip0_rot2": rotate_image(image_flip0_rot0, 2),
            "flip0_rot3": rotate_image(image_flip0_rot0, 3),

            "flipx_rot0": image_flipx_rot0,
            "flipx_rot1": rotate_image(image_flipx_rot0, 1),
            "flipx_rot2": rotate_image(image_flipx_rot0, 2),
            "flipx_rot3": rotate_image(image_flipx_rot0, 3),

            "flipy_rot0": image_flipy_rot0,
            "flipy_rot1": rotate_image(image_flipy_rot0, 1),
            "flipy_rot2": rotate_image(image_flipy_rot0, 2),
            "flipy_rot3": rotate_image(image_flipy_rot0, 3),
            }
    # Image lookup
    for tf, img in images_to_add.items():
        images[(id, tf)] = img

# Recursive backtracking algorithm similar as for e. g. n queens problem.
# Start at top left. We only have to check if interfaces at left and top match for the next tile.
def find_solution_(y, x, side_len, grid, used_tile_ids, depth):
    #print_grid(grid)
    #print()
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
        if options is None:
            options = [o for o in options_top if o[0] not in used_tile_ids]
        else:
            # Options is intersection set of options in top and left iface.
            options = [o for o in options if o in options_top] # Used id already checked.
    # Further filtering of options if not in last line (does not save time really...)
    #if y < side_len - 1: options = [o for o in options if ("top", o[2]["bottom"]) in interfaces]
    x_next = x + 1
    if x_next == side_len:
        # Next row.
        x_next = 0
        y_next = y + 1
    else: y_next = y
    max_depth = depth
    for o in options:
        grid[y][x] = o
        used_tile_ids.add(o[0])
        if y == x == side_len - 1:
            # Grid is full of valid tiles! We found a solution!
            return grid, max_depth
        grid_res, option_max_depth = find_solution_(y_next, x_next, side_len, grid, used_tile_ids, depth + 1)
        max_depth = max(max_depth, option_max_depth)
        used_tile_ids.remove(o[0]) # Undo change to used_tile_ids for next iterations and recursions.
        if grid_res is not None:
            return grid_res, max_depth
    # Reset changes to grid reference for previous recursion.
    grid[y][x] = None
    return None, max_depth

def find_solution():
    side_len = round(math.sqrt(len(tiles)))
    grid = [([None] * side_len) for _ in range(side_len)] # Items are (tile_id, tf, ifaces(tf))
    # Begin recursion. First tile could be anything.
    # This for loop could be parallelized (not sure how simple this is in python though...
    for i, (tile_id, tile) in enumerate(tiles.items()):
        #print("{} / {}".format(i, len(tiles)))
        for tf in TFS:
            if tf in tile:
                grid[0][0] = (tile_id, tf, tile[tf])
                grid_res, max_depth = find_solution_(0, 1, side_len, grid, {tile_id}, 0)
                #print("Max depth: {}".format(max_depth))
                if grid_res is not None: return grid_res
    return None

def print_grid(grid):
    for row in grid:
        l = ""
        for c in row:
            #l += "{} ({})  ".format(c[0], c[1])
            l += "{} ".format(c[0])
        print(l)

def part1():
    grid_res = find_solution()
    print_grid(grid_res)
    corners = [int(cell[0]) for cell in [grid_res[0][0], grid_res[0][-1], grid_res[-1][0], grid_res[-1][-1]]]
    prod = 1
    for id in corners: prod *= id
    return prod

def build_grid_image(grid):
    lines = []
    for row_grid in grid:
        tile_images = [images[(c[0], c[1])] for c in row_grid]
        lines_to_add = len(tile_images[0])
        for i in range(lines_to_add):
            #lines += ["  ".join((cc[i] for cc in tile_images))]
            lines += ["".join((cc[i] for cc in tile_images))]
        #lines += [""]
    return lines

def part2():
    grid_res = find_solution()
    grid_image = build_grid_image(grid_res)
    pattern = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "
        ]
    pattern_line_length = len(pattern[0])
    mask = [[i for i, c in enumerate(l) if c == "#"] for l in pattern]
    def mark_sea_monster(img):
        for il, l in enumerate(img[:-2]):
            for ic, _ in enumerate(l[:-pattern_line_length+1]):
                match = True
                for iml, ml in enumerate(mask):
                    for mc in ml:
                        if img[il+iml][ic+mc] not in "#O":
                            match = False
                            break
                    if match == False: break
                if match:
                    for iml, ml in enumerate(mask):
                        for mc in ml:
                            img[il+iml] = img[il+iml][:ic+mc] + "O" + img[il+iml][ic+mc+1:]

    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 1
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 2
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 3
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 0

    grid_image = flip_image_x(grid_image)
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 1
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 2
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 3
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 0
    grid_image = flip_image_x(grid_image)

    grid_image = flip_image_y(grid_image)
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 1
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 2
    mark_sea_monster(grid_image)
    grid_image = rotate_image(grid_image, 1) # 3
    mark_sea_monster(grid_image)
    print("\n".join(grid_image))
    return sum(sum(1 for c in l if c == "#") for l in grid_image)

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
