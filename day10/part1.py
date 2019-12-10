# usage:
#   python part1.py <map>

import sys

north = 0
northeast = 1
east = 2
southeast = 3
south = 4
southwest = 5
west = 6
northwest = 7

def general_direction(p, q):
    x1 = p[0]
    y1 = p[1]
    x2 = q[0]
    y2 = q[1]
    if x1 == x2 and y1 > y2:
        return north
    if x1 == x2 and y1 < y2:
        return south
    if x1 < x2 and y1 == y2:
        return east
    if x1 > x2 and y1 == y2:
        return west
    if x1 < x2 and y1 > y2:
        return northeast
    if x1 > x2 and y1 > y2:
        return northwest
    if x1 < x2 and y1 < y2:
        return southeast
    if x1 > x2 and y1 < y2:
        return southwest
    raise ValueError

class ray:
    def __init__(self, p, q):
        self.p = p
        x1 = p[0]
        y1 = p[1]
        x2 = q[0]
        y2 = q[1]
        self.a = y1 - y2
        self.b = x2 - x1
        self.c = x1 * y2 - x2 * y1
        self.direction = general_direction(p, q)

    def hit_test(self, q):
        x = q[0]
        y = q[1]
        return self.a * x + self.b * y + self.c == 0 and self.direction == general_direction(self.p, q)

def load(filename):
    points = []
    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            for x, character in enumerate(line):
                if character == '#':
                    points.append((x, y))
    return points

def detect(p, points):
    lines = [ray(p, points[0])]
    for q in points[1:]:
        unique = True
        for line in lines:
            if line.hit_test(q):
                unique = False
                break
        if unique:
            lines.append(ray(p, q))
    return len(lines)

if __name__ == "__main__":
    points = load(sys.argv[1])

    max_detected = 0
    max_point = None
    for index, point in enumerate(points):
        others = points[:index] + points[index+1:]
        detected = detect(point, others)
        if detected > max_detected:
            max_detected = detected
            max_point = point
    print max_point
    print max_detected 
