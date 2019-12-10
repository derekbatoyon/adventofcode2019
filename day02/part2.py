# usage:
#   python part2.py < <program>

import operator
import sys

def load(file):
    program = []
    lines = file.readlines()
    for line in lines:
        for value in line.split(','):
            value = value.strip()
            if (len(value) > 0):
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

def test(program):
    for noun in range(0, 100):
        for verb in range(0, 100):
            program2 = program[:]
            program2[1] = noun
            program2[2] = verb
            run(program2)
            if program2[0] == 19690720:
                return noun * 100 + verb
    return None

if __name__ == "__main__":
    program = load(sys.stdin)
    result = test(program)
    if result:
        print result
    else:
        print "answer was not found"
