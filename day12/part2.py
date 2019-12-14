# usage:
#   python part2.py <positions>

import fractions
import functools
import re
import sys

def parse(string):
    result = re.match('<x=([+-]?\d+),\s*y=([+-]?\d+),\s*z=([+-]?\d+)>', string)
    return [int(i) for i in result.group(1, 2, 3)]

def load(filename):
    with open(filename, 'r') as fh:
        positions = [parse(line) for line in fh]
    return positions

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
    positions = load(sys.argv[1])
    d = len(positions[0])

    periods = []
    for axis in range(d):
        periods.append(simulate([pos[axis] for pos in positions]))

    print functools.reduce(lcm, periods)
