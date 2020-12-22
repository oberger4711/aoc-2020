#!/usr/bin/env python3

p1_inp, p2_inp = open("input.txt").read().split("\n\n")
#p1_inp, p2_inp = open("input_test_1.txt").read().split("\n\n")
#p1_inp, p2_inp = open("input_test_2.txt").read().split("\n\n")
# Get rid of headers:
p1_inp = p1_inp[len("Player 1:\n"):].strip()
p2_inp = p2_inp[len("Player 2:\n"):].strip()

p1_stack_start = [int(l) for l in p1_inp.split("\n")]
p2_stack_start = [int(l) for l in p2_inp.split("\n")]

def part1():
    p1_stack = list(p1_stack_start)
    p2_stack = list(p2_stack_start)
    while len(p1_stack) > 0 and len(p2_stack) > 0:
        #print("\n" * 3)
        #print("p1 stack:")
        #print(p1_stack)
        #print("p2 stack:")
        #print(p2_stack)
        # Play a round.
        p1_top = p1_stack[0]
        p1_stack = p1_stack[1:]
        p2_top = p2_stack[0]
        p2_stack = p2_stack[1:]
        if p1_top > p2_top:
            #print("p1 wins")
            p1_stack = p1_stack + [p1_top, p2_top]
            winner_stack = p1_stack
        else:
            #print("p2 wins")
            p2_stack = p2_stack + [p2_top, p1_top]
            winner_stack = p2_stack
        #print(p1_stack)
        #print(p2_stack)
    return sum(f * v for f, v in zip(range(len(winner_stack), 0, -1), winner_stack))

def part2():
    p1_stack = list(p1_stack_start)
    p2_stack = list(p2_stack_start)
    def play_game(p1_stack, p2_stack, depth=0):
        #print("Game {}".format(depth))
        p1_stack_history = set()
        p2_stack_history = set()
        while len(p1_stack) > 0 and len(p2_stack) > 0:
            #print("\n" * 3)
            #print("p1 stack:")
            #print(p1_stack)
            #print("p2 stack:")
            #print(p2_stack)
            winner = None
            if tuple(p1_stack) in p1_stack_history and tuple(p2_stack) in p2_stack_history:
                #print("infinite rule triggered")
                return 1, p1_stack
            p1_stack_history.add(tuple(p1_stack))
            p2_stack_history.add(tuple(p2_stack))
            # Play a round.
            p1_top = p1_stack[0]
            p1_stack = p1_stack[1:]
            p2_top = p2_stack[0]
            p2_stack = p2_stack[1:]
            if len(p1_stack) >= p1_top and len(p2_stack) >= p2_top:
                # Recursion
                #print("recursion")
                winner, _ = play_game(list(p1_stack[:p1_top]), list(p2_stack[:p2_top]), depth + 1)
            else:
                # Normal round
                #print("normal round")
                if p1_top > p2_top:
                    winner = 1
                else:
                    winner = 2

            if winner == 1:
                #print("p1 wins")
                p1_stack = p1_stack + [p1_top, p2_top]
                winner_stack = p1_stack
            else:
                #print("p2 wins")
                p2_stack = p2_stack + [p2_top, p1_top]
                winner_stack = p2_stack
        #print("Game over, winner: ", winner)
        return winner, winner_stack

    _, winner_stack = play_game(p1_stack, p2_stack)
    return sum(f * v for f, v in zip(range(len(winner_stack), 0, -1), winner_stack))

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
