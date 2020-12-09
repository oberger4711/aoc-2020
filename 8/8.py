#!/usr/bin/env python3

loc = [l.rstrip("\n") for l in open("input.txt")]

# Maybe this assembler stuff will be used in future days too, therefore I made a class.
class Processor:
    def parse(loc):
        prog = []
        for l in loc:
            opcode, arg_s = l.split()
            prog += [(opcode, int(arg_s))]
        return prog

    def __init__(self, loc):
        self.ip = 0 # instruction pointer
        self.accumulator = 0
        self.program = Processor.parse(loc)
        self.instruction_set = {}

    def add_instruction(self, opcode, operation):
        self.instruction_set[opcode] = operation

    def interpret_instruction(self):
        if self.ip < 0 or self.ip > len(self.program):
            raise RuntimeError("IP {} is out of range [0, {}].".format(self.ip, len(self.program)))
        opcode, arg = self.program[self.ip]
        #print("{} {}".format(opcode, arg))
        if opcode in self.instruction_set:
            self.instruction_set[opcode](self, arg)
        else:
            raise RuntimeError("Unknown instruction at instruction {}: {}".format(self.ip, opcode))

    def reset_state(self):
        self.ip = 0
        self.accumulator = 0

    def at_end_of_program(self):
        return self.ip == len(self.program)

def nop(proc, arg):
    proc.ip += 1

def acc(proc, arg):
    proc.accumulator += arg
    proc.ip += 1

def jmp(proc, arg):
    proc.ip += arg

def make_processor(loc):
    proc = Processor(loc)
    proc.add_instruction("nop", nop)
    proc.add_instruction("acc", acc)
    proc.add_instruction("jmp", jmp)
    return proc

def part1():
    proc = make_processor(loc)
    ip_history = [False] * len(loc)
    while not proc.at_end_of_program():
        if ip_history[proc.ip]:
            return proc.accumulator # Endless loop
        ip_history[proc.ip] = True
        proc.interpret_instruction()

def part2():
    proc = make_processor(loc)
    for i, (opcode_original, arg) in enumerate(proc.program):
        if opcode_original == "acc": continue
        # Swap nop or jmp.
        elif opcode_original == "nop": proc.program[i] = ("jmp", arg)
        elif opcode_original == "jmp": proc.program[i] = ("nop", arg)
        proc.reset_state()
        ip_history = [False] * len(loc)
        while not proc.at_end_of_program():
            if ip_history[proc.ip]:
                break # Endless loop
            ip_history[proc.ip] = True
            proc.interpret_instruction()
        else:
            return proc.accumulator
        # Undo swap.
        proc.program[i] = (opcode_original, arg)

print("Part 1: {}".format(part1()))
print("Part 2: {}".format(part2()))
