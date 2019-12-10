# usage:
#   python part2.py < <wires>
# (two wires, each on a separate line)

import functools
import operator
import sys

class segment:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.x1 = p[0]
        self.y1 = p[1]
        self.x2 = q[0]
        self.y2 = q[1]
    def __str__(self):
        return "{} {}".format( (self.x1, self.y1), (self.x2, self.y2) )
    def containsPoint(self, point):
        if self.x1 == self.x2 == point[0]:
            return True
        if self.y1 == self.y2 == point[1]:
            return True
        return False

def manhattan(p, q = (0,0)):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def up(p, d):
    return (p[0], p[1] + d)

def down(p, d):
    return up(p, -d)

def right(p, d):
    return (p[0] + d, p[1])

def left(p, d):
    return right(p, -d)

def decode(line):
    operations = {
        'U': up,
        'D': down,
        'R': right,
        'L': left,
    }

    path = []
    p = (0,0)
    for part in line.split(','):
        part = part.strip()
        if len(part) > 0:
            op = part[0]
            d = int(part[1:])
            q = operations[op](p, d)
            path.append(segment(p, q))
            p = q
    return path

def intersection(seg1, seg2):
    x1 = seg1.x1
    y1 = seg1.y1
    x2 = seg1.x2
    y2 = seg1.y2
    x3 = seg2.x1
    y3 = seg2.y1
    x4 = seg2.x2
    y4 = seg2.y2

    a1 = x2 - x1
    b1 = x3 - x4
    c1 = x3 - x1

    a2 = y2 - y1
    b2 = y3 - y4
    c2 = y3 - y1

    denominator = (a1 * b2) - (a2 * b1)
    if denominator == 0:
        return None

    s0 = (c1*b2 - c2*b1) / float(denominator)
    if s0 < 0 or s0 > 1:
        return None

    t0 = (a1*c2 - a2*c1) / float(denominator)
    if t0 < 0 or t0 > 1:
        return None

    p = (x1 + s0 * (x2 - x1), y1 + s0 * (y2 - y1))
    #q = (x3 + t0 * (x4 - x3), y3 + t0 * (y4 - y3))

    return p

def intersections(path1, path2):
    results = []
    for seg1 in path1:
        for seg2 in path2:
            cross = intersection(seg1, seg2)
            if cross and cross != (0,0):
                results.append(cross)
    return results

def countsteps(path, point):
    steps = 0
    for seg in path:
        if seg.containsPoint(point):
            steps += manhattan(seg.p, point)
            break
        else:
            steps += manhattan(seg.p, seg.q)
    return steps

if __name__ == "__main__":
    line1 = sys.stdin.readline()
    path1 = decode(line1)
    line2 = sys.stdin.readline()
    path2 = decode(line2)
    points = intersections(path1, path2)
    result = countsteps(path1, points[0]) + countsteps(path2, points[0])
    for point in points[1:]:
        steps = countsteps(path1, point) + countsteps(path2, point)
        result = min(result, steps)
    print result
