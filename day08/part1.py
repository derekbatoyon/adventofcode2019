# usage:
#   python part1.py width height image_file

import sys

def analyze(layer):
    results = {digit:0 for digit in range(10)}
    for d in layer:
        digit = int(d)
        results[digit] = results[digit] + 1
    return results
        
if __name__ == "__main__":
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    pixels = width * height

    results = []
    with open(sys.argv[3]) as fh:
        while True:
            layer = fh.read(pixels).strip()
            if len(layer) == 0:
                break
            results.append(analyze(layer))

    results.sort(key = lambda item : item[0])
    print results[0][1] * results[0][2]
