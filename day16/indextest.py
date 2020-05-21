import fileinput
import numpy
import re
import sys

def generate_indices(n, length, phase):
    assert phase >= 1
    step = (n + 1) * 4

    if phase == 1:
        for offset in range(n+1):
            index = n + offset
            while index < length:
                yield (index, 1)
                index += step
            index = 3 * n + 2 + offset
            while index < length:
                yield (index, -1)
                index += step

    else:
        for offset in range(n+1):
            index = n + offset
            while index < length:
                for sub_index, sign in generate_indices(index, length, phase-1):
                    yield (sub_index, sign)
                index += step
            index = 3 * n + 2 + offset
            while index < length:
                for sub_index, sign in generate_indices(index, length, phase-1):
                    yield (sub_index, -sign)
                index += step

if __name__ == "__main__":
    length = 8
    if len(sys.argv) > 1:
        length = int(sys.argv[1])

    phases = 1
    if len(sys.argv) > 2:
        phases = int(sys.argv[2])

    print >> sys.stderr, "length:", length, "phases:", phases

    fft = numpy.zeros((length, length), dtype=int)
    for n in range(length):
        for index, sign in generate_indices(n, length, 1):
            fft[n,index] = sign

    for phase in range(1, phases):
        fft = fft.dot(fft)

    for n, row in enumerate(fft):
        indices = [0] * length
        for index, sign in generate_indices(n, length, phases):
            indices[index] += sign
        for a, b in zip(row, indices):
            if a != b:
                print '{}:'.format(n), row, indices
                sys.exit()

    print "all good!"
