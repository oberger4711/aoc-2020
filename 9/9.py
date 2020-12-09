#!/usr/bin/env python3

from measure import measure

BUF_SIZE = 25
numbers = [int(l.rstrip("\n")) for l in open("input.txt")]

@measure
def part1_brute_force():
    buf = []
    for i, n in enumerate(numbers):
        if i >= BUF_SIZE:
            # We are behind preamble now.
            found = False
            for j, s1 in enumerate(buf):
                for s2 in buf[j+1:]:
                    if s1 + s2 == n:
                        found = True
                        break
                if found: break
            else:
                return n # Did not find two numbers.
            buf = buf[1:] + [n]
        else:
            buf += [n]

@measure
def part1_optimized():
    lookup_cache = {} # Stores the number of occurances of any number in the current buffer.
    buf = [None] * BUF_SIZE # Some kind of ringbuffer.
    buf_insert_idx = 0
    for i, n in enumerate(numbers):
        if i >= BUF_SIZE:
            # We are behind preamble now.
            for m in buf:
                subtrahend = n - m
                if subtrahend in lookup_cache and lookup_cache[subtrahend] > 0:
                    break # Found two numbers in buffer that add to n.
            else:
                return n # Did not find two numbers.
        # Decrement old value counter from lookup cache.
        if buf[buf_insert_idx] is not None:
            lookup_cache[buf[buf_insert_idx]] -= 1
        # Insert next number into buffer and lookup cache.
        buf[buf_insert_idx] = n
        buf_insert_idx = (buf_insert_idx + 1) % BUF_SIZE
        if n in lookup_cache:
            lookup_cache[n] += 1
        else:
            lookup_cache[n] = 1

@measure
def part2_brute_force():
    for i, n in enumerate(numbers):
        total = n
        smallest, largest = n, n
        for m in numbers[i+1:]:
            total += m
            smallest = min(smallest, m)
            largest = max(largest, m)
            if total > 1504371145:
                break
            elif total == 1504371145:
                return smallest + largest

@measure
def part2_optimized():
    # Build integral image and reverse integral image lookup dict.
    integral_img = [0] * len(numbers)
    integral_lookup = {}
    total = 0
    for i, n in enumerate(numbers):
        total += n
        integral_img[i] = total
        integral_lookup[total] = i
    # Search for pair in integral image so that s2 - s1 = 1504371145.
    for i1, s1 in enumerate(integral_img):
        s2 = 1504371145 + s1
        if s2 in integral_lookup:
            i2 = integral_lookup[s2]
            # Find smallest and largest value in the area.
            smallest, largest = numbers[i1], numbers[i1]
            for n in numbers[i1+1:i2+1]:
                smallest = min(smallest, n)
                largest = max(largest, n)
            return smallest + largest


print("Part 1 (brute force): {}".format(part1_brute_force()))
print("Part 1 (optimized):   {}".format(part1_optimized()))
print("Part 2 (brute force): {}".format(part2_brute_force()))
print("Part 2 (optimized):   {}".format(part2_optimized()))
