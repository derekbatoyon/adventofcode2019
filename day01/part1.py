# usage: python part1.py < <list of modules>

import functools
import operator
import sys

def calculate(arg):
    return int(arg.strip()) // 3 - 2;

if __name__ == "__main__":
    print functools.reduce(operator.add, [calculate(arg) for arg in sys.stdin])
