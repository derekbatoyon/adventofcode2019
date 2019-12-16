# usage:
#   python part1.py program_file

from threading import Thread

import astar
import operator
import os
import sys
import time

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

reverse = {
    north: south,
    south: north,
    west: east,
    east: west,
}

direction_str = {
    north: 'south',
    south: 'north',
    west: 'east',
    east: 'west',
}

message = "goal: "

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

def draw_map(map, location, goal, path=[]):
    global message

    values = [loc[0] for loc in map.iterkeys()]
    min_x = min(values)
    max_x = max(values)
    values = [loc[1] for loc in map.iterkeys()]
    min_y = min(values)
    max_y = max(values)

    os.write(sys.stdout.fileno(), '\x1B\x5B2J\x1B\x5BH')
    print message

    for y in range(min_y, max_y+1):
        line = ''
        for x in range(min_x, max_x+1):
            if (x, y) == goal:
                line += 'O'
            elif (x, y) == location:
                line += 'D'
            elif (x, y) in path:
                line += '.'
            elif (x, y) in map:
                line += ' '
            else:
                line += '#'
        print line

def move(input_fd, output_fd, dir):
    write_line(output_fd, dir)
    return read_line(input_fd)

def explore(input_fd, output_fd, map, location, directions):
    global message

    assert location not in map
    map[location] = set()
    goal = None
    for direction in directions:
        new_location = movement[direction](location)
        if new_location not in map:
            status = move(input_fd, output_fd, direction)
            if status > 0:
                if status == 2 and goal is None:
                    goal = new_location
                    message += str(goal)
                map[location].add(new_location)
                opposite_direction = reverse[direction]
                new_directions = all_directions[:]
                new_directions.remove(opposite_direction)
                g = explore(input_fd, output_fd, map, new_location, new_directions)
                if g is not None:
                    goal = g
                status = move(input_fd, output_fd, opposite_direction)
                assert status > 0
    draw_map(map, location, goal)
    time.sleep(0.25)
    return goal

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        program = load(fh)

    (droid_input, controller_output) = os.pipe()
    (controller_input, droid_output) = os.pipe()

    droid = Thread(target=run, args=(program, droid_input, droid_output))
    droid.start()

    start = (0,0)
    map = dict()
    goal = explore(controller_input, controller_output, map, start, all_directions)
    print >> sys.stderr, "found goal:", goal

    path = list(astar.find_path(start, goal, lambda n: map[n], lambda a,b: 1, lambda a,b: 1))
    draw_map(map, start, goal, path)
    print "steps:", len(path) - 1

    os.close(droid_input)
    os.close(controller_output)

    droid.join()
