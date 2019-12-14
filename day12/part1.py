# usage:
#   python part1.py [-n] [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.  The n argument specifies
# the number of steps to simulate (default: 10)

import fileinput
import re
import sys

def parse(string):
    result = re.match('<x=([+-]?[0-9]*), y=([+-]?[0-9]*), z=([+-]?[0-9]*)>', string)
    return tuple(int(i) for i in result.group(1, 2, 3))

def load(fh):
    return {index: parse(line) for index, line in enumerate(fh)}

def pairs(items):
    while len(items) > 1:
        first = items[0]
        items = items[1:]
        for second in items:
            yield (first, second)

def dump(step, positions, velocities):
    print 'After {} steps:'.format(step)
    for pos, vel in zip(positions.itervalues(), velocities.itervalues()):
        print 'pos=<x={0:3d}, y={1:3d}, z={2:3d}>,'.format(pos[0], pos[1], pos[2]),
        print 'vel=<x={0:3d}, y={1:3d}, z={2:3d}>'.format(vel[0], vel[1], vel[2])

def compare(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

if __name__ == "__main__":
    steps = 10
    steps_re = re.compile('-(\d*)$')
    for index, arg in enumerate(sys.argv):
        result = steps_re.match(arg)
        if result:
            steps = int(result.group(1))
            del sys.argv[index]
            break

    positions = load(fileinput.input())
    n = len(positions)
    velocities = { i: (0, 0, 0) for i in range(n) }

    dump(0, positions, velocities)
    for step in range(1, steps+1):
        for i, j in pairs(range(n)):
            delta = [compare(a, b) for a, b in zip(positions[i], positions[j])]
            velocities[i] = tuple([v - d for v, d in zip(velocities[i], delta)])
            velocities[j] = tuple([v + d for v, d in zip(velocities[j], delta)])

        for i in range(n):
            positions[i] = tuple([p + v for p, v in zip(positions[i], velocities[i])])

        dump(step, positions, velocities)

    total_sum = 0
    for pos, vel in zip(positions.itervalues(), velocities.itervalues()):
        pot = sum([abs(p) for p in pos])
        kin = sum([abs(v) for v in vel])
        total = pot * kin
        total_sum += total
    print 'Sum of total energy:', total_sum
