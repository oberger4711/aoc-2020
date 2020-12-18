#!/usr/bin/env python3

lines = [l.rstrip("\n") for l in open("input.txt")]

def find_closing_parenthesis(expr, i_start):
    depth = 1
    for i, c_search in enumerate(expr[i_start+1:]):
        if c_search == "(":
            depth += 1
        elif c_search == ")":
            depth -= 1
            if depth == 0:
                return i_start + i + 1
    else:
        print("Paranthesis not closed in {}".format(expr))
        exit(1)



def part1():
    def calc(expr):
        #print("<expr start: {}>".format(expr))
        res = 0
        operator = "+"
        i = 0
        while i < len(expr):
            c = expr[i]
            #if c != " ": print(" " + c)
            if c in "0123456789(":
                # Determine operand.
                if c == "(":
                    # Find closing parenthesis.
                    i_end = find_closing_parenthesis(expr, i)
                    sub_expr = expr[i+1:i_end]
                    operand = calc(sub_expr)
                    i = i_end # Skip evaluated sub expression.
                else:
                    operand = int(c)
                # Apply operator.
                if operator == "+": res += operand
                elif operator == "*": res *= operand
                else:
                    print("No operator in expression {}".format(expr))
                    exit(1)
                operator = None
            elif c in "+*":
                operator = c
            i += 1
        #print("<expr end: {} = {}>".format(expr, res))
        return res
    # Tests
    #print(calc("2 * 3 + (4 * 5)"))
    #print(calc("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
    #print(calc("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
    #print(calc("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))
    return sum((calc(l) for l in lines))

def part2():
    # New concept for part 2: parse first, divide in sub expressions and then calc from left to right as before.
    def calc_left_to_right(expr):
        #print("<expr start>")
        #print(expr)
        res = 0
        operator = "+"
        for i, pos in enumerate(expr):
            if i % 2 == 0:
                # Determine operand.
                if isinstance(pos, list): operand = calc_left_to_right(pos)
                else: operand = pos
                # Apply operator.
                if operator == "+": res += operand
                elif operator == "*": res *= operand
                else:
                    print("No operator in expression {}".format(expr))
                    exit(1)
                operator = None
            else:
                if pos not in "+*":
                    print("No operator at {} in expression:".format(i))
                    exit(1)
                operator = pos
        #print("<expr end>")
        #print(expr)
        return res

    def parse(expr):
        #print("<expr start: {}>".format(expr))
        parsed_expr = []
        i = 0
        while i < len(expr):
            c = expr[i]
            if c == "(":
                i_end = find_closing_parenthesis(expr, i)
                parsed_expr += [parse(expr[i+1:i_end])]
                i = i_end # Skip evaluated sub expression.
            elif c in "0123456789":
                parsed_expr += [int(c)]
            elif c in "*+":
                parsed_expr += [c]
            i += 1
        # Now take care of + before * on the current level only.
        # Just put them in an expression for their own.
        i = 1 # Iterator through operators only.
        while i < len(parsed_expr):
            operator_i = parsed_expr[i]
            if operator_i == "+":
                # Replace the whole sum by a new sub expression.
                i_start, i_end = i - 1, i + 2
                for j in range(i, len(parsed_expr), 2):
                    operator_j = parsed_expr[j]
                    if operator_j == "+":
                        i_end = j + 2
                    else: break
                replacement_expr = list(parsed_expr[i_start:i_end])
                parsed_expr = parsed_expr[:i_start] + [parsed_expr[i_start:i_end]] + parsed_expr[i_end:]
            else:
                if operator_i != "*":
                    print("No operator at position {} in expression:".format(i))
                    print(parsed_expr)
                    exit(1)
                i += 2
        #print("<expr end: {} >".format(expr))
        #print(parsed_expr)
        return parsed_expr

    def parse_and_calc(expr):
        #print("## parse")
        parsed_expr = parse(expr)
        #print("## calc")
        return calc_left_to_right(parsed_expr)
    #print(parse_and_calc("1 + (2 * 3) + (4 * (5 + 6))"))
    #print(parse_and_calc("2 * 3 + (4 * 5)"))
    #print(parse_and_calc("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
    #print(parse_and_calc("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
    #print(parse_and_calc("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))
    return sum((parse_and_calc(l) for l in lines))

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
