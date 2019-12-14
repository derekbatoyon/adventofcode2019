# usage:
#   python part2.py [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.

import fileinput
import functools
import operator

def calculate(arg):
    mass = int(arg.strip())
    total = 0
    while True:
        fuel = mass // 3 - 2
        if fuel <= 0:
            break
        total += fuel
        mass = fuel
    return total

if __name__ == "__main__":
    print functools.reduce(operator.add, [calculate(arg) for arg in fileinput.input()])
