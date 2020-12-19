 #!/usr/bin/env python3

import regex

lines_all = [l.rstrip("\n") for l in open("input.txt")]
#lines_all = [l.rstrip("\n") for l in open("input_test_1.txt")]
#lines_all = [l.rstrip("\n") for l in open("input_test_2.txt")]
#lines_all = [l.rstrip("\n") for l in open("input_test_3.txt")]
lines_rules = [l for l in lines_all if ":" in l]
lines_messages = [l for l in lines_all if ":" not in l and l != ""]

def parse_rules():
    rules = {}
    for l in lines_rules:
        idx, value = l.split(":")
        rules[idx] = value.strip()
    return rules

def to_regex(idx, rules, memory={}):
    if idx in memory: return memory[idx]
    options = rules[idx].split("|")
    re_options = []
    for po in options:
        re_option = ""
        #if len(options) != 1: re_option = "(?:"
        re_option = "(?:"
        parts = po.split()
        for p in parts:
            if p in "\"a\"b\"":
                re_option += p[1] # End of recursion.
            else:
                re_option += to_regex(p, rules, memory)
        #if len(options) != 1: re_option += ")"
        re_option += ")"
        re_options += [re_option]
    res = "|".join(re_options)
    if len(options) > 1: res = "(?:{})".format(res)
    memory[idx] = res
    return res

def part1():
    # Parse all rule lines to a lookup dict.
    rules = parse_rules()
    # Build a HUUUGE regex string!
    regex_string = "^{}$".format(to_regex("0", rules))
    #print(regex_string)
    r = regex.compile(regex_string)
    #for l in lines_messages:
    #    if r.match(l): print("MATCH: {}".format(l))
    #    else: print("NO MATCH: {}".format(l))
    return sum((1 for l in lines_messages if r.match(l)))

def part2():
    pass

#print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
