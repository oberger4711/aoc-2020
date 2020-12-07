#!/usr/bin/env python3

import re

#lines = [l.rstrip("\n") for l in open("input_test.txt")]
lines = [l.rstrip("\n") for l in open("input.txt")]

def part1():
    container_for = {}
    regex = "\w+ \w+ bag"
    for l in lines:
        attributes = [p[:-4] for p in re.findall(regex, l)]
        for a in attributes[1:]:
            if a != "no other":
                if a in container_for:
                    container_for[a] += [attributes[0]]
                else:
                    container_for[a] = [attributes[0]]

    def count_distinc_containers_(attr, cache):
        cache[attr] = True
        total = 0
        if attr in container_for:
            for container in container_for[attr]:
                if not container in cache:
                    total += 1 + count_distinc_containers_(container, cache)
        return total

    def count_distinc_containers(attr):
        cache = {}
        return count_distinc_containers_(attr, cache)
    return count_distinc_containers("shiny gold")

def part2():
    content_of = {}
    regex = "(?:\d )?\w+ \w+ bag"
    for l in lines:
        digits_and_attributes = [p[:-4] for p in re.findall(regex, l)]
        container = digits_and_attributes[0]
        if digits_and_attributes[1] != "no other":
            for da in digits_and_attributes[1:]:
                num_s, a = da.split(" ", 1)
                num = int(num_s)
                if container in content_of:
                    content_of[container] += [(num, a)]
                else:
                    content_of[container] = [(num, a)]
    cache = {}
    def count_content(attr):
        #print("counting {}".format(attr))
        total = 0
        if attr in content_of:
            for num, c in content_of[attr]:
                if c in cache:
                    count = cache[c]
                else:
                    count = count_content(c)
                    cache[c] = count
                total += num + num * count
        #print("{} contains {}".format(attr, total))
        return total
    return count_content("shiny gold")

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
