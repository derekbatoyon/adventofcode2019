# usage:
#   python part2.py [x,y] [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.  If the focus is not
# specified in the input, then it must be given on the command line (via x,y).
# Otherwise, the input will take precedence.

import fileinput
import math
import re
import sys

def calculate_direction(p, q):
    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]
    direction = math.degrees(math.atan2(y2 - y1, x2 - x1)) + 90
    if direction < 0:
        direction =  direction + 360
    return direction

def calculate_distance(p, q):
    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]
    return math.sqrt(math.pow(y2 - y1, 2) + math.pow(x2 - x1, 2))

def load(fh):
    points = []
    focus = None
    for y, line in enumerate(fh):
        for x, character in enumerate(line):
            if character == '#':
                points.append((x, y))
            if character == 'X':
                focus = (x, y)
    return points, focus

def parse_focus(str):
    result = re.match('(\d+),(\d+)$', str)
    if result:
        return [int(i) for i in result.group(1, 2)]
    return None

if __name__ == "__main__":
    cmd_focus = None
    for index, arg in enumerate(sys.argv):
        cmd_focus = parse_focus(arg)
        if cmd_focus:
            del sys.argv[index]
            break

    points, focus = load(fileinput.input())
    if focus is None:
        focus = cmd_focus

    print >> sys.stderr, "focus:", focus

    vaporized = []

    while len(points) > 0:
        targets = {}
        for index, point in enumerate(points):
            direction = calculate_direction(focus, point)
            distance = calculate_distance(focus, point)
            if direction not in targets or distance < targets[direction][1]:
                targets[direction] = (index, distance)

        indices = []
        for key in sorted(targets.iterkeys()):
            target = targets[key]
            index = target[0]
            indices.append(index)
            vaporized.append(points[index])

        indices.sort()
        for index in reversed(indices):
            del points[index]

    for index, point in enumerate(vaporized, 1):
        print index, point
