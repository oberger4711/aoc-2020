#!/usr/bin/env python3

lines = [l.rstrip("\n") for l in open("input.txt")]

def part1():
    ts_min = int(lines[0])
    bus_ids = [int(n) for n in lines[1].split(",") if n != "x"]
    # Find earliest departure after ts_min
    ts_earliest_dep = None
    bus_id_earliest_dep = None
    for bus_id in bus_ids:
        if ts_min % bus_id == 0: return 0
        ts_dep = (ts_min // bus_id) * bus_id + bus_id
        if ts_earliest_dep is None or ts_dep < ts_earliest_dep:
            ts_earliest_dep = ts_dep
            bus_id_earliest_dep = bus_id
    return bus_id_earliest_dep * (ts_earliest_dep - ts_min)

# Too slow!:
def part2_bf():
    TS_START = 100000000000000
    #TS_START = 12021614
    indexed_bus_ids = [(i, int(n)) for i, n in enumerate(lines[1].split(",")) if n != "x"]
    # We check starting with the largest number to be more efficient.
    checks = sorted(indexed_bus_ids, key=lambda ibi: ibi[1], reverse=True)
    increment = checks[0][1]
    ts = ((TS_START // increment) * increment + increment) - checks[0][0]
    while True:
        for check in checks[1:]:
            if not ((ts + check[0]) % check[1]) == 0:
                break
        else:
            return ts
        ts += increment

def part2_optimized():
    TS_START = 100000000000000
    indexed_bus_ids = [[i, int(n)] for i, n in enumerate(lines[1].split(",")) if n != "x"]
    # We check starting with the largest number to be more efficient.
    checks = sorted(indexed_bus_ids, key=lambda ibi: ibi[1], reverse=True)
    increment = checks[0][1]
    ts = ((TS_START // increment) * increment + increment) - checks[0][0]
    idx_current_check = 1 # Index of the current check to apply. All preceding checks are true because we choose the correct increment.
    current_check = checks[idx_current_check]
    last_ts_current_check_succeeded = None # Used to calculate the new increment as soon as the current check succeeded twice.
    while True:
        if ((ts + current_check[0]) % current_check[1]) == 0:
            if idx_current_check == len(checks) - 1: return ts
            for check in checks[idx_current_check+1:]:
                if not ((ts + check[0]) % check[1]) == 0:
                    break
            else:
                return ts
            # Current check succeeded but not all others.
            if last_ts_current_check_succeeded is None:
                last_ts_current_check_succeeded = ts
            else:
                # We found the new larger increment to also skip the current check in the future.
                increment = ts - last_ts_current_check_succeeded
                last_ts_current_check_succeeded = None
                idx_current_check += 1
                current_check = checks[idx_current_check]
                #print("Passed check for bus id {}. New increment is {}.".format(current_check[1], increment))
        ts += increment

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2_optimized()))
