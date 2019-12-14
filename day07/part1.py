# usage:
#   python part1.py program_file [phase_setting_sequence]
#
# If the phase setting sequence is omitted, the maximal setting is calculated.

import operator
import os
import sys

from threading import Thread

def write_line(fd, arg):
    os.write(fd, "{}\n".format(arg))

def load(fh):
    program = []
    for line in fh:
        for value in line.split(','):
            if len(value.strip()) > 0:
                program.append(int(value))
    return program

def position_mode(program, index):
    return program[index]

def immediate_mode(value):
    return value

def run(program, input_fd, output_fd):
    operators = {
        1: operator.add,
        2: operator.mul,
    }

    getters = {
        0: lambda param: position_mode(program, param),
        1: lambda param: immediate_mode(param),
    }

    infile = os.fdopen(os.dup(input_fd))

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
            program[result_index] = int(infile.readline())
            index = index + 2
        elif opcode == 4:
            write_line(output_fd, getters[mode1](program[index+1]))
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

def test(program, phases):
    inpipe = 0
    outpipe = 1
    pipes = [os.pipe() for i in range(len(phases)+1)]
    threads = []
    for i, phase in enumerate(phases):
        write_line(pipes[i][outpipe], phase)
        thread = Thread(target=run, args=(program[:], pipes[i][inpipe], pipes[i+1][outpipe]))
        thread.start()
        threads.append(thread)

    infile = os.fdopen(os.dup(pipes[-1][inpipe]))

    write_line(pipes[0][outpipe], 0)
    result = infile.readline()

    for thread in threads:
        thread.join()

    for pipe in pipes:
        os.close(pipe[inpipe])
        os.close(pipe[outpipe])

    return int(result)

def permutations(sequence, length=None):
    if length is None:
        length = len(sequence)
    if length == 1:
        for x in sequence:
            yield [x]
    else:
        for i, x in enumerate(sequence):
            subsequence = sequence[:]
            del subsequence[i]
            for s in permutations(subsequence, length-1):
                yield [x] + s

def parse(str):
    return [int(c) for c in str.split(',')]

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        program = load(fh)

    if len(sys.argv) > 2:
        phases = parse(sys.argv[2])
        print test(program, phases)
    else:
        max = 0
        for phases in permutations([0,1,2,3,4]):
            result = test(program, phases)
            if result > max:
                max = result
        print max
