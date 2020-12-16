#!/usr/bin/env python3

import re

re_rule = re.compile("^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$")
# Split input lines.
lines = [l.rstrip("\n") for l in open("input.txt")]
#lines = [l.rstrip("\n") for l in open("input_test_1.txt")]
#lines = [l.rstrip("\n") for l in open("input_test_2.txt")]
lines_rules = []
for l in lines:
    if l != "": lines_rules += [l]
    else: break
line_your_ticket = lines[len(lines_rules) + 2]
lines_nearby_tickets = []
for l in lines[len(lines_rules) + 5:]:
    lines_nearby_tickets += [l]
# Parse lines.
rules = []
for l in lines_rules:
    m = re_rule.match(l)
    bounds = [int(s) for s in m.groups()[1:]]
    rules += [(m.groups()[0], bounds)]
your_ticket = [int(s) for s in line_your_ticket.split(",")]
nearby_tickets = []
for l in lines_nearby_tickets:
    values = [int(s) for s in l.split(",")]
    nearby_tickets += [values]

def rule_applies(rule, v):
    bounds = rule[1]
    return ((bounds[0] <= v and v <= bounds[1]) or (bounds[2] <= v and v <= bounds[3]))

def part1():
    res = 0
    for nt in nearby_tickets:
        for v in nt:
            for rule in rules:
                if rule_applies(rule, v): break
            else:
                res += v
    return res

def part2():
    # Discard invalid tickets.
    valid_nearby_tickets = []
    for nt in nearby_tickets:
        valid = True
        for v in nt:
            if all(not rule_applies(rule, v) for rule in rules):
                valid = False
                break
        if valid:
            valid_nearby_tickets += [nt]
    # Find out what the positions are using left over tickets.
    positions = {}
    #print("Matching rules to find out options.")
    for (name, bounds) in rules:
        for i in range(len(your_ticket)):
            for nt in valid_nearby_tickets:
                v = nt[i]
                if not ((bounds[0] <= v and v <= bounds[1]) or (bounds[2] <= v and v <= bounds[3])):
                    # Position does not match to rule. Must be something different.
                    break
            else:
                # Found a position that does not violate the rule.
                if name not in positions: positions[name] = []
                positions[name] += [i]
    #print("Options:")
    #for k, v in positions.items():
    #    print("  {}: [{}]".format(k, ", ".join([str(s) for s in v])))
    # Now derive step by step what must be the positions.
    #print("Derive sure positions by eliminating where only one option.")
    sure_positions = {}
    while len(sure_positions) < len(your_ticket):
        for label, pos_options in positions.items():
            if len(pos_options) == 1:
                # Only one possibility.
                pos_sure = pos_options[0]
                sure_positions[label] = pos_sure
                #print("  {} must be at {}.".format(label, pos_sure))
                # Remove from other options.
                for ps in positions.values():
                    if pos_sure in ps: ps.remove(pos_sure)
                break
    prod = 1
    for label, pos in sure_positions.items():
        if label.startswith("departure"):
            prod *= your_ticket[pos]
    return prod

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
