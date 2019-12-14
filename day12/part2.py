# usage:
#   python part2.py [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.

import fileinput
import fractions
import functools
import re
import sys

def parse(string):
    result = re.match('<x=([+-]?\d+),\s*y=([+-]?\d+),\s*z=([+-]?\d+)>', string)
    return [int(i) for i in result.group(1, 2, 3)]

def load(fh):
    return [parse(line) for line in fh]

def pairs(n):
    p = []
    while n > 1:
        n -= 1
        for second in range(n):
            p.append((n, second))
    return p

def compare(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def simulate(coordinates):
    starting_coordinates = coordinates[:]
    n = len(coordinates)
    speeds = [0] * n
    p = pairs(n)
    steps = 0
    while True:
        for i, j in p:
            delta = compare(coordinates[i], coordinates[j])
            speeds[i] -= delta
            speeds[j] += delta

        for i in range(n):
            coordinates[i] += speeds[i]

        steps += 1
        if coordinates == starting_coordinates and speeds == [0] * n:
            break

    return steps

def lcm(a,b):
    return (a*b) / fractions.gcd(a,b)

if __name__ == "__main__":
    positions = load(fileinput.input())
    d = len(positions[0])

    periods = []
    for axis in range(d):
        periods.append(simulate([pos[axis] for pos in positions]))

    print functools.reduce(lcm, periods)
