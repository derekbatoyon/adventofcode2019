# usage:
#   python part1.py <map>

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

def load(filename):
    points = []
    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            for x, character in enumerate(line):
                if character == '#':
                    points.append((x, y))
    return points

if __name__ == "__main__":
    points = load(sys.argv[1])

    max_detected = 0
    max_point = None

    for focus in points:
        directions = set()
        for point in points:
            if focus == point:
                continue
            directions.add(calculate_direction(focus, point))
        detected = len(directions)
        if detected > max_detected:
            max_detected = detected
            max_point = focus

    print max_point
    print max_detected
