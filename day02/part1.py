# usage:
#   python part1.py program_file

import operator
import sys

def load(fh):
    program = []
    for line in fh:
        for value in line.split(','):
            if len(value.strip()) > 0:
                program.append(int(value))
    return program

def run(program):
    operators = {
        1: operator.add,
        2: operator.mul,
    }

    index = 0
    while True:
        opcode = program[index]
        if opcode == 99:
            break
        else:
            op = operators[opcode]
            operand_index1 = program[index+1]
            operand_index2 = program[index+2]
            result_index   = program[index+3]
            program[result_index] = op(program[operand_index1], program[operand_index2])
            index = index + 4

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        program = load(fh)
    run(program)
    print program
