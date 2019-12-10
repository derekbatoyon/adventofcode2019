# usage:
#   python permutations.py <sequence to permute>

import sys

def permutations(sequence, length=None):
    if length is None:
        length = len(sequence)
    if length == 1:
        for x in sequence:
            yield [x]
    else:
        for i, x in enumerate(sequence):
            subsequence = sequence[:]
            del subsequence[i]
            for s in permutations(subsequence, length-1):
                yield [x] + s

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sequence = [int(i) for i in sys.argv[1].split(',')]
    else:
        sequence = [int(i) for i in range(5)]

    for permutation in permutations(sequence):
        print ",".join([str(x) for x in permutation])
