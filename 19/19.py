 #!/usr/bin/env python3

import re

REPS = 20

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

def to_regex(idx, rules, memory):
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
    regex_string = "^{}$".format(to_regex("0", rules, {}))
    #print(regex_string)
    r = re.compile(regex_string)
    #for l in lines_messages:
    #    if r.match(l): print("MATCH: {}".format(l))
    #    else: print("NO MATCH: {}".format(l))
    return sum((1 for l in lines_messages if r.match(l)))

def part2():
    rules = parse_rules()
    # Just create more rules so that most cases.
    idx_next_rule = max((int(k) for k in rules.keys())) + 1
    # 8: 42 | 42 8
    rules["8"] = "42 | {}".format(idx_next_rule)
    #print("{}: {}".format(8, rules["8"]))
    for reps in range(2, REPS + 1):
        new_rule = "{}| {}".format("42 " * reps, idx_next_rule + 1)
        rules[str(idx_next_rule)] = new_rule
        #print("{}: {}".format(idx_next_rule, new_rule))
        idx_next_rule += 1
    rules[str(idx_next_rule)] = "42" # Dummy
    idx_next_rule += 1
    # 11: 42 31 | 42 11 31
    rules["11"] = "42 31 | {}".format(idx_next_rule)
    #print("{}: {}".format(11, rules["11"]))
    for reps in range(2, REPS + 1):
        new_rule = "{}| {}".format(("42 " * reps) + ("31 " * reps), idx_next_rule + 1)
        rules[str(idx_next_rule)] = new_rule
        #print("{}: {}".format(idx_next_rule, new_rule))
        idx_next_rule += 1
    rules[str(idx_next_rule)] = "42 31"
    idx_next_rule += 1
    # Build an even HUUUGER regex string than in part 1!
    regex_string = "^{}$".format(to_regex("0", rules, {}))
    #print(regex_string) # You better do not do this!!
    r = re.compile(regex_string)
    #for l in lines_messages:
    #    if r.match(l): print("MATCH: {}".format(l))
    #    else: print("NO MATCH: {}".format(l))
    return sum((1 for l in lines_messages if r.match(l)))

def part2_did_not_work():
    # Parse all rule lines to a lookup dict.
    rules = parse_rules()
    # Manipulate memory with the special rules for part 2.
    # This is hacky but should work to the the solution.
    # Use named groups to check that number of 42 and 31 are the same.
    regex_memory = {}
    # 8: 42 | 42 8
    to_regex("8", rules, regex_memory) # Load 8 and 42 to memory.
    regex_memory["8"] = regex_memory["8"] + "+"
    # 11: 42 31 | 42 11 31
    to_regex("31", rules, regex_memory) # Load 31 to memory.
    # Now change previously loaded 42 and 31 to use named groups.
    # This will then only apply to the following to_regex() calls and therefore only to rule 11.
    regex_memory["42"] = regex_memory["42"] + "+"
    regex_memory["31"] = regex_memory["31"] + "+"
    # Build a HUUUGE regex string again!
    regex_string = "^{}$".format(to_regex("0", rules, regex_memory))
    print(regex_string)
    r = re.compile(regex_string)
    r_left_single = re.compile("^" + to_regex("42", rules, regex_memory)[:-1]) # Remove +
    r_right_single = re.compile(to_regex("31", rules, regex_memory)[:-1] + "$") # Remove +
    total = 0
    for l in lines_messages:
        print(l)
        m = r.match(l)
        if m is not None:
            l_lstripped = l
            count_42, subs = 0, 1
            while subs > 0:
                l_lstripped, subs = re.subn(r_left_single, "", l_lstripped)
                if subs > 1: raise RuntimeError("This should not happen.")
                count_42 += subs

            l_rstripped = l
            count_31, subs = 0, 1
            while subs > 0:
                l_rstripped, subs = re.subn(r_right_single, "", l_rstripped)
                if subs > 1: raise RuntimeError("This should not happen.")
                count_31 += subs
            if count_42 == 0 or count_31 == 0:
                raise RuntimeError("This should not happen.")
            if count_42 > count_31:
                print("MATCH: {}".format(l))
            total += 1
        else:
            print("NO MATCH: {}".format(l))
    return total

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
