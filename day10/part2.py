# usage:
#   python part2.py <map> [focus]

import math
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

def load(filename):
    points = []
    focus = None
    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            for x, character in enumerate(line):
                if character == '#':
                    points.append((x, y))
                if character == 'X':
                    focus = (x, y)
    return points, focus

if __name__ == "__main__":
    points, focus = load(sys.argv[1])
    if focus is None:
        focus = [int(i) for i in sys.argv[2].split(',')]

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
