# usage:
#   python part1.py [file ...]
#
# The file operands are processed in command-line order.  If file is a single
# dash (`-') or absent, reads from the standard input.  Only two lines of input
# are read, one for each wire.

from fileinput import FileInput

class segment:
    def __init__(self, p, q):
        self.x1 = p[0]
        self.y1 = p[1]
        self.x2 = q[0]
        self.y2 = q[1]
    def __str__(self):
        return "{} {}".format( (self.x1, self.y1), (self.x2, self.y2) )

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

if __name__ == "__main__":
    fi = FileInput()
    path1 = decode(fi.readline())
    path2 = decode(fi.readline())
    results = intersections(path1, path2)
    results.sort(key=manhattan)
    print results
    print manhattan(results[0])
