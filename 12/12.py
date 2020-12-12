#!/usr/bin/env python3

import numpy as np

ORIENTATIONS = ["N", "W", "S", "E"]
ORIENTED_STEPS = [(0, 1), (-1, 0), (0, -1), (1, 0)]

#actions = [(l[0], int(l.rstrip("\n")[1:])) for l in open("input_test.txt")]
actions = [(l[0], int(l.rstrip("\n")[1:])) for l in open("input.txt")]

def part1():
    state = [0, 0, 3] # x, y, orientation (idx)
    for a in actions:
        if a[0] == "N":   state[1] += a[1]
        elif a[0] == "S": state[1] -= a[1]
        elif a[0] == "E": state[0] += a[1]
        elif a[0] == "W": state[0] -= a[1]
        elif a[0] == "L": state[2] = (state[2] + (a[1] // 90)) % 4
        elif a[0] == "R": state[2] = (state[2] - (a[1] // 90)) % 4
        elif a[0] == "F":
            step = ORIENTED_STEPS[state[2]]
            state[0] += step[0] * a[1]
            state[1] += step[1] * a[1]
        #print(state)
    return abs(state[0]) + abs(state[1])

def make_rot_matrix(theta):
    sin_theta, cos_theta = round(np.sin(theta)), round(np.cos(theta))
    return np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]], dtype=np.int64)

def part2():
    pos = np.array([0, 0], dtype=np.int64)
    waypoint = np.array([10, 1], dtype=np.int64)
    for a in actions:
        if a[0] == "N":   waypoint[1] += a[1]
        elif a[0] == "S": waypoint[1] -= a[1]
        elif a[0] == "E": waypoint[0] += a[1]
        elif a[0] == "W": waypoint[0] -= a[1]
        elif a[0] == "L": waypoint = make_rot_matrix(np.radians(a[1])) @ waypoint
        elif a[0] == "R": waypoint = make_rot_matrix(np.radians(-a[1])) @ waypoint
        elif a[0] == "F":
            pos += waypoint * a[1]
        #print("ship: {}, waypoint: {}".format(pos, waypoint))
    return abs(pos[0]) + abs(pos[1])

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
