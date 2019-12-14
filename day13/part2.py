# usage:
#   python part2.py program_file

from threading import Thread

import operator
import os
import sys

empty = 0 
wall = 1 
block = 2 
paddle = 3 
ball = 4 

tiles = {
    empty  : ' ',
    wall   : '#',
    block  : '=',
    paddle : '-',
    ball   : '@',
}

joystick_neutral = '0'
joystick_left = '-1'
joystick_right = '1'

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

def clear_screen():
    str = '\x1B\x5B2J'
    os.write(sys.stdout.fileno(), str)

def draw_tile(x, y, c):
    y += 2
    x += 1
    str = '\x1B\x5B{};{}H{}'.format(y, x, tiles[c])
    os.write(sys.stdout.fileno(), str)

def move_cursor(y):
    y += 2
    str = '\x1B\x5B{}H'.format(y)
    os.write(sys.stdout.fileno(), str)

def draw_score(s):
    str = '\x1B\x5B1;1HScore: {}\x1B\x5BK'.format(s)
    os.write(sys.stdout.fileno(), str)

def do_nothing(ball, padl):
    return joystick_neutral

def calculate_move(ball, padl):
    if ball > padl:
        return joystick_right
    elif ball < padl:
        return joystick_left
    else:
        return joystick_neutral

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        program = load(fh)

    (game_input, controller_output) = os.pipe()
    (screen_input, game_output) = os.pipe()

    clear_screen()
    draw_score(0)

    program[0] = 2
    game = Thread(target=run, args=(program, game_input, game_output))
    game.start()

    paddle_x = None

    infile = os.fdopen(screen_input)

    bottom = 0
    movement = do_nothing
    while True:
        x = infile.readline()
        if len(x) == 0:
            break
        y = infile.readline()
        if len(y) == 0:
            break
        t = infile.readline()
        if len(t) == 0:
            break

        x = int(x)
        y = int(y)
        bottom = max(bottom, y)

        if x == -1 and y == 0:
            draw_score(t.strip())
        else:
            tile = int(t)
            draw_tile(x, y, tile)

            if tile == ball:
                move = movement(x, paddle_x)
                movement = calculate_move
                write_line(controller_output, move)

            elif tile == paddle:
                paddle_x = x

    os.close(game_input)
    os.close(controller_output)

    game.join()

    move_cursor(bottom+1)
