import fileinput
import re
import sys

def generate_pattern(base, repeat):
    while True:
        for digit in base:
            for i in range(repeat):
                yield digit

if __name__ == "__main__":
    phases = 4
    for index, arg in enumerate(sys.argv):
        result = re.match('-(\d+)$', arg)
        if result:
            phases = int(result.group(1))
            del sys.argv[index]
            break

    base_pattern = [0, 1, 0, -1]

    input_signal = [int(c) for c in fileinput.input().next().strip()]
    length = len(input_signal)
    output_signal = [None] * length

    #print >> sys.stderr, ''.join([str(digit) for digit in input_signal])
    for phase in range(phases):
        for i in range(length):
            pattern = generate_pattern(base_pattern, i+1)
            pattern.next()
            total = sum([input * multiplier for input, multiplier in zip(input_signal, pattern)])
            output_signal[i] = abs(total) % 10
        #print >> sys.stderr, ''.join([str(digit) for digit in output_signal])
        input_signal = output_signal

    print ''.join([str(digit) for digit in output_signal[:8]])
