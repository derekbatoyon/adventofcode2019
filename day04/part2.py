# usage:
#   python part2.py lower_bound-upper_bound
#
# this produces all passwords matching criteria, count like:
#   python part2.py 254032-789860 | wc -l

import sys

def convert(list):
    result = 0
    for x in list:
        result = result * 10 + x
    return result

def correct_grouping(g):
    r = []
    y = g[0]
    n = 1
    for x in g[1:]:
        if x == y:
            n = n + 1
        else:
            r.append(n)
            n = 1
            y = x
    #print convert(g), r + [n]
    if n == 2 or 2 in r:
        return True

def guess(digits, l=0, u=9):
    if digits == 1:
        for x in range(l, u+1):
            yield [x]
    else:
        for x in range(l, u+1):
            for g in guess(digits-1, x, u):
                yield [x] + g

def generate_guesses(digits=6):
    for g in guess(digits):
        if correct_grouping(g):
            yield convert(g)

if __name__ == "__main__":
    assert not correct_grouping([1, 2, 3, 7, 8, 9])
    assert correct_grouping([1, 1, 2, 2, 3, 3])
    assert not correct_grouping([1, 2, 3, 4, 4, 4])
    assert correct_grouping([1, 1, 1, 1, 2, 2])

    (l, u) = sys.argv[1].split('-', 2)
    lower = int(l)
    upper = int(u)
    for g in generate_guesses():
        if g >= lower and g <= upper:
            print g
