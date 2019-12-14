# usage:
#   python part1.py lower_bound-upper_bound
#
# this produces all passwords matching criteria, count like:
#   python part1.py 254032-789860 | wc -l

import sys

def convert(list):
    result = 0
    for x in list:
        result = result * 10 + x
    return result

def repeating(g):
    y = g[0]
    for x in g[1:]:
        if x == y:
            return True
        y = x

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
        if repeating(g):
            yield convert(g)

if __name__ == "__main__":
    assert not repeating([1, 2, 3, 7, 8, 9])
    assert repeating([1, 2, 3, 7, 7, 9])

    (l, u) = sys.argv[1].split('-', 2)
    lower = int(l)
    upper = int(u)
    for g in generate_guesses():
        if g >= lower and g <= upper:
            print g
