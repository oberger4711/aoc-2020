#!/usr/bin/env python3

import re

lines = [l.rstrip("\n") for l in open("input.txt")]
#lines = [l.rstrip("\n") for l in open("input_test_1.txt")]

re_mem = re.compile("^mem\[(\d+)\] = (\d+)$")
re_mask = re.compile("^mask = ([X01]+)$")

def part1():
    mask = {
        "AND": 0xFFFFFFFFFF,
        "OR": 0x0
        }
    mem = {}
    for l in lines:
        match_mem = re_mem.match(l)
        if match_mem:
            # Memory assignment
            addr_str, val_str = match_mem.groups()
            val_masked = (int(val_str) & mask["AND"]) | mask["OR"]
            mem[int(addr_str)] = val_masked
            #print("mem[{}] = {:10} --mask--> {}".format(addr_str, val_str, val_masked))
        else:
            # Mask assignment
            match_mask = re_mask.match(l)
            mask_str = match_mask.groups()[0]
            # Generate and mask (applied first).
            mask_and_str = mask_str.replace("1", "0").replace("X", "1")
            mask["AND"] = int(mask_and_str, base=2)
            # Generate or mask (applied second).
            mask_or_str = mask_str.replace("X", "0")
            mask["OR"] = int(mask_or_str, base=2)
    return sum(mem.values())

def part2():
    pass

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
