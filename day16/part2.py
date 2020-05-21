import fileinput
import numpy
import re
import sys

def multipliers(n, phases):
    fft = numpy.zeros((n, n), dtype=numpy.float64)
    for i in range(n):
        for j in range(n):
            if i <= j:
                fft[i,j] = 1

    for phase in range(phases):
        fft = fft.dot(fft)

    return fft[0]

if __name__ == "__main__":
    phases = 4
    for index, arg in enumerate(sys.argv):
        result = re.match('-(\d+)$', arg)
        if result:
            phases = int(result.group(1))
            del sys.argv[index]
            break

    input_signal = fileinput.input().next().strip()

    message_offset = int(input_signal[0:7])
    input_length = len(input_signal)
    output_length = 8

    m = multipliers(output_length, phases)
    print m

    output_signal = []
    for i in range(output_length):
        t = [input_signal[(i + j + message_offset) % input_length] for j in range(output_length)]
        sum = 0
        for a, b in zip(m, t):
            sum += a * int(b)
        output_signal.append(int(sum % 10))

    print ''.join([str(d) for d in output_signal])
