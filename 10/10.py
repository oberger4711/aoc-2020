#!/usr/bin/env python3

import numpy as np

numbers_file = [int(l.rstrip("\n")) for l in open("input.txt")]
#numbers_file = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4] # For testing

def part1():
    numbers = np.array([0] + numbers_file + [max(numbers_file) + 3])
    diffs = np.diff(np.sort(numbers))
    return diffs[diffs == 1].shape[0] * diffs[diffs == 3].shape[0]

def part2():
    numbers = [0] + sorted(numbers_file) + [max(numbers_file) + 3]
    cache = {}
    def count_arrangements(i):
        if i == len(numbers) - 1: return 1
        total = 0
        j = i + 1
        while j < len(numbers) and numbers[j] - numbers[i] <= 3:
            if j in cache: total += cache[j]
            else: total += count_arrangements(j)
            j += 1
        cache[i] = total
        return total
    return count_arrangements(0)

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
