# usage:
#   python part2.py <program> [output image]

from PIL import Image
from threading import Thread

import operator
import os
import sys

black = 0
white = 1

color_character = {
    black: '#',
    white: ' ',
}

color_rgba = {
    black: (0, 0, 0, 255),
    white: (255, 255, 255, 255),
}

face_up = 0
face_right = 1
face_down = 2
face_left = 3

def move(location, orientation):
    x = location[0]
    y = location[1]
    movement = {
        face_up:    lambda x, y: (x,     y - 1),
        face_right: lambda x, y: (x + 1, y    ),
        face_down:  lambda x, y: (x,     y + 1),
        face_left:  lambda x, y: (x - 1, y    ),
    }
    return movement[orientation](x, y)

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
            input = os.read(input_fd, 1)
            setters[mode1](result_index, int(input))
            index = index + 2
        elif opcode == 4:
            os.write(output_fd, str(getters[mode1](program[index+1])))
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

    os.close(output_fd)

def get_color(colors, location):
    try:
        color = colors[location]
    except KeyError:
        color = black
    return color

def noop():
    pass

def print_character(fh, color=None):
    if color is None:
        print >> fh
    else:
        print >> fh, color_character[color],

def paint_pixel(im, scale, x, y, color):
    for i in range(scale):
        for j in range(scale):
            px = x * scale + i
            py = y * scale + j
            im.putpixel((px, py), color_rgba[color])

def create_image(destination, colors):
    values = [loc[0] for loc in colors.iterkeys()]
    min_x = min(values)
    max_x = max(values)
    values = [loc[1] for loc in colors.iterkeys()]
    min_y = min(values)
    max_y = max(values)

    if isinstance(destination, basestring):
        scale = 16
        width  = (max_x - min_x + 1) * scale
        height = (max_y - min_y + 1) * scale
        im = Image.new('RGBA', (width, height))
        paint = lambda x, y, color: paint_pixel(im, scale, x - min_x, y - min_y, color)
        newline = noop
    else:
        im = None
        paint = lambda x, y, color: print_character(destination, color)
        newline = lambda: print_character(destination)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            color = get_color(colors, (x, y))
            paint(x, y, color)
        newline()

    if im:
        im.save(destination)

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        program = load(file)

    (robot_input, program_output) = os.pipe()
    (program_input, robot_output) = os.pipe()

    thread = Thread(target=run, args=(program, program_input, program_output))
    thread.start()

    left_turn = 0
    left_turns = {
        face_up: face_left,
        face_left: face_down,
        face_down: face_right,
        face_right: face_up,
    }
    right_turn = 1
    right_turns = {
        face_up: face_right,
        face_right: face_down,
        face_down: face_left,
        face_left: face_up,
    }

    orientation = face_up

    location = (0, 0)
    colors = { location: white }

    os.write(robot_output, str(colors[location]))

    while True:
        input = os.read(robot_input, 1)
        if input == '':
            break
        color = int(input)

        input = os.read(robot_input, 1)
        if input == '':
            break
        turn = int(input)

        colors[location] = color

        if turn == left_turn:
            orientation = left_turns[orientation]
        elif turn == right_turn:
            orientation = right_turns[orientation]
        else:
            raise ValueError

        location = move(location, orientation)
        color = get_color(colors, location)
        os.write(robot_output, str(color))

    thread.join()

    os.close(program_input)
    os.close(robot_input)
    os.close(robot_output)

    if len(sys.argv) > 2:
        create_image(sys.argv[2], colors)
    else:
        create_image(sys.stdout, colors)
