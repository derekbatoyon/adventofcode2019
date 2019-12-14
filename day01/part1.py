# usage:
#   python part1.py [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.

import fileinput
import functools
import operator

def calculate(arg):
    return int(arg.strip()) // 3 - 2;

if __name__ == "__main__":
    print functools.reduce(operator.add, [calculate(arg) for arg in fileinput.input()])
