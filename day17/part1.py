# usage:
#   python part1.py program_file

from threading import Thread

import operator
import os
import sys

empty = 46
north = 1
south = 2
west = 3
east = 4
all_directions = [north, east, south, west]

movement = {
    north: lambda l: (l[0], l[1] - 1),
    south: lambda l: (l[0], l[1] + 1),
    west:  lambda l: (l[0] - 1, l[1]),
    east:  lambda l: (l[0] + 1, l[1]),
}

direction_str = {
    north: 'south',
    south: 'north',
    west: 'east',
    east: 'west',
}

def write_line(fd, arg):
    os.write(fd, "{}\n".format(arg))

def read_line(fd):
    c = ''
    while c not in ['0', '1', '2']:
        c = os.read(fd, 1)
    return int(c)

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

def run(program, input_fd, output_fd):
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

    if input_fd:
        infile = os.fdopen(os.dup(input_fd))
    else:
        infile = None

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
            inp = infile.readline()
            if len(inp) == 0:
                break
            setters[mode1](result_index, int(inp))
            index = index + 2
        elif opcode == 4:
            write_line(output_fd, str(getters[mode1](program[index+1])))
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

    if output_fd:
        os.close(output_fd)

def load_map(fh):
    map = dict()
    x = y = 0
    for data in [int(n) for n in fh]:
        if data == 10:
            x = 0
            y += 1
        else:
            if data != empty:
                map[(x, y)] = data
            x += 1
    return map

def draw_map(map):
    values = [loc[0] for loc in map.iterkeys()]
    min_x = min(values)
    max_x = max(values)
    values = [loc[1] for loc in map.iterkeys()]
    min_y = min(values)
    max_y = max(values)

    os.write(sys.stdout.fileno(), '\x1B\x5B2J\x1B\x5BH')

    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            if (x, y) in map:
                line.append(map[(x, y)])
            else:
                line.append(empty)
        print ''.join([chr(x) for x in line])

def analyze_map(map):
    total = 0
    for x, y in map.iterkeys():
        if all([movement[dir]((x, y)) in map for dir in all_directions]):
            total += x * y
    return total

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        program = load(fh)

    (controller_input, camera_output) = os.pipe()

    assert program[0] == 1
    camera = Thread(target=run, args=(program, None, camera_output))
    camera.start()

    map = load_map(os.fdopen(controller_input))
    draw_map(map)
    print analyze_map(map)

    camera.join()
