# usage:
#   python part1.py <program file> <phase setting sequence>
#
# run like:
#   python permutations.py | xargs -n 1 python part1.py input.txt | sort --numeric-sort
#
# (last line of result is correct result)

import operator
import os
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

def position_mode(program, index):
    return program[index]

def immediate_mode(value):
    return value

def run(program):
    operators = {
        1: operator.add,
        2: operator.mul,
    }

    getters = {
        0: lambda param: position_mode(program, param),
        1: lambda param: immediate_mode(param),
    }

    index = 0
    while True:
        instruction = program[index]
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
            value1 = getters[mode1](program[index+1])
            value2 = getters[mode2](program[index+2])
            result_index = program[index+3]
            program[result_index] = op(value1, value2)
            index = index + 4
        elif opcode == 3:
            result_index = program[index+1]
            inp = sys.stdin.readline()
            program[result_index] = int(inp)
            index = index + 2
        elif opcode == 4:
            print getters[mode1](program[index+1])
            index = index + 2
        elif opcode == 5:
            value1 = getters[mode1](program[index+1])
            value2 = getters[mode2](program[index+2])
            if value1:
                index = value2
            else:
                index = index + 3
        elif opcode == 6:
            value1 = getters[mode1](program[index+1])
            value2 = getters[mode2](program[index+2])
            if value1 == 0:
                index = value2
            else:
                index = index + 3
        elif opcode == 7:
            value1 = getters[mode1](program[index+1])
            value2 = getters[mode2](program[index+2])
            result_index = program[index+3]
            result = 0
            if value1 < value2:
                result = 1
            program[result_index] = result
            index = index + 4
        elif opcode == 8:
            value1 = getters[mode1](program[index+1])
            value2 = getters[mode2](program[index+2])
            result_index = program[index+3]
            result = 0
            if value1 == value2:
                result = 1
            program[result_index] = result
            index = index + 4
        else:
            pass

def read_all(fd):
    str = ""
    s = os.read(fd, 1)
    while len(s) > 0:
        if s.isspace():
            break
        str = str + s
        s = os.read(fd, 1)
    return str

def test(program, phases):
    input = 0
    output = 1
    pipes = [os.pipe() for i in range(len(phases)+1)]
    for i, phase in enumerate(phases):
        if os.fork() == 0:
            os.dup2(pipes[i][input], sys.stdin.fileno())
            os.dup2(pipes[i+1][output], sys.stdout.fileno())
            run(program)
            sys.exit(0)
        else:
            os.write(pipes[i][output], "{}\n".format(phase))

    os.write(pipes[0][output], "{}\n".format(0))
    result = read_all(pipes[-1][input])

    for pipe in pipes:
        os.close(pipe[input])
        os.close(pipe[output])

    return int(result)

def parse(str):
    return [int(c) for c in str.split(',')]

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        program = load(file)

    phases = parse(sys.argv[2])
    print test(program, phases)
