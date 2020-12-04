#!/usr/bin/env python3
import re

raw_passports = open("input.txt").read().split("\n\n")
fields = [ "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid",
        # Ignore this:
        #"cid"
        ]

def part1():
    field_re = re.compile("^" + "|".join(fields))
    def has_all_fields(raw_passport):
        words = raw_passport.split()
        hits = sum((1 for w in words if field_re.match(w)))
        return hits == len(fields)
    return sum((1 for pp in raw_passports if has_all_fields(pp)))

def part2():
    # Decorator to check number in range, which is used for multiple fields.
    def check_number_between(regex, lower, upper):
        def check(w):
            match = regex.match(w)
            if match:
                val = int(match.groups()[0])
                return lower <= val and val <= upper
            return False
        return check
    # Decorator to check only if regex matches.
    def check_match(regex):
        return lambda w: regex.match(w)

    checks = [
            check_number_between(re.compile("^byr:(\d{4})$"), 1920, 2002),
            check_number_between(re.compile("^iyr:(\d{4})$"), 2010, 2020),
            check_number_between(re.compile("^eyr:(\d{4})$"), 2010, 2030),
            check_number_between(re.compile("^hgt:(\d+)cm$"), 150, 193), # for cm
            check_number_between(re.compile("^hgt:(\d+)in$"), 59, 76), # for in
            check_match(re.compile("^hcl:#[0-9a-f]{6}$")),
            check_match(re.compile("^ecl:(amb|blu|brn|gry|grn|hzl|oth)$")),
            check_match(re.compile("^pid:\d{9}$"))
        ]
    def has_all_fields(raw_passports):
        words = raw_passports.split()
        hits = sum((1 for w in words if any((check(w) for check in checks))))
        return hits == len(fields)
    return sum((1 for pp in raw_passports if has_all_fields(pp)))

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
