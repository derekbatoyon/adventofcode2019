# usage: python part2.py < <list of modules>

import functools
import operator
import sys

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
    print functools.reduce(operator.add, [calculate(arg) for arg in sys.stdin])
