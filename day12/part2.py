# usage:
#   python part2.py <positions>

import operator
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

def compute_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n /= 2
    d = 3
    while n > 1:
        if n % d == 0:
            factors.append(d)
            n /= d
        elif d*d > n:
            factors.append(n)
            break
        else:
            d += 2
    return factors

def combine_factors(list1, list2):
    unique = list1[:]
    for item in list2:
        try:
            unique.remove(item)
        except ValueError:
            list1.append(item)

if __name__ == "__main__":
    positions = load(sys.argv[1])
    d = len(positions[0])

    factors = []
    for axis in range(d):
        period = simulate([pos[axis] for pos in positions])
        combine_factors(factors, compute_factors(period))

    print reduce(operator.mul, factors)
