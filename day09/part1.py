# usage:
#   python part1.py program_file
#
# The program may read from stdin and write to stdout.

import operator
import sys

def load(fh):
    program = []
    for line in fh:
        for value in line.split(','):
            if len(value.strip()) > 0:
                program.append(int(value))
    return program

def position_mode(program, index):
    if index < 0:
        raise ValueError("invalid index: {}".format(index))
    try:
        return program[index]
    except IndexError:
        return 0

def immediate_mode(value):
    return value

def store(program, index, value):
    if index < 0:
        raise ValueError("invalid index: {}".format(index))
    try:
        program[index] = value
    except IndexError:
        extra = index - len(program) + 1
        program.extend([0] * extra)
        program[index] = value

def run(program):
    relative_base = 0

    operators = {
        1: operator.add,
        2: operator.mul,
    }

    getters = {
        0: lambda param: position_mode(program, param),
        1: lambda param: immediate_mode(param),
        2: lambda param: position_mode(program, relative_base + param),
    }

    setters = {
        0: lambda i, v: store(program, i, v),
        2: lambda i, v: store(program, i + relative_base, v),
    }

    get = lambda i: position_mode(program, i)

    index = 0
    while True:
        instruction = get(index)
        opcode = instruction % 100
        instruction = instruction / 100
        mode1 = instruction % 10
        instruction = instruction / 10
        mode2 = instruction % 10
        instruction = instruction / 10
        mode3 = instruction % 10

        if opcode == 99:
            break
        elif opcode in (1, 2):
            op = operators[opcode]
            value1 = getters[mode1](get(index+1))
            value2 = getters[mode2](get(index+2))
            result_index = get(index+3)
            setters[mode3](result_index, op(value1, value2))
            index = index + 4
        elif opcode == 3:
            result_index = get(index+1)
            inp = sys.stdin.readline()
            setters[mode1](result_index, int(inp))
            index = index + 2
        elif opcode == 4:
            print getters[mode1](get(index+1))
            index = index + 2
        elif opcode == 5:
            value1 = getters[mode1](get(index+1))
            value2 = getters[mode2](get(index+2))
            if value1:
                index = value2
            else:
                index = index + 3
        elif opcode == 6:
            value1 = getters[mode1](get(index+1))
            value2 = getters[mode2](get(index+2))
            if value1 == 0:
                index = value2
            else:
                index = index + 3
        elif opcode == 7:
            value1 = getters[mode1](get(index+1))
            value2 = getters[mode2](get(index+2))
            result_index = get(index+3)
            result = 0
            if value1 < value2:
                result = 1
            setters[mode3](result_index, result)
            index = index + 4
        elif opcode == 8:
            value1 = getters[mode1](get(index+1))
            value2 = getters[mode2](get(index+2))
            result_index = get(index+3)
            result = 0
            if value1 == value2:
                result = 1
            setters[mode3](result_index, result)
            index = index + 4
        elif opcode == 9:
            relative_base += getters[mode1](get(index+1))
            index = index + 2
        else:
            raise RuntimeError("illegal opcode {}".format(opcode))

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        program = load(fh)
    run(program)
