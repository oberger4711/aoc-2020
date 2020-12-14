#!/usr/bin/env python3

import re

lines = [l.rstrip("\n") for l in open("input.txt")]
#lines = [l.rstrip("\n") for l in open("input_test_1.txt")]
#lines = [l.rstrip("\n") for l in open("input_test_2.txt")]

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
    mask_or = 0
    mask_and = 0xFFFFFFFFFF
    floating_digits = []
    mem = {}
    for l in lines:
        match_mem = re_mem.match(l)
        if match_mem:
            # Memory assignment
            addr_str, val_str = match_mem.groups()
            addr_base = (int(addr_str) | mask_or) & mask_and
            val = int(val_str)
            for code in range(2 ** len(floating_digits)):
                addr = addr_base
                for i, fd in enumerate(reversed(floating_digits)):
                    addr |= ((code >> i) & 1) << fd
                #print("{:b} --mask({})--> {:b}".format(addr_base, code, addr))
                #print("mem[{}] = {}".format(addr, val_str))
                mem[addr] = val
        else:
            # Mask assignment
            match_mask = re_mask.match(l)
            mask_str = match_mask.groups()[0]
            mask_or = int(mask_str.replace("X", "1"), base=2)
            mask_and = int(mask_str.replace("0", "1").replace("X", "0"), base=2)
            floating_digits = [len(mask_str) - 1 - i for i, c in enumerate(mask_str) if c == "X"]
    return sum(mem.values())

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
