#!/usr/bin/env python3

start_seq = [1, 0, 16, 5, 17, 4]
#start_seq = [0, 3, 6]

def solve(stop_turn):
    mem = {} # number -> turn
    prev_num, prev_turn = -1, None
    # Starting sequence
    for turn, num in enumerate(start_seq):
        mem[prev_num] = prev_turn
        prev_num, prev_turn = num, turn
    # Now the next number depends on previous number.
    for turn in range(prev_turn + 1, stop_turn):
        if not prev_num in mem:
            num = 0
        else:
            num = prev_turn - mem[prev_num]
        mem[prev_num] = prev_turn
        prev_num, prev_turn = num, turn
    return num

print("Part 1: {}".format(solve(2020)))
print("Part 2: {}".format(solve(30000000)))
